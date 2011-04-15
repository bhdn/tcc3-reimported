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

    def train(self, machine):
        raise NotImplementedError

    def predict(self, machine, window):
        raise NotImplementedError

class WindowGeneratorMixIn(object):

    def _class_from_cpu_use(self, value):
        "A value identifiying the range (class) @value is part"
        if value == self.maxcpuval:
            return self.nranges - 1
        class_ = int((value / self.maxcpuval) * self.nranges)
        return class_

    def build_examples(self, machine, winsize):
        """Returns windows + classification with one value of delay

        This is one example of how one window + class is formed:

        ... [ 66 11 56 22 78 44 ] 98 <<14>> ...

        [] indicates values used to form the window, 98 is the value ignore
        for the classification, which is kept in a 'limbo', and 14 is the
        value to be used as the classification.
        """
        curwin = collections.deque()
        pendingdist = -1
        limbo = None
        for (value,) in self.maindb.values(machine):
            # the source always provides as values of 'idle' from vmstat
            value = self.maxcpuval - int(value)
            if pendingdist == 0:
                yield tuple(curwin), self._class_from_cpu_use(value)
                curwin.popleft()
                curwin.append(limbo)
                limbo = value
            elif len(curwin) == winsize:
                # time to stop filling the window and wait for the
                # classification value
                pendingdist = 1
                limbo = value
            else:
                curwin.append(value)
            # <space!>
            if pendingdist > 0:
                pendingdist -= 1

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
        newprobly = []
        newproblx = [value for _, value in selected]
        for i in xrange(len(probly)):
            ys = []
            newprobly.append(ys)
            for j, x in selected:
                ys.append(probly[i][j])
        return newproblx, newprobly

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

class SVMMethod(SVMBaseMethod):

    def __init__(self, config, maindb, traindb):
        super(SVMMethod, self).__init__(config, maindb, traindb)
        self.libsvm_dir = config.libsvm_dir
        self.params = config.libsvm_params
        self._load_libsvm()

    def _load_libsvm(self):
        import sys
        import os
        sys.path.insert(0, self.libsvm_dir)
        os.environ["LIBSVM_DIR"] = os.path.join(self.libsvm_dir, "..")
        try:
            import svm
            import svmutil
        except ImportError:
            raise SVMError, "libsvm not loadable from %s" % (self.libsvm_dir)
        self.svm = svm
        self.svmutil = svmutil
        logger.debug("loaded libsvm")

    def train(self, machine):
        problx, probly = self.prepare_examples(machine)
        svmproblems = [self.svm.svm_problem(ys, problx) for ys in probly]
        param = self.svm.svm_parameter(self.params)
        logger.debug("BEHOLD! trainning the svm")
        models = []
        for i, problem in enumerate(svmproblems):
            logger.debug("progress!")
            model = self.svm.libsvm.svm_train(problem, param)
            models.append(model)
            #self.svmutil.svm_save_model("model-%d" % (i), model)

class SVMLightMethod(SVMBaseMethod):

    def __init__(self, config, maindb, traindb):
        super(SVMLightMethod, self).__init__(config, maindb, traindb)
        self.svmlight_cmd = shlex.split(config.svmlight_command)
        self.logger.debug("svmlight comes from %s", self.svmlight_cmd)

    def train(self, machine):
        import tempfile
        problx, probly = self.prepare_examples(machine)
        for i, ys in enumerate(probly):
            trainfile = tempfile.mktemp(prefix="tcc3-%d-" % (i))
            tf = open("/tmp/svm-%d.txt" % (i), "w")
            for j, y in enumerate(ys):
                xline = " ".join("%d:%f" % (col+1, value)
                        for col, value in enumerate(problx[j]))
                line = str(y) + " " + xline + "\n"
                tf.write(line)
            tf.flush()
            args = self.svmlight_cmd[:]
            args.append(tf.name)
            args.append(trainfile)
            self.logger.debug("running: %r", args)
            system_command(args)
            tf.close()

methods = Registry()
methods.register("knn", KNNMethod)
methods.register("svm", SVMMethod)
methods.register("svm-svmlight", SVMLightMethod)

def get_method(config, maindb, traindb):
    return methods.get_instance(config.learning_method, config, maindb,
            traindb)
