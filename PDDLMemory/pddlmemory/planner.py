# planner.py
#
# The Planner class launches the default planner
# with the knowledge files (.pdkb) provided.
#
# Created: 06/22/2014
# Author: Ivo Chichkov

# modules
from launcher import Launcher
from parser import Parser
from pddl_utils import compile_PDKB_to_PDDL

# config
from config import print_planner_output

###
# NOTES
#
# reusable code:
#
# to do:
#   * done
#
###


class Planner():

    @classmethod
    def run(self, problem_id, domain_template, problem_template,
                 facts_pdkb, goals_pdkb):

        """
        Execute the planner and return the parsed output.
        Before the planner is executed the pddl problem file is created
        dynamically by inserting the knowledge base (kb_files) and the current
        goals (goal_files) at the right location in the problem template.

        @param problem_id           The id for the particular
                                    problem/domain set

        @param domain_template      The path of the pddl domain template

        @param problem_template     The name of the pddl problem template that
                                    contains special insertion marks

        @param facts_pdkb           The fact files to be inserted in
                                    the pddl problem file

        @param goals_pdkb           The goal files to be inserted in the pddl
                                    problem file

        """

        # insert the PDKB files into the PDDL templates
        (domain_file, problem_file) = compile_PDKB_to_PDDL(
            problem_id, domain_template, problem_template,
            facts_pdkb, goals_pdkb)

        # launch the planner and redirect output to parser
        l = Launcher(domain_file, problem_file)
        l.launch()
        p = Parser(l.get_output())

        if print_planner_output:
            print l.get_output()

        # return the parsed plan
        return p
