import os
import tempfile
import heapq
import collections
import logging
import itertools
import math
import shlex
import random
import subprocess
from tcc3 import Error
from tcc3.registry import Registry
from tcc3.util import system_command, Counter

import numpy

logger = logging.getLogger("tcc3.method")

class MethodError(Error):
    pass

class SVMError(MethodError):
    pass

WINDOW_CPU_INDEX = 0

class Method(object):

    def __init__(self, config, maindb, traindb):
        self.config = config
        self.maindb = maindb
        self.traindb = traindb
        self.nfuturevalues = int(config.future_values)
        self.maxcpuval = float(config.max_cpu_value)
        self.nranges = int(config.cpu_usage_ranges)
        self.skip_zeroes = bool(int(config.skip_zeroes))

    def train(self, machine):
        raise NotImplementedError

    def predict(self, machine, window):
        raise NotImplementedError

class WindowGeneratorMixIn(object):

    def class_from_cpu_use(self, value, ranges=None):
        "A value identifiying the range (class) @value is part"
        if ranges is None:
            ranges = self.nranges
        if value == self.maxcpuval:
            return ranges - 1
        class_ = int((value / self.maxcpuval) * ranges)
        return class_

    def make_future_values(self, examples, allvalues):
        # the return value must be 'compatible' with the raw cpu load
        # value, as it is used with class_from_cpu_use()
        total = 0.0
        # it uses allvalues because 'examples' is already normalized
        for i, example in examples:
            total += allvalues[i][WINDOW_CPU_INDEX] # 0 is the index of the cpu load
        return total / len(examples)
        #return float(sum(allvalues[i][cpuidx]
        #        for i, example in examples)) / len(examples) # avg

    def categorize_window(self, values):
        ranges = self.nranges
        for value in values:
            class_ = self.class_from_cpu_use(value, ranges=ranges)
            for i in xrange(ranges):
                yield int(i == class_)

    def load_values(self, machine, db=None):
        values = []
        if db is None:
            db = self.maindb
        for rawcols in db.values(machine):
            cols = []
            for i, raw in enumerate(rawcols):
                if i == 0: # cpu value
                    cols.append(self.maxcpuval - float(raw))
                else:
                    cols.append(float(raw))
            values.append(cols)
        return values

    def build_candidate(self, example):
        candidate = []
        for cols in example:
            #FIXME consider grouping by type
            candidate.extend(cols)
        return candidate

    def invalid_example(self, window, winsize, allvalues):
        return 0 == sum(x[WINDOW_CPU_INDEX] for x in window)

    def normalize_values(self, candidates):
        # http://docs.google.com/viewer?a=v&q=cache:_sFjFz5OMOgJ:ir.iit.edu/~dagr/DataMiningCourse/Spring2001/Notes/Data_Preprocessing.pdf+sigmoidal+normalization&hl=en&pid=bl&srcid=ADGEESjENwqav9GUs0VinnhtyH_CLJKWMjuxV4yrOsX8DYjPlXhTDTDQltrnhWK91HQEWdl-nQswNUECMs-iLPeIp5qpxFm5ZovgV7q_J9QxzZg0SzTqN2fD7BtC542N6IU_aM09aWtZ&sig=AHIEtbRtN8FYbICbfU0-P0Rvjve4o8kAZQ
        if not candidates:
            return []
        cols = len(candidates[0])
        max = [0.0] * cols
        min = [0.0] * cols
        std = [0.0] * cols
        avg = [0.0] * cols
        for i in xrange(cols):
            values = numpy.array([cand[i] for cand in candidates],
                    dtype=float)
            max[i] = values.max()
            min[i] = values.min()
            std[i] = numpy.std(values)
            avg[i] = numpy.average(values)
        new = []
        for cand in candidates:
            newcand = []
            for i in xrange(cols):
                if i == WINDOW_CPU_INDEX: # cpu use
                    #newval = float(self.class_from_cpu_use(cand[i])) / self.nranges
                    newval = cand[i] / 100.0
                else:
                    alpha = (cand[i] - avg[i]) / std[i]
                    ae = math.exp(-alpha)
                    newval = (1 - ae) / (1 + ae)
                newcand.append(newval)
            new.append(newcand)
        return new

    def build_examples(self, machine, winsize, db=None):
        """Returns windows + classification with one value of delay

        This is one example of how one window + class is formed:

        ... [ 66 11 56 22 78 44 ] avg(<<14 15 16 17 18>>) ...

        [] indicates values used to form the window, 98 is the value ignore
        for the classification, which is kept in a 'limbo', and 14 is the
        value to be used as the classification.
        """
        pendingdist = -1
        lag = 0 # const actually
        curwin = collections.deque()
        limbo = None
        needed = winsize + lag + self.nfuturevalues
        allvalues = self.load_values(machine, db=db)
        normvalues = self.normalize_values(allvalues)
        skipped = 0
        for i, values in enumerate(normvalues):
            curwin.append((i, tuple(values)))
            if len(curwin) >= needed:
                window = tuple(value for j, value in curwin)[:winsize]
                # :-winsize as we may want to have a lag between the window
                # and the values used to compute the 'future'
                future = tuple(curwin)[:-winsize]
                transf = self.make_future_values(future, allvalues)
                class_ = self.class_from_cpu_use(transf)
                candidate = self.build_candidate(window)
                if not (self.skip_zeroes and
                        self.invalid_example(window, winsize, allvalues)):
                    assert len(candidate) == winsize
                    yield candidate, class_
                else:
                    skipped += 1
                curwin.popleft()
        yield ([0.0]*winsize, 0)
        self.logger.debug("skipped windows: %d", skipped)
        assert len(curwin) == needed - 1 # -1 as we have .popleft()

