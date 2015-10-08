# placenode.py
#
# The PlaceNode class represents a node in the place graph.
# A PlaceNode is a unit of memory that represents the knowledge
# associated with the current location.
#
# Created: 07/18/2014
# Author: Ivo Chichkov


class PlaceNode:

    def __init__(self, label):
        # set the node id
        self.nid = label

        # facts and goals contained in the node
        self.facts = {}
        self.goals = {}

    def addFact(self, fact):
        # create a hash and use it as a key
        # for the fact in the facts dictionary
        h = hash(fact.dumpPDDL())
        self.facts[h] = fact

    def delFact(self, fact):
        try:
            h = hash(fact.dumpPDDL())
            self.facts.pop(h)
        except KeyError:
            pass

    def addGoal(self, goal):
        # use the goal name as a key
        self.goals[goal.name] = goal

    def delGoal(self, goal_name):
        try:
            self.goals.pop(goal_name)
        except KeyError:
            pass

    def dumpFactsToPDDL(self):
        facts_pddl = "; " + self.nid + "\n"
        for fact_id in self.facts:
            facts_pddl += self.facts[fact_id].dumpPDDL() + "\n"
        return facts_pddl

    def dumpGoalsToPDDL(self):
        goals_pddl = ""
        for goal_id in self.goals:
            goals_pddl += self.goals[goal_id].dumpPDDL()
        return goals_pddl

    def hasUnsolvedGoals(self):
        if len(self.goals) > 0:
            return True
        else:
            return False

    def __str__(self):
        """ Return a string representation """
        return "PlaceNode<" + self.nid + ">"