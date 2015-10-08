# ce.py
#
# This PDDLMemory Central Executive module which controls
# the memory processes in PDDLMemory. Main function is
# the activation and deactivation of items and the
# controlled execution of the external planner (FF).
#
# Created: 09/09/2014
# Author: Ivo Chichkov

# config
from config import current_domain_path
from config import current_domain_name
from config import output_path
from config import maximum_iterations
from config import strengthening_factor

# modules
from memory.fact import Fact
from memory.goal import Goal
from memory.placenode import PlaceNode
from planner import Planner

# lib
from random import choice

###
# NOTES
#
# reusable code:
#   * filter all elements from a list using a lambda operator
#
# to do:
#   * done
#
###


class PDDLMemoryCE():

    def __init__(self, memory):
        """
        Init the PDDLMemory Central Executive.

        @param  Memory   A reference to the PDDLMemory
                         instance to be controlled
        """
        self.memory = memory

    def runPlannerOnce(self):
        """
        This method runs the planner once with the currently
        active PlaceNodes (active facts and goals).
        """

        # write active nodes to output folder
        active_facts_pdkb = output_path + "active_facts.pdkb"
        active_goals_pdkb = output_path + "active_goals.pdkb"

        # todo: add filtering
        factsPDDL = ""
        goalsPDDL = ""
        for i in self.memory.retreiveActiveItems():
            node = i.getObject()
            factsPDDL += node.dumpFactsToPDDL()
            goalsPDDL += node.dumpGoalsToPDDL()

        # write the facts PDKB file
        active_facts_file = open(active_facts_pdkb, 'w')
        for l in factsPDDL.split("\n"):
            active_facts_file.write(l + "\n")
        active_facts_file.close()

        # write the goals PDKB file
        active_goals_file = open(active_goals_pdkb, 'w')
        for l in goalsPDDL.split("\n"):
            active_goals_file.write(l + "\n")
        active_goals_file.close()

        # insert the PDKB files into the PDDL templates
        # todo: set the domain id as an option
        domain_template = current_domain_path + "domain-template.pddl"
        problem_template = current_domain_path + "problem-template.pddl"

        # run the planner
        p = Planner.run(current_domain_name, domain_template, problem_template,
                        [active_facts_pdkb],
                        [active_goals_pdkb])

        return p

    def progressiveActivation(self, goalRemoval=False):
        """
        This method loads PlaceNodes into memory sequentially and
        runs the planner everytime the set of active nodes is
        expanded.

        If the goalRemoval Parameter is activated, every solved
        goal is removed from its corresponding active PlaceNode.

        The effectiveness of Progressive Activation is higly dependent
        on the number of items that can be activated simultaneously.
        (see config file, activation_limit)

        @param   goalRemoval     Defines wether solved goals are removed
                                from active PlaceNodes
        """
        # get all items
        items = self.memory.retreiveItems(filter=PlaceNode)
        # deactivate all
        for i in items:
            self.memory.deactivateItem(str(i))

        items = self.memory.retreiveItems(filter=PlaceNode)
        # activate progressively
        for i in items:
            self.memory.activateItem(str(i))
            p = self.runPlannerOnce()

            # Goal removal on successful planning,
            # so that solved goals don't have to be solved again
            if goalRemoval and p.is_solution():
                self.memory.removeActiveGoals()

            yield p

    def directedRehearsal(self, max_iterations=maximum_iterations):
        """
        Items in memory compete for being activated. Inhibition
        is the process by which the activation of particular items
        is being suppressed, because other items are activated more strongly.

        In this strategy every item is activated with a certain probability.
        For stronger competitors the probability for being activated is high.
        For weaker competitors the probability for being activated is low.
        Increasing the activation probability of strong competitors leads to a
        decreased  probability for weak competitors (inhibition).

        Directed rehearsal determines which competitors are strong based
        on their relevance for successful planning. An item is a strong
        competitor when it represents a node with unsolved goals.
        (see Thesis) Then its probability for being selected is increased.
        (i.e. it is rehearsed more often).

        @param   max_iterations     The number of maximum iterations. (config)

        @return                     A tuple with
                                        * the parsed planner output
                                        * the number of solved goals during
                                          the last iteration
                                        * the number of total goals

        """

        nr_of_items = self.memory.countPlaceNodes()
        nr_of_goals = 0
        # count all goals
        for i in self.memory.retreiveItems(filter=PlaceNode):
            node = i.getObject()
            for g in node.goals.values():
                nr_of_goals += 1

        # main iteration
        solved_goals = 0
        nr_of_iterations = 0
        while solved_goals < nr_of_goals:
            if(nr_of_iterations >= max_iterations):
                break
            # select relevant items
            relevance_list = []
            items = self.memory.retreiveItems(filter=PlaceNode)
            for i in items:
                node = i.getObject()
                # do not include protected items in the relevance list
                if self.memory.isProtected(str(i)):
                    continue
                # if the item has usolved goals, use the strengthening_factor
                # to increase the probability of selection
                if node.hasUnsolvedGoals():
                    relevance_list += [str(node)] * strengthening_factor
                else:
                    relevance_list += [str(node)]

                # initially, make sure that item ar deactivated
                self.memory.deactivateItem(str(i))
            # activate the items according to their relevance
            activated_items = len(self.memory.active_item_ids)
            while not self.memory.activationLimitReached():
                if activated_items >= nr_of_items:
                    break
                # select an item and activate it, if not already activated
                selected = choice(relevance_list)
                if not self.memory.isActive(selected):
                    self.memory.activateItem(selected)
                    # remove all ocurrences of the selected item from the relevance list
                    relevance_list = filter(lambda delitem: delitem != selected, relevance_list)
                    activated_items += 1
            # run the planner
            p = self.runPlannerOnce()
            # Goal removal on successful planning,
            # so that solved goals don't have to be solved again
            g_count = 0
            if p.is_solution():
                g_count = self.memory.removeActiveGoals()
                solved_goals += g_count
            nr_of_iterations += 1
            # return (plan, solved goals, total goals)
            yield (p, solved_goals, nr_of_goals)