class KNNMethod(Method, WindowGeneratorMixIn):

    def __init__(self, config, maindb, traindb):
        super(KNNMethod, self).__init__(config, maindb, traindb)
        self.neighbours = int(config.knn_number_neighbours)
        self.testsize = int(config.knn_test)
        self.trainsize = int(config.knn_train)
        self.windowsize = int(config.window_size)
        self.test_dir = shlex.split(config.svm_test_dir)[0]
        self.logger = logging.getLogger("tcc3.method.knn")
        self.logger.debug("created KNN instance with N = %d",
                self.neighbours)
        self._examples = {}

    def _test_file_name(self, machine):
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        return os.path.join(self.test_dir, "%s" % (machine))

    def train(self, machine):
        examples = list(self.build_examples(machine, self.windowsize,
            db=self.maindb))
        random.shuffle(examples)
        self.traindb.destroy(machine)
        for i in xrange(self.trainsize):
            example, class_ = examples[i]
            line = list(example)
            line.append(class_)
            self.traindb.add(line, machine)
        path = self._test_file_name(machine)
        f = open(path, "w")
        for i in xrange(self.trainsize, self.trainsize+self.testsize):
            example, class_ = examples[i]
            line = (" ".join(str(value) for value in example)
                    + " %d" % (class_))
            f.write(line + "\n")
        f.close()

    def _distance(self, one, another):
        dist = 0.0
        for i, onesvalue in enumerate(one):
            dist += math.pow(onesvalue - another[i], 2)
        return math.sqrt(dist)

    def _build_predict_examples(self, machine):
        for entry in self.traindb.values(machine):
            values = [float(raw) for raw in entry[:-1]]
            assert values[0] <= 1.00
            class_ = int(entry[-1])
            yield values, class_

    def _predict(self, window, examples):
        winsize = len(window)
        candidates = []
        normalized = [val/self.maxcpuval for val in window]
        for candidate, class_ in examples:
            dist = self._distance(candidate, normalized)
            info = (-dist, class_)
            if len(candidates) < self.neighbours:
                # grow the neighbours list up to its size
                heapq.heappush(candidates, info)
            elif dist <= -candidates[0][0]:
                # replace candidates which have distance smaller than the
                # most distant in the selected neighbours
                heapq.heappushpop(candidates, info)
        self.logger.debug("candidates: %r", candidates)
        count = Counter(class_ for dist, class_ in candidates)
        return count.most_common()[0][0]

    def predict(self, machine, window):
        if machine not in self._examples:
            self._examples[machine] = list(self._build_predict_examples(machine))
        return self._predict(window, self._examples[machine])

    def test(self, machine):
        path = self._test_file_name(machine)
        total = 0
        correct = 0
        for line in open(path):
            rawvalues = line.split()
            example = [self.maxcpuvalue * float(rawvalue) for rawvalue in rawvalues[:-1]]
            correctclass_ = int(rawvalues[-1])
            predicted = self.predict(machine, example)
            if predicted == correctclass_:
                correct += 1
            total += 1
        self.logger.info("total/correct: %d/%d", total, correct)

