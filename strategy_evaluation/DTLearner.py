""""""
"""  		  	   		  		 			  		 			     			  	 
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		  	   		  		 			  		 			     			  	 
Note, this is NOT a correct DTLearner; Replace with your own implementation.  		  	   		  		 			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		  		 			  		 			     			  	 
All Rights Reserved  		  	   		  		 			  		 			     			  	 

Template code for CS 4646/7646  		  	   		  		 			  		 			     			  	 

Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		  		 			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		  		 			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		  		 			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 			  		 			     			  	 
or edited.  		  	   		  		 			  		 			     			  	 

We do grant permission to share solutions privately with non-students such  		  	   		  		 			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		  		 			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 			  		 			     			  	 
GT honor code violation.  		  	   		  		 			  		 			     			  	 

-----do not edit anything above this line---  		  	   		  		 			  		 			     			  	 

Student Name: Peilun Jiang (replace with your name)  		  	   		  		 			  		 			     			  	 
GT User ID: pjiang49 (replace with your User ID)  		  	   		  		 			  		 			     			  	 
GT ID: 903561681 (replace with your GT ID)  		  	   		  		 			  		 			     			  	 
"""

import warnings

import numpy as np


class DTLearner(object):
    """
    This is a decision tree learner object that is implemented incorrectly. You should replace this DTLearner with
    your own correct DTLearner from Project 3.

    :param leaf_size: The maximum number of samples to be aggregated at a leaf, defaults to 1.
    :type leaf_size: int
    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.
    :type verbose: bool
    """

    def __init__(self, leaf_size=1, verbose=False):
        """
        Constructor method
        """
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.root = None
        self.selected_feature_idx = -1

    def author(self):
        """
        :return: The GT username of the student
        :rtype: str
        """
        return "pjiang49"  # replace tb34 with your Georgia Tech username

    def add_evidence(self, Xtrain, Ytrain):
        """
        Add training data to learner

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """

        self._select_feature(Xtrain, Ytrain)
        self.root = self._build_tree(Xtrain[:, self.selected_feature_idx], Ytrain)

    def query(self, XTest):
        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        feature = XTest[:, self.selected_feature_idx]

        return np.array([self._one_point_query(item) for item in feature])

    def _one_point_query(self, val):
        is_leaf = False
        cur_node = self.root
        cur_row = 0
        epsilon = 1e-4
        while not is_leaf:
            if val <= self.root[cur_row][1]:
                cur_row += int(self.root[cur_row][2] + epsilon)
            else:
                cur_row += int(self.root[cur_row][3] + epsilon)
            is_leaf = self.root[cur_row][0]

        return self.root[cur_row][1]

    def _build_tree(self, X, Y):
        if len(X) <= self.leaf_size:
            return np.array([[True, np.mean(Y), np.nan, np.nan]])
        if len(np.unique(X)) == 1:
            return np.array([[True, np.mean(Y), np.nan, np.nan]])
        split_val = np.median(X)

        if len(X[X <= split_val]) == len(X) or len(X[X > split_val]) == len(X):
            return np.array([[True, np.mean(Y), np.nan, np.nan]])

        left_node = self._build_tree(X[X <= split_val], Y[X <= split_val])
        right_node = self._build_tree(X[X > split_val], Y[X > split_val])

        root = np.array([[False, split_val, 1, len(left_node) + 1]])
        return np.append(np.append(root, left_node, axis=0), right_node, axis=0)

    def _select_feature(self, Xtrain, Ytrain):

        num_features = Xtrain.shape[1]

        best_corr = -10;

        for idx in range(num_features):
            corr = abs(np.corrcoef(Xtrain[:, idx], Ytrain)[0, 1])

            if corr > best_corr:
                best_corr = corr
                self.selected_feature_idx = idx

        return


if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
