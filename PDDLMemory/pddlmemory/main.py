# main.py
#
# This is the main class of the PDDLMemory lib. It is
# derived from the Memory class (memory/main.py) which
# contains the fundamental memory functionality.
#
# The PDDLMemory lib provides a memory module that operates
# with PDDL entities such as Goals and Facts (basic entities)
# and PlaceNodes (complex entities) that represent clusters of
# basic nodes associated with a specific location.
#
# Created: 08/09/2014
# Author: Ivo Chichkov

# config
from pddlmemory.config import current_domain_path
from pddlmemory.config import current_domain_node_ids

# modules
from memory.main import Memory
from pddlmemory.memory.placenode import PlaceNode
from pddlmemory.pdkb_parser import PDKBParser

# lib
import os
import os.path

###
# NOTES
#
# reusable code:
#   * obtain a list of all files in a folder (loadNode)
#
# to do:
#   * done
#
###


class PDDLMemory(Memory):

    def __init__(self):
        """ Init PDDLMemory """
        super(PDDLMemory, self).__init__()

    def loadNode(self, node_files_path, node):
        """ Load PDKB files into PlaceNode """

        node_facts_path = node_files_path + "facts/"
        node_goals_path = node_files_path + "goals/"

        # Retreive the fact and goals files
        # print (node_facts_path)
        facts_pdkb = [(node_facts_path + f)
                      for f in os.listdir(node_facts_path)
                      if os.path.isfile(node_facts_path + f)
                      and (node_facts_path + f).endswith(".pdkb")]
        # print (node_goals_path)
        goals_pdkb = [(node_goals_path + f)
                      for f in os.listdir(node_goals_path)
                      if os.path.isfile(node_goals_path + f)
                      and (node_facts_path + f).endswith(".pdkb")]

        # Parse the files
        (parsed_facts, parsed_goals) = PDKBParser.parse(facts_pdkb, goals_pdkb)

        # Add facts and goals to node
        for f in parsed_facts:
            node.addFact(f)
        for g in parsed_goals:
            node.addGoal(g)

    def loadDomain(self):
        """
        Load the structured domain representation into memory.
        """

        nodes = []
        for nid in current_domain_node_ids:
            node = PlaceNode(nid)
            nodes.append(node)
            node_files_path = current_domain_path + nid + "/"
            self.loadNode(node_files_path, node)

        for n in nodes:
            self.addNode(n)
            # protect the base node
            if str(n) == "PlaceNode<base>":
                self.items[str(n)].keep_active = True

            # protect the corridor node
            # if str(n) == "PlaceNode<corridor>":
            #     self.items[str(n)].keep_active = True

    def removeActiveGoals(self):
        """
        Remove all goals from the currently active nodes.

        @return     the number of removed goals.
        """
        g_count = 0
        for item_id in self.items:
            if self.items[item_id].activation > 0:
                obj = self.items[item_id].getObject()
                if isinstance(obj, PlaceNode):
                    node = obj
                    for g in node.goals.values():
                        node.delGoal(g.getName())
                        g_count += 1
        return g_count

    def countPlaceNodes(self):
        """
        Return the number of total PlaceNodes in memory.
        """
        counter = 0
        items = self.retreiveItems(filter=PlaceNode)
        for i in items:
            counter += 1
        return counter