class AutoRegressiveMethod(Method, WindowGeneratorMixIn):

    def __init__(self, config, maindb, traindb):
        super(AutoRegressiveMethod, self).__init__(config, maindb, traindb)
        self.ncoefs = int(config.ar_coefs)

    def _dump_coefs(self, coefs, machine):
        self.traindb.destroy(machine)
        self.traindb.add(coefs, machine)

    def train(self, machine):
        from nitime.algorithms.autoregressive import AR_est_YW
        allvalues = self.load_values(machine)
        normvalues = self.normalize_values(allvalues)
        values = numpy.array([sample[WINDOW_CPU_INDEX] for sample in normvalues])
        coefs, sig_sq = AR_est_YW(values, self.ncoefs)
        self._dump_coefs(coefs, machine)

    def predict(self, machine, window):
        raise NotImplementedError

class TendencyBasedMethod(Method, WindowGeneratorMixIn):

    def __init__(self, *args, **kwargs):
        super(TendencyBasedMethod, self).__init__(*args, **kwargs)
        self.increment = 1.0
        self.decrement = 1.0
        self.adaptdegree = 1.0
        self.avg = None
        self.logger = logging.getLogger("tcc3.method.tendency")

    def train(self, machine):
        import numpy
        allvalues = numpy.array(self.load_values(machine))
        values = numpy.array([sample[WINDOW_CPU_INDEX] for sample in allvalues])
        avg = numpy.average(values)
        self.traindb.destroy(machine)
        self.traindb.add((avg,), machine)

    def predict(self, machine, window):
        # gather data about the whole training set
        if self.avg is None:
            for values in self.traindb.values(machine):
                self.avg = float(values[0])
                break
            else:
                raise MethodError, "you must run tcc3-train beforehand"
        self.logger.debug("avg: %f", self.avg)
        #
        # the prediction:
        cur = window[-1]
        prev = window[-2]
        diff = cur - prev
        if diff > 0:
            # tendency: increase
            newval = cur + self.increment
            # "increment adaptation process"
            incvalue = cur - newval
            self.increment = self.increment + ((incvalue - self.increment) *
                                self.adaptdegree)
        elif diff == 0:
            # tendency: stabilize
            newval = cur
        else:
            # tendency: decrease
            newval = cur - self.decrement
            # "decrement adaptation process"
            decvalue = cur - newval
            self.decrement = self.decrement + ((decvalue - self.decrement) *
                                self.adaptdegree)
        # now convert this value to the identifier of a value range, as we
        # use in svm method TODO: change predict in all other classes to
        # return the "worst case" for each class, this way we benefit those
        # methods that can return a more precise cpu prediction
        self.logger.debug("newval: %d", newval)
        newval = min(newval, 100.0)
        return self.class_from_cpu_use(newval)

