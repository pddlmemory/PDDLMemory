# launcher.py
#
# The launcher class starts the planner with the specified
# problem and domain files. It parses the output and stores
# important details (plan length, plan generation time).
#
# Created: 04/15/2014
# Author: Ivo Chichkov

import subprocess
from config import planner_path

###
# NOTES
#
# reusable code:
#   * launch a program
#   * parse program output
#
###


class Launcher:

    def __init__(self, domain_file, problem_file):
        """
        Init the launcher

        @param domain_file  The pddl domain file
        @param problem_file The pddl problem file

        """

        self.domain_file = domain_file
        self.problem_file = problem_file
        self.output = ""

    def launch(self):
        """ Execute the launcher """

        try:
            self.output = subprocess.check_output(
                [planner_path, "-o", self.domain_file, "-f", self.problem_file]
                )

        except subprocess.CalledProcessError as e:
            self.output = e.output

    def get_output(self):
        """
        Return the planner output

        @return     The output string
        """

        return self.output
