# fact.py
#
# The fact class represents a PDDL fact.
#
# Created: 07/11/2014
# Author: Ivo Chichkov


class Fact:

    def __init__(self, predicate, *args):
        self.predicate = predicate
        self.args = args
        self.negative = False

    def dumpPDDL(self):
        """ Return the PDDL representation. """
        # Known limitation: doesn't work with functions,
        # i.e. (= (hiring-cost d4) 82)
        pddl = ("(not " if self.negative else "") + \
            "("+self.predicate
        for a in self.args:
            pddl += " "+a
        pddl += ")" + (")" if self.negative else "")
        return pddl

    def setNegative(self, neg=True):
        self.negative = neg

    def __str__(self):
        """ Return a string representation """
        return "Fact<"+self.dumpPDDL()+">"