class SVMBaseMethod(Method, WindowGeneratorMixIn):

    def __init__(self, config, maindb, traindb):
        super(SVMBaseMethod, self).__init__(config, maindb, traindb)
        self.maindb = maindb
        self.traindb = traindb
        self.windowsize = int(config.window_size)
        self.samples = int(config.svm_samples)
        self.ntest = int(config.svm_test)
        self.trained_dir = shlex.split(config.svm_trained_dir)[0]
        self.test_dir = shlex.split(config.svm_test_dir)[0]
        self.logger = logging.getLogger("tcc3.method.svm")
        self.logger.debug("created SVM instance with windowsize = %d",
                self.windowsize)


    def select_samples(self, problx, probly):
        # burn memory burn!!
        pairs = list(enumerate(problx))
        random.shuffle(pairs)
        selected = pairs[:self.samples]
        rest = pairs[self.samples:self.samples+self.ntest+1]
        resty = []
        restx = [value for _, value in rest]
        newprobly = []
        newproblx = [value for _, value in selected]
        for i in xrange(len(probly)):
            ys = []
            for j, x in selected:
                ys.append(probly[i][j])
            newprobly.append(ys)
            ys = []
            for j, x in rest:
                ys.append(probly[i][j])
            resty.append(ys)
        return newproblx, newprobly, restx, resty

    def select_winner(self, values):
        return sorted([(value, i) for i, value in enumerate(values)],
                reverse=True)[0][1]

    def prepare_examples(self, machine):
        problx = []
        probly = [[] for i in xrange(self.nranges)] # n svms = n classes
        self.logger.debug("creating 'training problem' vectors")
        for candidate, class_ in self.build_examples(machine, self.windowsize):
            problx.append(candidate)
            for i in xrange(self.nranges):
                if class_ == i:
                    probly[i].append(1)
                else:
                    probly[i].append(-1)
        return self.select_samples(problx, probly)

    def _class_file_name(self, machine, i):
        return os.path.join(self.trained_dir, "%s-%02d" % (machine, i))

    def _test_file_name(self, machine, i):
        return os.path.join(self.test_dir, "%s-%02d" % (machine, i))

    def _dump_rest(self, machine, restx, resty):
        for i, ys in enumerate(resty):
            path = self._test_file_name(machine, i)
            dir = os.path.dirname(path)
            if not os.path.exists(dir):
                self.logger.debug("created %s" % (dir))
                os.makedirs(dir)
            f = open(path, "w")
            self.logger.debug("writing test entries to %s" % (path))
            f.writelines(self.dump_libsvm_line(cand, ys[j])
                    for j, cand in enumerate(restx))
            f.close()

    def train(self, machine):
        problx, probly, restx, resty = self.prepare_examples(machine)
        self._dump_rest(machine, restx, resty)
        trainedfiles = []
        if not os.path.exists(self.trained_dir):
            logger.debug("creating directory %s", self.trained_dir)
            os.makedirs(self.trained_dir)
        for i, ys in enumerate(probly):
            trainfile = tempfile.mktemp(prefix="training.%02d" % (i),
                    dir=self.trained_dir)
            tf = open("/tmp/svm-%d.txt" % (i), "w")
            for j, y in enumerate(ys):
                line = self.dump_libsvm_line(problx[j], y)
                tf.write(line)
            tf.flush()
            args = self.learn_cmd[:]
            args.append(tf.name)
            args.append(trainfile)
            self.logger.debug("running: %r", args)
            system_command(args, show=True)
            tf.close()
            dbtrained = self._class_file_name(machine, i)
            trainedfiles.append((trainfile, dbtrained))
        for trainfile, dbtrained in trainedfiles:
            self.logger.debug("renaming %s to %s", trainfile, dbtrained)
            os.rename(trainfile, dbtrained)

    def _generic_class_file(self, class_):
        path = os.path.join(self.trained_dir, "generic-%02d" % (class_))
        return path

    def predict(self, machine, rawcandidate):
        from tcc3.collector import parse_vmstat_fieldslist
        vmstatfields = parse_vmstat_fieldslist(self.config.vmstat_fields)

        # for now we only handle candidates with only cpu readings
        assert len(vmstatfields) == 1

        if len(vmstatfields) * self.windowsize != len(rawcandidate):
            raise MethodError, ("invalid candidate, expected %d values" %
                    (len(vmstatfields) * self.windowsize))


        tf = tempfile.NamedTemporaryFile()
        windows = [[val] for val in rawcandidate]
        cand = self.normalize_values(windows)
        self.logger.debug("normalized candidate: %r", cand)
        line = self.dump_libsvm_line((col[0] for col in cand), 0)
        tf.write(line)
        tf.flush()
        classes = []
        outfiles = []
        procs = []
        for i in xrange(self.nranges):
            outfile = tempfile.mktemp()
            outfiles.append(outfile)
            path = self._class_file_name(machine, i)
            if not os.path.exists(path):
                newpath = self._generic_class_file(i)
                self.logger.debug("%s not found, using generic %s", path,
                        newpath)
                path = newpath
            args = self.classify_cmd[:]
            args.append(tf.name)
            args.append(path)
            args.append(outfile)
            self.logger.debug("classifier: %r", args)
            #system_command(args)
            p = subprocess.Popen(args, shell=False)
            procs.append(p)
        for p in procs:
            if p.wait() != 0:
                raise MethodError, "command %s failed!"
        for i in xrange(self.nranges):
            data = open(outfiles[i]).read().strip()
            self.logger.debug("for %d it returned %r", i, data)
            dist = float(data)
            classes.append(dist)
            os.unlink(outfiles[i])
        tf.close()
        return self.select_winner(classes)

    def test(self, machine):
        import itertools
        allresults = []
        correctresults = []
        for i in xrange(self.nranges):
            outname = tempfile.mktemp()
            testpath = self._test_file_name(machine, i)
            modelpath = self._class_file_name(machine, i)
            args = self.classify_cmd[:]
            args.append(testpath)
            args.append(modelpath)
            args.append(outname)
            self.logger.debug("running: %r" % (args))
            system_command(args, show=True)
            fout = open(outname)
            ftest = open(testpath)
            total = 0
            correct = 0
            myresults = []
            allresults.append(myresults)
            for rawout, rawtest in itertools.izip(fout, ftest):
                outval = float(rawout.strip()) < 0
                testval = float(rawtest.split()[0].strip()) < 0
                if outval == testval:
                    correct += 1
                    myresults.append(True)
                else:
                    myresults.append(False)
                total += 1
            self.logger.debug("TOTAL/CORRECT for class %d: %d/%d/%f%%", i,
                    total, correct, ((float(correct)/total)*100.0))
            ftest.close()
            fout.close()
            os.unlink(outname)
        total = None
        for i in xrange(self.nranges):
            if total is None:
                total = len(allresults[i])
            else:
                if len(allresults[i]) != total:
                    raise Error, ("eita! totais diferentes: %d vs %d" %
                            (total, len(allresults[i])))
        assert (sum(float(len(r)) for r in allresults) / self.nranges
                == len(allresults[0])) # ensure sizes are equal
        matches = 0
        for k in xrange(len(allresults[0])):
            if all(allresults[i][k] for i in xrange(self.nranges)):
                matches += 1
        perc = float(matches)/total*100.0
        self.logger.debug("MATCHES: %d / TOTAL: %d, %f%%", matches, total,
                perc)
        return "%f%%" % (perc)
            
