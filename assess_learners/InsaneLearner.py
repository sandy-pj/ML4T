from BagLearner import BagLearner
from LinRegLearner import LinRegLearner
import numpy as np
class InsaneLearner(object):

    def __init__(self,verbose):
        self.verbose = verbose
        self.num_of_bag_learners = 20
        self.bag_learners = [ BagLearner(LinRegLearner, kwargs={}, bags=20, boost=False, verbose=False) for _ in range(self.num_of_bag_learners)]

    def author(sel):
        return 'pjiang49'

    def add_evidence(self, Xtrain, Ytrain):
        for learner in self.bag_learners:
            learner.add_evidence(Xtrain, Ytrain)

    def query(self, Xtest):
        return np.mean([learner.query(Xtest) for learner in self.bag_learners], axis=0)
