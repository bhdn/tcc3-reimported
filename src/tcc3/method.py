from tcc3.registry import Registry

class Method(object):

    def get_learner(self, database):
        raise NotImplementedError

    def get_predictor(self, database):
        raise NotImplementedError

class KNNMethod(Method):

    def __init__(self, config):
        self.neighbours = int(config.knn_number_neighbours)

    def get_learner(self, database):
        pass

    def get_predictor(self, database):
        pass

methods = Registry()
methods.register("knn", KNNMethod)

def get_method(config):
    return methods.get_instance(config.learning_method, config)