class LibsvmDumperMixIn:

    def dump_libsvm_line(self, x, y):
        """Returns a generator dumping lines in the format of feature
        vectors used by libsvm"""
        xline = " ".join("%d:%f" % (col+1, value)
                for col, value in enumerate(x))
        line = str(y) + " " + xline + "\n"
        return line

class SVMLightMethod(SVMBaseMethod, LibsvmDumperMixIn):

    def __init__(self, config, maindb, traindb):
        super(SVMLightMethod, self).__init__(config, maindb, traindb)
        self.learn_cmd = shlex.split(config.svmlight_learn_command)
        self.classify_cmd = shlex.split(config.svmlight_classify_command)

class LibsvmMethod(SVMLightMethod):

    def __init__(self, config, maindb, traindb):
        super(SVMLightMethod, self).__init__(config, maindb, traindb)
        self.learn_cmd = shlex.split(config.libsvm_learn_command)
        self.classify_cmd = shlex.split(config.libsvm_classify_command)

class MulticlassLibsvmMethod(LibsvmMethod):

    def categorize_window(self, values):
        return values
    
    def prepare_examples(self, machine):
        all = list(self.build_examples(machine, self.windowsize))
        xs = []
        ys = []
        for x, y in all:
            xs.append(x)
            ys.append(y)
        return self.select_samples(xs, [ys])

class SVRLibsvmMethod(MulticlassLibsvmMethod):

    def class_from_cpu_use(self, cpu):
        return cpu / self.maxcpuval

methods = Registry()
methods.register("knn", KNNMethod)
methods.register("ar", AutoRegressiveMethod)
methods.register("tendency", TendencyBasedMethod)
methods.register("svm", LibsvmMethod)
methods.register("svm-multiclass", MulticlassLibsvmMethod)
methods.register("svm-svmlight", SVMLightMethod)
methods.register("svm-svr", SVRLibsvmMethod)

def get_method(config, maindb, traindb):
    return methods.get_instance(config.learning_method, config, maindb,
            traindb)
