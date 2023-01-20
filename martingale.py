""""""  		  	   		  		 			  		 			     			  	 
"""Assess a betting strategy.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
  		  	   		  		 			  		 			     			  	 
Student Name: Tucker Balch (replace with your name)  		  	   		  		 			  		 			     			  	 
GT User ID: tb34 (replace with your User ID)  		  	   		  		 			  		 			     			  	 
GT ID: 900897987 (replace with your GT ID)  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def author():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    :return: The GT username of the student  		  	   		  		 			  		 			     			  	 
    :rtype: str  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    return "pjiang49"  # replace tb34 with your Georgia Tech username.
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def gtid():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    :return: The GT ID of the student  		  	   		  		 			  		 			     			  	 
    :rtype: int  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    return 903561681  # replace with your GT ID number
  		  	   		  		 			  		 			     			  	 

def get_spin_result(win_prob):
    """  		  	   		  		 			  		 			     			  	 
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param win_prob: The probability of winning  		  	   		  		 			  		 			     			  	 
    :type win_prob: float  		  	   		  		 			  		 			     			  	 
    :return: The result of the spin.  		  	   		  		 			  		 			     			  	 
    :rtype: bool  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    result = False  		  	   		  		 			  		 			     			  	 
    if np.random.random() <= win_prob:  		  	   		  		 			  		 			     			  	 
        result = True  		  	   		  		 			  		 			     			  	 
    return result  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def strategy_simulate():
    # init an array with shape (1001) and value 80
    win_prob = 0.5 # the prob of black
    result_array = np.full((1001), 0)
    episode_winnings = 0
    spin_cnt = 0
    while episode_winnings < 80 and spin_cnt < 1000:
        won = False
        bet_amount = 1

        while not won:
            won = get_spin_result(win_prob)
            spin_cnt += 1

            if won:
                episode_winnings += bet_amount
            else:
                episode_winnings -= bet_amount
                bet_amount *= 2

            result_array[spin_cnt] = episode_winnings
            # print("At spin {}: the winning amount is {}".format(spin_cnt, episode_winnings))
            if spin_cnt == 1000:
                break
    result_array[spin_cnt:] = episode_winnings
    return result_array

# ================================================
# make figure 1 to 6
def experiment1_fig1():
    # run simulator 10x and plot winnings
        # start from time 0
        # 10 arrays needed for graph
    # plot all 10 runs on one chart
        # x axis must range from 0 to 300
        # y axis must range from -256 to 100
    res = []
    for i in range(10):
        cur_episode = strategy_simulate()
        res.append(cur_episode)
    df = pd.DataFrame(res).T

    df.plot()
    plt.axis([0, 300, -256, 100])
    plt.title("Figure 1: Experiment 1 - simulate 10 episodes")
    plt.xlabel("Number of spins")
    plt.ylabel("Total winnings")
    plt.legend()

    plt.savefig("Figure1.png")
    plt.clf()

def experiment1_fig2():
    res = []
    for i in range(1000):
        episode_result = strategy_simulate()
        res.append(episode_result)

    df = pd.DataFrame(res).T
    mean_line = df.mean(axis=1)
    up_boundary = df.mean(axis=1)+df.std(axis=1)
    down_boundary = df.mean(axis=1)-df.std(axis=1)

    plt.plot(mean_line, label = "mean")
    plt.plot(up_boundary, label="up boundary")
    plt.plot(down_boundary, label="down boundary")

    plt.axis([0, 300, -256, 100])
    plt.title("Figure 2: Experiment 1 - simulate 1000 episodes")
    plt.xlabel("Number of spins")
    plt.ylabel("Total winnings")
    plt.legend()

    plt.savefig("Figure2.png")
    plt.clf()

def experiment1_fig3():
    res = []
    for i in range(1000):
        episode_result = strategy_simulate()
        res.append(episode_result)

    df = pd.DataFrame(res).T
    mean_line = df.median(axis=1)
    up_boundary = df.median(axis=1)+df.std(axis=1)
    down_boundary = df.median(axis=1)-df.std(axis=1)

    plt.plot(mean_line, label = "median")
    plt.plot(up_boundary, label="up boundary")
    plt.plot(down_boundary, label="down boundary")

    plt.axis([0, 300, -256, 100])
    plt.title("Figure 3: Experiment 1 - simulate 1000 episodes")
    plt.xlabel("Number of spins")
    plt.ylabel("Total winnings")
    plt.legend()

    plt.savefig("Figure3.png")
    plt.clf()

