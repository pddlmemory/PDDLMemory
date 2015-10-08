# parser.py
#
# The parser for the planner's output (used planner: FF)
#
# Created: 04/15/2014
# Author: Ivo Chichkov

###
# NOTES
#
# reusable code:
#   * parse program output
#
###


class Parser:

    def __init__(self, unparsed_output):
        self.txt = unparsed_output

    def get_steps(self):
        """
        Get an array with the steps of the plan represented as strings.

        @return     An array with planning steps.
        """

        lines = self.txt.split("\n")
        steps = []
        addsteps = False
        for l in lines:
            words = l.split()
            if addsteps:
                if len(words):
                    if words[0] == "time":
                        addsteps = False
                        break
                    else:
                        steps.append([words[1], " ".join(words[2:])])
            if len(words) and words[0] == "step":
                # plan has been found

                # check for empty plan (goals already fulfiled, 0 steps)
                if len(words) < 2:
                    return steps

                # otherwise start collecting steps
                addsteps = True
                steps.append([words[2], " ".join(words[3:])])

        return steps

    def get_info(self):
        """
        Get information about the time needed to generate the plan and the
        size of the state space.

        @return     Dictionary that contains the information provided by the
                    planner.
        """

        lines = self.txt.split("\n")
        timerows = []

        # there are 6 rows with information about the time in the output
        # count the number of rows already parsed
        timescounter = 0

        for l in lines:
            words = l.split()
            if timescounter:
                if timescounter > 6:
                    break
                else:
                    timerows.append(l)
                    timescounter += 1
            if len(words) and words[0] == "time":
                timescounter = 1
                timerows.append(l)

        if not timescounter:
            return {"easy_templates": 0,
                    "hard_templates": 0,
                    "problemspace_size": 0,
                    "total_time": 0
                    }
        else:

            easy_templates = timerows[0].split()[5]
            hard_templates = timerows[0].split()[7]
            problemspace_size = timerows[4].split()[4]
            total_time = timerows[5].split()[0]

            return {"easy_templates": int(easy_templates),
                    "hard_templates": int(hard_templates),
                    "problemspace_size": int(problemspace_size),
                    "total_time": float(total_time)
                    }

    def is_solution(self):
        """ Returns True if a solution for the problem has been found. """
        lines = self.txt.split("\n")
        for l in lines:
            words = l.split()
            if len(words):
                if words[0] == "ff:":
                    message = " ".join(words[1:])
                    # a regular plan has been found
                    if message.find("found legal plan") != -1:
                        return True
                    # the empty plan solves the problem (goals already solved)
                    if message.find("goal can be simplified to TRUE") != -1:
                        return True
        return False

    def is_empty(self):
        """ Returns True if the plan is an empty plan. """
        lines = self.txt.split("\n")
        for l in lines:
            words = l.split()
            if len(words):
                if words[0] == "ff:":
                    message = " ".join(words[1:])
                    # The plan is an empty plan
                    if message.find("goal can be simplified to TRUE") != -1:
                        return True
        return False
