# goal.py
#
# The goal class represents a PDDL goal.
# Goals can be comprised of one or many facts.
#
# Created: 07/11/2014
# Author: Ivo Chichkov


class Goal:

    def __init__(self, name, facts=[]):
        """
        Generates a Goal object.

        @param  name        A name (id) for the goal.
        @param  facts	    A list with facts that should be true when
                            the goal is fulfiled.
        """
        self.name = name
        self.facts = []
        for f in facts:
            self.facts.append(f)

    def dumpPDDL(self):
        """ Return the PDDL representation. """
        pddl = "; *** "+self.name+" ***\n"
        for f in self.facts:
            pddl += f.dumpPDDL() + "\n"
        return pddl

    def getName(self):
        return self.name

    def __str__(self):
        """ Return a string representation """
        return "Goal<"+self.getName()+">"
