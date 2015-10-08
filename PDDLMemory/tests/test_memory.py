# A test for the memory module

from pddlmemory.memory.main import Memory
from pddlmemory.memory.placenode import PlaceNode

from pddlmemory.memory.item import Item
from pddlmemory.memory.fact import Fact
from pddlmemory.memory.goal import Goal

# Tests for shape
# a = Fact("(is-at table cup)")
# b = Fact("(is-at plot honey)")
# c = Fact("(is-at plot tea)")
# d = Fact("(is-at waterboiler water)")
# e = Goal("Cup-At-Plot", [Fact("(is-at plot cup)")])

def printActive(memory):
    active = memory.retreiveActiveItems()
    print "Active items: ",
    for item in active:
        print item,
    print ""

def printAll(memory):
    active = memory.retreiveItems()
    print "All items: ",
    for item in active:
        print item,
    print ""

pn = []
pn.append(PlaceNode("kitchen"))
pn.append(PlaceNode("livingroom"))
pn.append(PlaceNode("garden"))
pn.append(PlaceNode("balcony"))
pn.append(PlaceNode("corridor"))
pn.append(PlaceNode("bedroom"))
pn.append(PlaceNode("garage"))

# Init memory
memory = Memory()
for n in pn:
    # Return the active items
    memory.addNode(n)
    printActive(memory)


# remove the kitchen node
# ... active items should not change (limit = 4)
print "Removing kitchen node..."
memory.removeNode(str(pn[0]))

# remove the garage node
# ... active items should change, garage is removed (limit = 4)
print "Removing garage node..."
memory.removeNode(str(pn[6]))
printActive(memory)

# adding garage again
memory.addNode(str(pn[6]))
printActive(memory)

# Testing protection of items

# protect balcony item
print "Protecting balcony..."
memory.items["PlaceNode<balcony>"].keep_active = True
print "Keep balcony: ", memory.items["PlaceNode<balcony>"].keep_active

# add some more nodes
pn2 = []
pn2.append(PlaceNode("newnode1"))
pn2.append(PlaceNode("newnode2"))
pn2.append(PlaceNode("newnode3"))
pn2.append(PlaceNode("newnode4"))
pn2.append(PlaceNode("newnode5"))
for n in pn2:
    memory.addNode(n)

# print Active, balcony should still be there
printActive(memory)

# Tests for shape
# memory.shape(a)
# memory.shape(b)
# memory.shape(c)
# memory.shape(d)
# memory.shape(e)


# protect all active items
for i in memory.retreiveActiveItems():
    i.keep_active = True

# try activating new items (should leave memory unaffected)
pn3 = []
pn3.append(PlaceNode("newnodeX"))
pn3.append(PlaceNode("newnodeY"))
pn3.append(PlaceNode("newnodeZ"))
for n in pn3:
    memory.addNode(n)
printActive(memory)

# remove the items via iteration over active items
# Result: this is not allowed, RuntimeError because it is a generator function
# print "Removing all active nodes from memory."
# for i in memory.retreiveActiveItems():
#    memory.removeNode(str(i))
# printActive()

# a second take
print "Removing all active nodes from memory."
removelist = []
for i in memory.retreiveActiveItems():
    removelist.append(str(i))
for r in removelist:
    memory.removeNode(r)
printActive(memory)
printAll(memory)
