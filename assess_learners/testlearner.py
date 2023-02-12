""""""  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
Test a learner.  (c) 2015 Tucker Balch  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
"""  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import math  		  	   		  		 			  		 			     			  	 
import sys  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import numpy as np  		  	   		  		 			  		 			     			  	 
import LinRegLearner as lrl
import DTLearner as dtl
import RTLearner as rtl
import BagLearner as bl
import InsaneLearner as il

if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    if len(sys.argv) != 2:  		  	   		  		 			  		 			     			  	 
        print("Usage: python testlearner.py <filename>")  		  	   		  		 			  		 			     			  	 
        sys.exit(1)  		  	   		  		 			  		 			     			  	 
    inf = open(sys.argv[1])
    data = np.array(
        [list(map(float, s.strip().split(",")[1:])) for s in inf.readlines() if  not s.startswith('date') ]
    )

    # compute how much of the data is training and testing  		  	   		  		 			  		 			     			  	 
    train_rows = int(0.6 * data.shape[0])  		  	   		  		 			  		 			     			  	 
    test_rows = data.shape[0] - train_rows  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # separate out training and testing data  		  	   		  		 			  		 			     			  	 
    train_x = data[:train_rows, 0:-1]  		  	   		  		 			  		 			     			  	 
    train_y = data[:train_rows, -1]  		  	   		  		 			  		 			     			  	 
    test_x = data[train_rows:, 0:-1]  		  	   		  		 			  		 			     			  	 
    test_y = data[train_rows:, -1]  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    print(f"{test_x.shape}")  		  	   		  		 			  		 			     			  	 
    print(f"{test_y.shape}")  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # create a learner and train it  		  	   		  		 			  		 			     			  	 
#    learner = lrl.LinRegLearner(verbose=True)  # create a LinRegLearner

    
    ### Experiment 1
    import matplotlib.pyplot as plt
    rmse_res = []
    for l_size in range(1, 100):
        learner = dtl.DTLearner(leaf_size=l_size, verbose=False)


        learner.add_evidence(train_x, train_y)  # train it

        # evaluate in sample
        pred_y = learner.query(train_x)  # get the predictions
        rmse = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])
#        print()
#        print("In sample results")
#        print(f"RMSE: {rmse}")
        c = np.corrcoef(pred_y, y=train_y)
#        print(f"corr: {c[0,1]}")

        # evaluate out of sample
        pred_y = learner.query(test_x)  # get the predictions
        rmse = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
        rmse_res.append(rmse)
#        print()
#        print("Out of sample results")
#        print(f"RMSE: {rmse}")
        c = np.corrcoef(pred_y, y=test_y)
#        print(f"corr: {c[0,1]}")
    plt.plot(range(1, 100), rmse_res)
    plt.title('DTLearner RMSE with respect to leaf size')
    plt.savefig('./DTLearner_leaf_size_rmse.png')
#    plt.show()
    plt.clf()
    ### Experiment 2
    import matplotlib.pyplot as plt
    bag_rmse_res = []
    for l_size in range(1, 100):
        learner = bl.BagLearner(learner=dtl.DTLearner, kwargs={"leaf_size": l_size}, bags=10, boost=False,verbose=False)


        learner.add_evidence(train_x, train_y)  # train it

        # evaluate in sample
        pred_y = learner.query(train_x)  # get the predictions
        rmse = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])
#        print()
#        print("In sample results")
#        print(f"RMSE: {rmse}")
        c = np.corrcoef(pred_y, y=train_y)
#        print(f"corr: {c[0,1]}")

        # evaluate out of sample
        pred_y = learner.query(test_x)  # get the predictions
        rmse = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
        bag_rmse_res.append(rmse)
#        print()
#        print("Out of sample results")
#        print(f"RMSE: {rmse}")
        c = np.corrcoef(pred_y, y=test_y)
#        print(f"corr: {c[0,1]}")
    plt.plot(range(1, 100), rmse_res, label='DTLearner')
    plt.plot(range(1, 100), bag_rmse_res, label='BagLearner')
    plt.legend()

    plt.title('BagLearner bags=10 RMSE with respect to leaf size')
    plt.savefig('./BagLearner_10_bags_leaf_size_rmse.png')
    plt.clf()

    ### Experiment 3
    import time
    dt_times = []
    bag_dt_r_square_res = []
    for bag_size in range(1, 50):
        start = time.time()
        learner = bl.BagLearner(learner=dtl.DTLearner, kwargs={"leaf_size": 10}, bags=bag_size, boost=False,verbose=False)
        learner.add_evidence(train_x, train_y)  # train it
        end = time.time()
        # evaluate in sample
#        pred_y = learner.query(train_x)  # get the predictions
#
#        # evaluate out of sample
        pred_y = learner.query(test_x)  # get the predictions
        R_square = 1-((test_y-pred_y)**2).sum()/((test_y-np.mean(test_y)**2).sum())
        dt_times.append(end -start)

        bag_dt_r_square_res.append(R_square)


    rt_times = []
    bag_rt_r_square_res = []
    for bag_size in range(1, 50):
        start = time.time()
        learner = bl.BagLearner(learner=rtl.RTLearner, kwargs={"leaf_size": 10}, bags=bag_size, boost=False,verbose=False)
        learner.add_evidence(train_x, train_y)  # train it
        end = time.time()

        rt_times.append(end-start)
        ## evaluate in sample
        #pred_y = learner.query(train_x)  # get the predictions

        ## evaluate out of sample
        pred_y = learner.query(test_x)  # get the predictions
        R_square = 1-((test_y-pred_y)**2).sum()/((test_y-np.mean(test_y)**2).sum())
        bag_rt_r_square_res.append(R_square)

    plt.plot(range(1, 50), dt_times, label='DTLearner')
    plt.plot(range(1, 50), rt_times, label='RTLearner')
    plt.legend()

    plt.title('DT/RT learner leaf_size=10 train time for different bags')
    plt.savefig('./DT_RT_bags_train_time.png')
    plt.clf()

    plt.plot(range(1, 50), bag_dt_r_square_res, label='DTLearner')
    plt.plot(range(1, 50), bag_rt_r_square_res, label='RTLearner')
    plt.legend()

    plt.title('DT/RT learner leaf_size=10 r square for different bags')
    plt.savefig('./DT_RT_bags_r_square.png')

