# pdkb_parser.py
#
# Classes for parsing PDKB files to Fact and Goal objects and
# writing Fact and Goal objects to PDKB files.
#
# Created: 07/29/2014
# Author: Ivo Chichkov

# config
from config import output_path

# lib
import itertools

# modules
from external.parser import parse_nested_list
from external.parser import ParseError
from pddlmemory.memory.fact import Fact
from pddlmemory.memory.goal import Goal

###
# NOTES
#
# reusable code:
#   * itertools.chain: Treat several sequences of iterators/lists as a chain
#
# to do:
#   * done
#
###

class PDKBParser:
    """
    Read a PDKB file into Fact and Goal classes
    """

    @classmethod
    def parse(self, facts_pdkb, goals_pdkb):
        """
        The parse method parses facts and goals pdkb files to
        two lists of Facts and Goals objects.

        @param  facts_pdkb  A list of pdkb files containing facts, negative facts are allowed.

        @param  goals_pdkb  A list of pdkb files containing goals, negative goals are allowed.

        @return             A tuple with a Facts list and a Goals list.

        """
        # parse facts
        parsed_facts = []
        for fact_file in facts_pdkb:

            try:
                f = open(fact_file, "r")
                # chain an iterator with a static list, extremely useful
                parsed_fact_list = parse_nested_list(
                    itertools.chain(["("], f, [")"]))
            except IOError as e:
                raise SystemExit(
                    "Error: Could not read file: %s\nReason: %s." %
                    (e.filename, e))
            except ParseError as e:
                raise SystemExit(
                    "ParseErrorr: Could not parse %s file: %s\n" %
                    (type, fact_file))
            parsed_facts.extend(parsed_fact_list)

        # parse goals
        parsed_goals = []
        for goal_file in goals_pdkb:
            try:
                f = open(goal_file, "r")
                parsed_goal_list = parse_nested_list(
                    itertools.chain(["("], f, [")"]))
            except IOError as e:
                raise SystemExit(
                    "Error: Could not read file: %s\nReason: %s." %
                    (e.filename, e))
            except ParseError as e:
                raise SystemExit(
                    "Error: Could not parse %s file: %s\n" %
                    (type, goal_file))

            # extract goal name from filename
            lim = goal_file.rfind("/")+1 if goal_file.rfind("/") > 0 else 0
            goalname = goal_file[lim:-5]
            parsed_goals.append([goalname, parsed_goal_list])

        # generate the Facts objects
        facts = []
        for f in parsed_facts:
            # don't include negative facts
            if f[0] == "not":
                continue
            # create fact objects
            else:
                fact = Fact(f[0], *f[1:])
                facts.append(fact)

        # generate the Goals objects
        goals = []
        for g in parsed_goals:
            goal_name = g[0]
            subgoals = []

            # extracting the subgoals
            for f in g[1]:
                negative = False
                # negative subgoals are allowed
                if f[0] == "not":
                    negative = True
                    f = f[1]
                # generate subgoal (encoded as fact object)
                fact = Fact(f[0], *f[1:])
                if negative:
                    fact.setNegative()
                subgoals.append(fact)

            # finally, generate the goal object
            goal = Goal(goal_name, subgoals)
            goals.append(goal)

        return (facts, goals)

class PDKBWriter:
    """
    Write a set of Fact and Goal classes to a PDKB file
    """
