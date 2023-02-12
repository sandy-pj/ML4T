import numpy as np
class BagLearner(object):
    def __init__(self, learner, kwargs, bags=20, boost=False, verbose=False):
        kwargs['verbose'] = verbose
        self.learners = [learner(**kwargs) for _ in range(bags)]


    def author(self):
        return 'pjiang49'

    def add_evidence(self, Xtrain, Ytrain):
        for learner in self.learners:
            indices = np.random.choice(Xtrain.shape[0], Xtrain.shape[0])
            learner.add_evidence(Xtrain[indices], Ytrain[indices])

    def query(self, Xtest):
        return np.mean([learner.query(Xtest) for learner in self.learners], axis=0)
