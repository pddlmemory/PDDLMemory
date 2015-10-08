# pddl_utils.py
#
# Useful functions for working with PDKB and PDDL files.
#
# Created: 07/23/2014
# Author: Ivo Chichkov

# lib
import StringIO
import fileinput
import shutil
import os

# config
from config import output_path

###
# NOTES
#
# reusable code:
#   * insert lines in file (by replacing a marker string in the file
#     eg. [[MARKER]])
#   * use string as a file (StringIO)
#   * copy files with shutil
#   * functions for dealing with chunks in PDDLMemory
#
# to do:
#   * done
#
###


def compile_PDKB_to_PDDL(problem_id, domain_template, problem_template,
                         facts_pdkb, goals_pdkb):
    """
    Function to compile the PDKB files together into a PDDL domain
    and problem file.

    @param problem_id           The id for the particular problem/domain set

    @param domain_template      The path of the pddl domain template

    @param problem_template     The path of the pddl problem template
                                that contains special insertion marks
                                (goals, facts)

    @param facts_pdkb           A list of paths of fact files to be
                                inserted in the pddl problem file

    @param goals_pdkb           A list of paths of goal files to be
                                inserted in the pddl problem file

    @return                     A tuple with the paths of the newly
                                created domain and problem files.

    """

    # create the domain file
    domain_file = output_path + problem_id + "-domain.pddl"
    shutil.copyfile(domain_template, domain_file)

    # create the problem file
    problem_file = output_path + problem_id + "-problem.pddl"
    shutil.copyfile(problem_template, problem_file)
    _insert_PDKB_in_PDDL("[[KNOWLEDGE BASE]]", problem_file, facts_pdkb)
    _insert_PDKB_in_PDDL("[[GOAL BASE]]", problem_file, goals_pdkb)

    # return the paths to the domain/problem pair
    return (domain_file, problem_file)


def _insert_PDKB_in_PDDL(insertion_mark, pddl_file, pdkb_files):
        """
        Insert the knowledge base files at the right place
        (insertion_mark) in the problem file.
        """

        # create a temporary copy of the pddl file
        tempfile = pddl_file + ".tmp"
        shutil.copyfile(pddl_file, tempfile)

        # compile the pdkb files together
        complete_kb = StringIO.StringIO()
        for filename in pdkb_files:
            f = open(filename)
            for line in f:
                complete_kb.write(line)
            complete_kb.write("\n\n")
            f.close()

        f = fileinput.input(tempfile, inplace=1)
        for line in f:
            line = line.replace(insertion_mark, complete_kb.getvalue())
            print line,
        f.close()

        # write the new copy to the output file
        shutil.copyfile(tempfile, pddl_file)

        # delete the temp file
        os.remove(tempfile)