def strategy_simulate_with_limited_bankroll():
    # init an array with shape (1001) and value 80
    win_prob = 0.5 # the prob of black
    result_array = np.full((1001), 0)
    episode_winnings = 0
    spin_cnt = 0
    while episode_winnings < 80 and episode_winnings > -256 and spin_cnt < 1000:
        won = False
        bet_amount = 1

        while not won:
            won = get_spin_result(win_prob)
            if won:
                episode_winnings += bet_amount
            else:
                episode_winnings -= bet_amount
                bet_amount = min( 2 * bet_amount, episode_winnings + 256)

            spin_cnt += 1
            result_array[spin_cnt] = episode_winnings
            # print("At spin {}: bet amount it {}, the winning amount is {}".format(spin_cnt, bet_amount, episode_winnings))
            if spin_cnt == 1000:
                break
    result_array[spin_cnt:] = episode_winnings
    return result_array

def experiment2_fig4():
    res = []
    for i in range(1000):
        episode_result = strategy_simulate_with_limited_bankroll()
        res.append(episode_result)

    df = pd.DataFrame(res).T
    mean_line = df.mean(axis=1)
    up_boundary = df.mean(axis=1)+df.std(axis=1)
    down_boundary = df.mean(axis=1)-df.std(axis=1)

    plt.plot(mean_line, label = "mean")
    plt.plot(up_boundary, label="up boundary")
    plt.plot(down_boundary, label="down boundary")

    plt.axis([0, 300, -256, 100])
    plt.title("Figure 4: Experiment 2 - simulate 1000 episodes")
    plt.xlabel("Number of spins")
    plt.ylabel("Total winnings")
    plt.legend()

    plt.savefig("Figure4.png")
    plt.clf()

def experiment2_fig5():
    res = []
    for i in range(1000):
        episode_result = strategy_simulate_with_limited_bankroll()
        res.append(episode_result)

    df = pd.DataFrame(res).T
    mean_line = df.median(axis=1)
    up_boundary = df.median(axis=1)+df.std(axis=1)
    down_boundary = df.median(axis=1)-df.std(axis=1)

    plt.plot(mean_line, label = "median")
    plt.plot(up_boundary, label="up boundary")
    plt.plot(down_boundary, label="down boundary")

    plt.axis([0, 300, -256, 100])
    plt.title("Figure 5: Experiment 2 - simulate 1000 episodes")
    plt.xlabel("Number of spins")
    plt.ylabel("Total winnings")
    plt.legend()

    plt.savefig("Figure5.png")
    plt.clf()

def question_experiments():
    # question 1
    sum1 = 0
    for i in range(1000):
        sum1 += (strategy_simulate()[-1] == 80)
    prob1 = sum1 / 1000
    print("Q1: The estimated probability of winning $80 within 1000 sequential bets is {}".format(prob1))

    #question 4
    sum2 = 0
    for i in range(1000):
        sum2 += (strategy_simulate_with_limited_bankroll()[-1] == 80)
    prob2 = sum2 / 1000
    print("Q4: The estimated probability of winning $80 within 1000 sequential bets is {}".format(prob2))

    #question 5
    sum5 = 0
    for i in range(1000):
        winning = strategy_simulate_with_limited_bankroll()[-1]
        sum5 += winning
    res5 = sum5 / 1000
    print("Q5: The estimated expected value of winnings after 1000 sequential bets is {}".format(res5))


def plot_df(df):
    plt.plot(df)
    plt.show()
    plt.clf()

def test_code():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    Method to test your code  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    win_prob = 0.60  # set appropriately to the probability of a win  		  	   		  		 			  		 			     			  	 
    np.random.seed(gtid())  # do this only once  		  	   		  		 			  		 			     			  	 
    # add your code here to implement the experiments

    experiment1_fig1()
    experiment1_fig2()
    experiment1_fig3()
    experiment2_fig4()
    experiment2_fig5()

    question_experiments()

    #res = []
    #for i in range(100):
    #    res.append(strategy_simulate_with_limited_bankroll())
    #df = pd.DataFrame(res).T
    #plot_df(df)

if __name__ == "__main__":
    test_code()

