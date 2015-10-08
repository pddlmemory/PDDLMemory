# visualizer.py
#
# The visualizer is used to plot the results (plan lenght, execution time)
# that were collected by the parser.
#
# Created: 04/23/2014
# Author: Ivo Chichkov

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

###
# NOTES
#
# reusable code:
#   * generate a plot
#   * restrict axis values to integers (discrete scale)
#
# to do:
#   * done
#
###

class Visualizer():

    def __init__(self):
        pass

    def plot_plan_lengths(self, plan_array, labels,
        title="Plan lengths with different memory sets"):
        """
        Plot the number of steps for every plan given in the plan_array.
        Finally, display the plot.

        @param plan_array   Array of plans represented as parser objects
        @param labels       Array of labels for the the individual bars
        """

        errormsg = "Visualizer: plan array and labels array differ in length."
        assert len(plan_array) == len(labels), errormsg

        # generate the plot
        plan_lengths = np.array([len(p.get_steps()) for p in plan_array])
        plt.title(title)
        plt.xlabel('Memory Set')
        plt.ylabel('Plan length')
        plt.axis([-0.5, len(plan_lengths)*0.9, 0, max(plan_lengths)+1])

        # set y axis to integer
        ya = plt.gca().get_yaxis()
        ya.set_major_locator(MaxNLocator(integer=True))

        # set x ticks
        index = np.arange(len(labels))
        width = 0.25
        plt.xticks(index+width/2., labels)

        # show plot
        plt.bar(index, plan_lengths, width, color='b')
        plt.show()

    def plot_plan_times(self, plan_array, labels,
        title="Plan lengths with different memory sets"):
        """
        Plot the number of steps and the generation times for every plan
        given in the plan_array. Finally, display the plot.

        @param plan_array   Array of plans represented as parser objects
        @param labels       Array of labels for the the individual bars

        """

        errormsg = "Visualizer: plan array and labels array differ in length."
        assert len(plan_array) == len(labels), errormsg

        plan_lengths = np.array([len(p.get_steps()) for p in plan_array])
        plan_times = np.array([p.get_info()["total_time"] for p in plan_array])

        index = np.arange(len(labels))

        # create axes (left and right y-axis)
        fig, ax1 = plt.subplots()
        # ax2 = ax1.twinx()

        # set format of left y-axis to integer
        # ya = ax1.get_yaxis()
        # ya.set_major_locator(MaxNLocator(integer=True))

        # generate the bars
        width = 0.25
        # ax1.bar(index, plan_lengths, width, color='b')
        ax1.bar(index+width, plan_times, width, color='r')

        # generate text
        ax1.set_title(title)
        ax1.set_xlabel('Planning tasks')
        # ax1.set_ylabel('Plan length (steps)')
        ax1.set_ylabel('Plan generation time (s)')
        ax1.set_xticks(index+width)
        ax1.set_xticklabels(labels)

        # show plot
        # ax1.axis([-0.2, len(plan_lengths), 0, max(plan_lengths)+1])
        ax1.axis([-0.2, len(plan_lengths), 0, max(plan_times)+1.0])
        plt.show()

    def plot_plan_lt(self, plan_array, labels,
        title="Plan lengths with different memory sets"):
        """
        Plot the number of steps and the generation times for every plan
        given in the plan_array. Finally, display the plot.

        @param plan_array   Array of plans represented as parser objects
        @param labels       Array of labels for the the individual bars

        """

        errormsg = "Visualizer: plan array and labels array differ in length."
        assert len(plan_array) == len(labels), errormsg

        plan_lengths = np.array([len(p.get_steps()) for p in plan_array])
        plan_times = np.array([p.get_info()["total_time"] for p in plan_array])


        index = np.arange(len(labels))

        # create axes (left and right y-axis)
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        # set format of left y-axis to integer
        ya = ax1.get_yaxis()
        ya.set_major_locator(MaxNLocator(integer=True))

        # generate the bars
        width = 0.25
        ax1.bar(index, plan_lengths, width, color='b')
        ax2.bar(index+width, plan_times, width, color='r')

        # generate text
        ax1.set_title(title)
        ax1.set_xlabel('Planning tasks')
        ax1.set_ylabel('Plan length (steps)')
        ax2.set_ylabel('Plan generation time (s)')
        ax1.set_xticks(index+width)
        ax1.set_xticklabels(labels)

        # show plot
        ax1.axis([-0.2, len(plan_lengths), 0, max(plan_lengths)+1])
        ax2.axis([-0.2, len(plan_lengths), 0, max(plan_times)+0.5])
        plt.show()

    def plot_plan_lt_avg(self, plan_groups, labels,
        title="Plan lengths with different memory sets"):
        """
        Plot the avarage of number of steps and the generation times
        for every plan in each plan group.

        given in the plan_array. Finally, display the plot.

        @param plan_groups  Array of Arrays containing planning lengths/imes
                            e.g. p1 = [plan_length, plan_time]
                            plan_groups = [[p1,p2,p3], [p4,p5,p6]]
                            represented as parser objects.
        @param labels       Array of labels for the the individual bars

        """

        errormsg = "Visualizer: plan_groups array is empty."
        assert len(plan_groups) > 0, errormsg

        errormsg = "Visualizer: plan_groups array and labels array differ in length."
        assert len(plan_groups) == len(labels), errormsg

        # check if list with success of planning iterations is provided
        # plan_success = True if (len(plan_groups[0])==3) else False

        # iterate over the plan groups
        time_stats = []
        plan_stats = []
        succ_stats = []
        for pg in plan_groups:
            plan_lengths = np.array([p[0] for p in pg])
            plan_times = np.array([p[1] for p in pg])
            success = np.array([p[2] for p in pg])
            print "plan_lengths:",plan_lengths
            print "plan_times:",plan_times

            # calculate the averages, SD, and SE
            plan_lengths_avg = np.mean(plan_lengths)
            plan_lenghts_SD = np.std(plan_lengths)
            plan_lengths_SE = plan_lenghts_SD / np.sqrt(len(plan_lengths))

            plan_times_avg = np.mean(plan_times)
            plan_times_SD = np.std(plan_times)
            plan_times_SE = plan_times_SD / np.sqrt(len(plan_times))

            success_avg = np.mean(success)

            # append to array with lenght statistics (plan_stasts)
            # and time statistics (time_stats)
            plan_stats.append([plan_lengths_avg, plan_lengths_SE])
            time_stats.append([plan_times_avg, plan_times_SE])
            succ_stats.append(success_avg)

        plan_stats = np.array(plan_stats)
        time_stats = np.array(time_stats)
        succ_stats = np.array(succ_stats)

        index = np.arange(len(labels))

        # create axes (left and right y-axis)
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        # set format of left y-axis to integer
        ya = ax1.get_yaxis()
        ya.set_major_locator(MaxNLocator(integer=True))

        # generate the bars
        width = 0.25
        length_bars = ax1.bar(index, plan_stats[...,0], width, color='b', yerr=plan_stats[...,1])
        time_bars = ax2.bar(index+width, time_stats[...,0], width, color='r', yerr=time_stats[...,1])
        success_bars  = ax2.bar(index+(2*width), succ_stats, width, color='0.75')

        # generate text
        ax1.set_title(title)
        ax1.set_xlabel('Planning tasks')
        ax1.set_ylabel('Plan length (steps)')
        ax2.set_ylabel('Plan generation time (s)')
        ax1.set_xticks(index+width)
        ax1.set_xticklabels(labels)

        # show plot
        ax1.axis([-0.2, len(plan_stats), 0, max(plan_stats[...,0])+5])
        ax2.axis([-0.2, len(time_stats), 0, max(time_stats[...,0])+5])
        plt.show()


    def compare_plan_times(self, plan_groups1, plan_groups2, labels, legend,
        title="Plan times comparision"):

        errormsg = "Visualizer: plan_groups array is empty."
        assert len(plan_groups1) > 0, errormsg
        assert len(plan_groups2) > 0, errormsg

        errormsg = "Visualizer: plan_groups array and labels array differ in length."
        assert len(plan_groups1) == len(labels), errormsg
        assert len(plan_groups2) == len(labels), errormsg

        # iterate over the plan groups
        time_stats1 = []
        time_stats2 = []
        for pg in plan_groups1:
            plan_times1 = np.array([p[1] for p in pg])

            plan_times1_avg = np.mean(plan_times1)
            plan_times1_SD = np.std(plan_times1)
            plan_times1_SE = plan_times1_SD / np.sqrt(len(plan_times1))

            # and time statistics (time_stats)
            time_stats1.append([plan_times1_avg, plan_times1_SE])

        for pg in plan_groups2:
            plan_times2 = np.array([p[1] for p in pg])

            plan_times2_avg = np.mean(plan_times2)
            plan_times2_SD = np.std(plan_times2)
            plan_times2_SE = plan_times2_SD / np.sqrt(len(plan_times2))

            # and time statistics (time_stats)
            time_stats2.append([plan_times2_avg, plan_times2_SE])

        time_stats1 = np.array(time_stats1)
        time_stats2 = np.array(time_stats2)

        index = np.arange(len(labels))

        # create axes (left and right y-axis)
        fig, ax1 = plt.subplots()

        # set format of left y-axis to integer
        ya = ax1.get_yaxis()
        ya.set_major_locator(MaxNLocator(integer=True))

        # generate the bars
        width = 0.25
        time1_bars = ax1.bar(index, time_stats1[...,0], width, yerr=time_stats1[...,1], color="#7a68a6") # color="#9b9b9b" )
        time2_bars = ax1.bar(index+width, time_stats2[...,0], width, yerr=time_stats2[...,1], color="#3485FF" ) # color="#a9cbfd"

        # generate text
        # ax1.set_title(title)
        ax1.set_xlabel('Planning tasks')
        ax1.set_ylabel('Plan generation time (s)')
        ax1.set_xticks(index+width)
        ax1.set_xticklabels(labels)

        # generate legend
        ax1.legend( ( time1_bars[0],  time2_bars[0],), (legend[0], legend[1]), loc="left" )

        # show plot
        plt_height = max(max(time_stats1[...,0]), max(time_stats2[...,0]))+5
        ax1.axis([-0.2, len(time_stats1), 0, plt_height])
        plt.show()

    def compare_plan_lengths(self, plan_groups1, plan_groups2, labels, legend,
        title="Plan lengths comparision"):

        errormsg = "Visualizer: plan_groups array is empty."
        assert len(plan_groups1) > 0, errormsg
        assert len(plan_groups2) > 0, errormsg

        errormsg = "Visualizer: plan_groups array and labels array differ in length."
        assert len(plan_groups1) == len(labels), errormsg
        assert len(plan_groups2) == len(labels), errormsg

        # check if list with success of planning iterations is provided
        # plan_success = True if (len(plan_groups[0])==3) else False

        print "plan_groups1 ", plan_groups1
        print "plan_groups2 ", plan_groups2
        # iterate over the plan groups
        plan_stats1 = []
        succ_stats1 = []
        plan_stats2 = []
        succ_stats2 = []

        for pg in plan_groups1:
            plan_lengths1 = np.array([p[0] for p in pg])
            success1 = np.array([p[2] for p in pg])

            # calculate the averages, SD, and SE
            plan_lengths1_avg = np.mean(plan_lengths1)
            plan_lenghts1_SD = np.std(plan_lengths1)
            plan_lengths1_SE = plan_lenghts1_SD / np.sqrt(len(plan_lengths1))

            success1_count = np.count_nonzero(success1)
            success1_total = len(success1)

            # append to array with lenght statistics (plan_stasts)
            # and time statistics (time_stats)
            plan_stats1.append([plan_lengths1_avg, plan_lengths1_SE])
            succ_stats1.append([success1_count, success1_total])

        for pg in plan_groups2:
            plan_lengths2 = np.array([p[0] for p in pg])
            success2 = np.array([p[2] for p in pg])

            # calculate the averages, SD, and SE
            plan_lengths2_avg = np.mean(plan_lengths2)
            plan_lenghts2_SD = np.std(plan_lengths2)
            plan_lengths2_SE = plan_lenghts2_SD / np.sqrt(len(plan_lengths2))

            success2_count = np.count_nonzero(success2)
            success2_total = len(success2)

            # append to array with lenght statistics (plan_stasts)
            # and time statistics (time_stats)
            plan_stats2.append([plan_lengths2_avg, plan_lengths2_SE])
            succ_stats2.append([success2_count, success2_total])

        plan_stats1 = np.array(plan_stats1)
        succ_stats1 = np.array(succ_stats1)
        plan_stats2 = np.array(plan_stats2)
        succ_stats2 = np.array(succ_stats2)

        index = np.arange(len(labels))

        # create axes (left and right y-axis)
        fig, ax1 = plt.subplots()

        # set format of left y-axis to integer
        ya = ax1.get_yaxis()
        ya.set_major_locator(MaxNLocator(integer=True))

        # generate the bars
        width = 0.25
        length1_bars = ax1.bar(index, plan_stats1[...,0], width, yerr=plan_stats1[...,1], color="#7a68a6") # color="#9b9b9b")
        length2_bars = ax1.bar(index+width, plan_stats2[...,0], width, yerr=plan_stats2[...,1], color="#3485FF")

        # generate text
        # ax1.set_title(title)
        ax1.set_xlabel('Planning tasks')
        ax1.set_ylabel('Plan length (steps)')
        ax1.set_xticks(index+width)
        ax1.set_xticklabels(labels)

        # show plot
        plt_height =  max(max(plan_stats1[...,0]),max(plan_stats2[...,0]))+5
        ax1.axis([-0.2, len(plan_stats1), 0, plt_height])

        # generate legend
        ax1.legend( ( length1_bars[0],  length2_bars[0],), (legend[0], legend[1]), loc="left" )

        # generate the bar labels
        nr_of_succ1 = succ_stats1[...,0]
        nr_of_succ2 = succ_stats2[...,0]
        total_runs1 = succ_stats1[...,1]
        total_runs2 = succ_stats2[...,1]

        barlabels_l1 = [str(nr_of_succ1[i])+"/"+str(total_runs1[i]) for i in range(len(total_runs1))]
        barlabels_l2 = [str(nr_of_succ2[i])+"/"+str(total_runs2[i]) for i in range(len(total_runs2))]

        self.barlabel(length1_bars, ax1, barlabels_l1)
        self.barlabel(length2_bars, ax1, barlabels_l2)

        plt.show()


    def plot_plan_lg(self, plan_array, labels, u_goals,
        title="Subsequent planning executions with # of unsolved goals"):
        """
        Plot the number of unsolved goals for every planning iteration.
        (number of iterations)

        @param plan_array       Array of plans represented as parser objects
        @param labels           Array of labels for the the individual bars
        @param u_goals          Array with number of unsolved goals for
                                every planner iteration

        """

        errormsg = "Visualizer: plan array and labels array differ in length."
        assert len(plan_array) == len(labels), errormsg

        errormsg = "Visualizer: plan array and goals array differ in length."
        assert len(plan_array) == len(u_goals), errormsg

        plan_lengths = np.array([len(p.get_steps()) for p in plan_array])
        plan_times = np.array([p.get_info()["total_time"] for p in plan_array])
        unsolved_goals = np.array(u_goals)

        index = np.arange(len(labels))
        # create axes (left and right y-axis)
        fig, ax1 = plt.subplots()
        # ax2 = ax1.twinx()

        # set format of left y-axis to integer
        ya = ax1.get_yaxis()
        ya.set_major_locator(MaxNLocator(integer=True))

        # generate the bars / plots
        width = 0.25
        # ax1.bar(index, plan_lengths, width, color='b')
        # ax2.bar(index+width, plan_times, width, color='r')
        ax1.plot(labels, unsolved_goals, 'o-')

        # generate text
        ax1.set_title(title)
        ax1.set_xlabel("Planning iterations")
        # ax1.set_ylabel("Plan length (steps)")
        ax1.set_ylabel("Number of unsolved goals")
        # ax1.set_xticks(index+width)
        # ax1.set_xticklabels(labels)

        # show plot
        # ax1.axis([-0.2, len(plan_lengths), 0, max(plan_lengths)+1])
        # ax1.axis([-0.2, len(plan_lengths), 0, max(unsolved_goals)+0.5])
        plt.show()


    def plot_plan_lgt(self, plan_array, labels, u_goals,
        title="Subsequent planning executions with # of unsolved goals"):
        """
        Plot the number of unsolved goals for every planning iteration.
        (planning times)

        @param plan_array       Array of plans represented as parser objects
        @param labels           Array of labels for the the individual bars
        @param u_goals          Array with number of unsolved goals for
                                every planner iteration

        """

        errormsg = "Visualizer: plan array and labels array differ in length."
        assert len(plan_array) == len(labels), errormsg

        errormsg = "Visualizer: plan array and goals array differ in length."
        assert len(plan_array) == len(u_goals), errormsg

        # sum up the planning times
        plan_times = []
        for i in range(len(plan_array)):
            plan_times.append(
                sum([p.get_info()["total_time"] for p in plan_array[:(i+1)]]))

        plan_times.insert(0,0.0)
        u_goals.insert(0,5)
        planning_durations = np.array(plan_times)
        unsolved_goals = np.array(u_goals)

        print "Viz, plan time: ", [p.get_info()["total_time"] for p in plan_array]
        print "Viz, planning durations:", planning_durations
        print "Viz, unsolved goals:", unsolved_goals
        index = np.arange(len(labels))

        # create axes (left and right y-axis)
        fig, ax1 = plt.subplots()
        # ax2 = ax1.twinx()

        # set format of left y-axis to integer
        ya = ax1.get_yaxis()
        ya.set_major_locator(MaxNLocator(integer=True))

        # generate the bars / plots
        # width = 0.25
        # ax1.bar(index, plan_lengths, width, color='b')
        # ax2.bar(index+width, plan_times, width, color='r')
        ax1.plot(planning_durations, unsolved_goals, 'o-')

        # generate text
        ax1.set_title(title)
        ax1.set_xlabel("Total planning time (in s)")
        # ax1.set_ylabel("Plan length (steps)")
        ax1.set_ylabel("Number of unsolved goals")
        # ax1.set_xticks(index+width)
        # ax1.set_xticklabels(labels)

        # show plot
        # ax1.axis([-0.2, len(plan_lengths), 0, max(plan_lengths)+1])
        # ax1.axis([-0.2, len(plan_lengths), 0, max(unsolved_goals)+0.5])
        plt.show()

    def plot_plan_lg(self, plan_array, labels, u_goals,
        title="Subsequent planning executions with # of unsolved goals"):
        """
        Plot the number of unsolved goals for every planning iteration.
        (number of iterations)

        @param plan_array       Array of plans represented as parser objects
        @param labels           Array of labels for the the individual bars
        @param u_goals          Array with number of unsolved goals for
                                every planner iteration

        """

        errormsg = "Visualizer: plan array and labels array differ in length."
        assert len(plan_array) == len(labels), errormsg

        errormsg = "Visualizer: plan array and goals array differ in length."
        assert len(plan_array) == len(u_goals), errormsg

        plan_lengths = np.array([len(p.get_steps()) for p in plan_array])
        plan_times = np.array([p.get_info()["total_time"] for p in plan_array])
        unsolved_goals = np.array(u_goals)

        index = np.arange(len(labels))
        # create axes (left and right y-axis)
        fig, ax1 = plt.subplots()
        # ax2 = ax1.twinx()

        # set format of left y-axis to integer
        ya = ax1.get_yaxis()
        ya.set_major_locator(MaxNLocator(integer=True))

        # generate the bars / plots
        width = 0.25
        # ax1.bar(index, plan_lengths, width, color='b')
        # ax2.bar(index+width, plan_times, width, color='r')
        ax1.plot(labels, unsolved_goals, 'o-')

        # generate text
        ax1.set_title(title)
        ax1.set_xlabel("Planning iterations")
        # ax1.set_ylabel("Plan length (steps)")
        ax1.set_ylabel("Number of unsolved goals")
        # ax1.set_xticks(index+width)
        # ax1.set_xticklabels(labels)

        # show plot
        # ax1.axis([-0.2, len(plan_lengths), 0, max(plan_lengths)+1])
        # ax1.axis([-0.2, len(plan_lengths), 0, max(unsolved_goals)+0.5])
        plt.show()


    def barlabel(self, rects, ax, labels):
        # attach some text labels

        errormsg = "Visualizer: Bar lables do not match number of bars."
        assert len(rects) == len(labels), errormsg

        i = 0
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, labels[i],
                    ha='center', va='bottom', size=8)
            i+=1

