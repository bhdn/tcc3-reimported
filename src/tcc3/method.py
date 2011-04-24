import os
import tempfile
import heapq
import collections
import logging
import itertools
import math
import shlex
import random
from tcc3 import Error
from tcc3.registry import Registry
from tcc3.util import system_command

logger = logging.getLogger("tcc3.method")

class MethodError(Error):
    pass

class SVMError(MethodError):
    pass

class Method(object):

    def __init__(self, config, maindb, traindb):
        self.config = config
        self.maindb = maindb
        self.traindb = traindb
        self.nfuturevalues = int(config.future_values)

    def train(self, machine):
        raise NotImplementedError

    def predict(self, machine, window):
        raise NotImplementedError

class WindowGeneratorMixIn(object):

    def class_from_cpu_use(self, value):
        "A value identifiying the range (class) @value is part"
        if value == self.maxcpuval:
            return self.nranges - 1
        class_ = int((value / self.maxcpuval) * self.nranges)
        return class_

    def transform_future_values(self, values):
        return float(sum(values)) / len(values) # avg

    def build_examples(self, machine, winsize):
        """Returns windows + classification with one value of delay

        This is one example of how one window + class is formed:

        ... [ 66 11 56 22 78 44 ] avg(<<14 15 16 17 18>>) ...

        [] indicates values used to form the window, 98 is the value ignore
        for the classification, which is kept in a 'limbo', and 14 is the
        value to be used as the classification.
        """
        curwin = collections.deque()
        pendingdist = -1
        limbo = None
        needed = winsize + self.nfuturevalues
        for values in self.maindb.values(machine):
            value = self.maxcpuval - float(values[0])
            curwin.append(value)
            if len(curwin) >= needed:
                window = tuple(curwin)[:winsize]
                future = tuple(curwin)[winsize:]
                transf = self.transform_future_values(future)
                class_ = self.class_from_cpu_use(transf)
                winsum = sum(window)
                if not (winsum == 0.0 or winsum == 100.0*winsize):
                    #print "yielding", window, class_, "avg", transf, future
                    yield window, class_
                curwin.popleft()
        yield ((0.0,) * winsize), 0
        yield ((100.0,) * winsize), (self.nranges - 1)

class KNNMethod(Method, WindowGeneratorMixIn):

    def __init__(self, config, maindb, traindb):
        super(KNNMethod, self).__init___(config, maindb, traindb)
        self.neighbours = int(config.knn_number_neighbours)
        self.nranges = int(config.cpu_usage_ranges)
        self.maxcpuval = float(config.max_cpu_value)
        self.logger = logging.getLogger("tcc3.method.knn")
        self.logger.debug("created KNN instance with N = %d",
                self.neighbours)

    def train(self, machine):
        self.logger.info("pretending to be trainning a K-NN for %s",
                machine)

    def _distance(self, one, another):
        dist = 0.0
        for i, onesvalue in enumerate(one):
            dist += math.pow(onesvalue - another[i], 2)
        return math.sqrt(dist)

    def predict(self, machine, window):
        winsize = len(window)
        candidates = []
        for candidate, class_ in self.build_examples(machine, winsize):
            dist = self._distance(candidate, window)
            info = (-dist, class_)
            if len(candidates) < self.neighbours:
                # grow the neighbours list up to its size
                heapq.heappush(candidates, info)
            elif dist <= -candidates[0][0]:
                # replace candidates which have distance smaller than the
                # most distant in the selected neighbours
                heapq.heappushpop(candidates, info)
        self.logger.debug("candidates: %r", candidates)
        count = collections.Counter(class_ for dist, class_ in candidates)
        return count.most_common()[0][0]

class SVMBaseMethod(Method, WindowGeneratorMixIn):

    def __init__(self, config, maindb, traindb):
        super(SVMBaseMethod, self).__init__(config, maindb, traindb)
        self.maindb = maindb
        self.traindb = traindb
        self.windowsize = int(config.svm_window_size)
        self.nranges = int(config.cpu_usage_ranges)
        self.maxcpuval = float(config.max_cpu_value)
        self.samples = int(config.svm_samples)
        self.ntest = int(config.svm_test)
        self.trained_dir = shlex.split(config.svm_trained_dir)[0]
        self.test_dir = shlex.split(config.svm_test_dir)[0]
        self.logger = logging.getLogger("tcc3.method.svm")
        self.logger.debug("created SVM instance with windowsize = %d",
                self.windowsize)

    def normalize(self, candidate):
        normcand = [(val / self.maxcpuval) for val in candidate]
        return normcand

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
            normcand = self.normalize(candidate)
            problx.append(normcand)
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

    def predict(self, machine, window):
        tf = tempfile.NamedTemporaryFile()
        cand = self.normalize(window)
        self.logger.debug("normalized candidate: %r", cand)
        line = self._dump_svmlight_line(cand, 0)
        tf.write(line)
        tf.flush()
        classes = []
        for i in xrange(self.nranges):
            outfile = tempfile.mktemp()
            path = self._class_file_name(i)
            args = self.classify_cmd[:]
            args.append(tf.name)
            args.append(path)
            args.append(outfile)
            self.logger.debug("classifier: %r", args)
            system_command(args)
            data = open(outfile).read().strip()
            self.logger.debug("for %d it returned %r", i, data)
            dist = float(data)
            classes.append(dist)
            os.unlink(outfile)
        tf.close()
        return self.select_winner(classes)

    def test(self, machine):
        import itertools
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
            for rawout, rawtest in itertools.izip(fout, ftest):
                outval = float(rawout.strip()) < 0
                testval = float(rawtest.split()[0].strip()) < 0
                if outval == testval:
                    correct += 1
                total += 1
            print "TOTAL/CORRECT:", total, correct, ((float(correct)/total)*100.0)
            ftest.close()
            fout.close()
            os.unlink(outname)

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

methods = Registry()
methods.register("knn", KNNMethod)
methods.register("svm", LibsvmMethod)
methods.register("svm-svmlight", SVMLightMethod)

def get_method(config, maindb, traindb):
    return methods.get_instance(config.learning_method, config, maindb,
            traindb)
