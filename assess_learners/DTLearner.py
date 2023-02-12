import numpy as np
class DTLearner(object):

    def __init__(self, leaf_size, verbose):

        self.leaf_size = leaf_size
        self.verbose = verbose
        self.root  = None
        self.selected_feature_idx = -1


    def author(self):
        return 'pjiang49'

    def add_evidence(self, Xtrain, Ytrain):

        self._select_feature(Xtrain, Ytrain)
        self.root = self._build_tree(Xtrain[:,self.selected_feature_idx], Ytrain)

    def query(self, XTest):
        feature = XTest[:, self.selected_feature_idx]

        return np.array([self._one_point_query(item) for item in feature])

    def _one_point_query(self, val):
        is_leaf = False
        cur_node = self.root
        cur_row = 0
        epsilon = 1e-4
        while not is_leaf:
            if val <= self.root[cur_row][1]:
                cur_row += int(self.root[cur_row][2]+epsilon)
            else:
                cur_row += int(self.root[cur_row][3]+epsilon)
            is_leaf = self.root[cur_row][0]

        return self.root[cur_row][1]

    def _build_tree(self, X, Y):
        if len(X) <= self.leaf_size:
            return np.array([[True, np.mean(Y), np.nan, np.nan]])
        if len(np.unique(X)) == 1:
            return np.array([[True, np.mean(Y), np.nan, np.nan]])
        split_val =  np.median(X)

        if len(X[X<=split_val]) == len(X) or len(X[X>split_val]) == len(X):
            return np.array([[True, np.mean(Y), np.nan, np.nan]])

        left_node =  self._build_tree(X[X<=split_val], Y[X<=split_val])
        right_node = self._build_tree(X[X> split_val], Y[X > split_val])

        root = np.array([[False, split_val, 1, len(left_node) + 1]])
        return np.append(np.append(root, left_node,axis=0), right_node, axis=0)

    def _select_feature(self, Xtrain, Ytrain):

        num_features = Xtrain.shape[1]

        best_corr = -10;
        
        for idx in  range(num_features):
            corr = abs(np.corrcoef(Xtrain[:, idx], Ytrain)[0,1])

            if corr > best_corr:
                best_corr = corr
                self.selected_feature_idx =  idx

        return
            

