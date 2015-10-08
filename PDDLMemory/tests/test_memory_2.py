# A test for the memory module

from pddlmemory.memory.main import Memory
from pddlmemory.memory.placenode import PlaceNode

from pddlmemory.memory.item import Item
from pddlmemory.memory.fact import Fact
from pddlmemory.memory.goal import Goal


# todo: Pass Facts or Goals to memory, create Items in memory.

def load_facts_in_node(PDDL, node):
    # split to facts
    facts = []
    for l in PDDL.split("\n"):
        f = Fact(l)
        facts.append(f)

    for f in facts:
        node.addFact(f)

def load_goals_in_node(goals, node):
    for g in goals:
        node.addGoal(g)

def retreive_active_items(memory):
    for item in memory.retreiveActiveItems():
        node = item.getObject()
        print "Dumping Facts"
        print node.dumpFactsToPDDL()
        print "Dumping Goals"
        print node.dumpGoalsToPDDL()

# Creating Node 1
node_1 = PlaceNode("Node 1")
pddl_1 = """(is-at desk chair)
(is-at desk small_chair)
(is-at bed laundry1)
(is-at bedroom_cabinet laundry2)
(is-at bedroom_cabinet laundry3)
(is-at bedroom_lamp lightbulb8)
(is-at bedside_lamp lightbulb9)
(is-attached lightbulb8)
(is-attached lightbulb9)
(is-intact lightbulb8)
(is-intact lightbulb9)"""
goals_1 = [
    Goal("Cup-At-Plot", [
        Fact("(is-at plot cup)")
    ])
]
load_facts_in_node(pddl_1, node_1)
load_goals_in_node(goals_1, node_1)

# Creating Node 2
node_2 = PlaceNode("Node 2")
pddl_2 = """(is-in corridor shoe_cabinet)
(is-in corridor coat_stand)
(is-in corridor co_lamp)
(is-in corridor co_lightswitch)
(is-in corridor co_garbage)
(is-in corridor co_floor)
(is-in corridor pass_ki_co)
(is-in corridor door_be_co)
(is-in corridor door_li_co)
(is-in corridor door_cl_co)
(is-in corridor door_ba_co)
(is-in corridor door_wc_co)
(is-in corridor door_out)"""
goals_2 = [
    Goal("shoe-ordering", [
        Fact("(is-at shoe_cabinet shoepair1)"),
        Fact("(is-at shoe_cabinet shoepair2)"),
        Fact("(is-at shoe_cabinet shoepair3)"),
    ])
]
load_facts_in_node(pddl_2, node_2)
load_goals_in_node(goals_2, node_2)

memory = Memory()
memory.addNode(node_1)
memory.addNode(node_2)

# Return the active facts
retreive_active_items(memory)

print "---"
print "Deleting fact... + Adding fact...",
node_1.delFact(Fact("(is-attached lightbulb8)"))
node_1.addFact(Fact("(not (is-attached lightbulb8))"))

# Return the active facts
retreive_active_items(memory)


if __name__ == '__main__':
    pass
    # load_facts_in_node(pddl_1, node_1)
    # load_goals_in_node(goals_1, node_1)
    # print(node_1)
    # print("Printing facts:")
    # print(node_1.facts)
    # print("Printing goals:")
    # print(node_1.goals)

    # # deleting a node
    # node_1.delFact(Fact("(is-at bedroom_cabinet laundry3)"))
    # print("Printing facts:")
    # print(node_1.facts)
