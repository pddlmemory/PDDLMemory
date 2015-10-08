===========
PDDL Memory
===========

This is the PDDL Memory module which implements a simple
memory system for AI planning with PDDL. The PDDL Memory module was 
developed as part of my Bachelor's Thesis, "Implementation and evaluation 
of a short-term memory for a simulated household robot".

Author: Ivo Chichkov

===========
Code
===========

If you want to look at the code, the following files provide good insight:

pddlmemory/memory/main.py 	- the core memory module
pddlmemory/ce.py		- the central executive module
pddlmemory/memory/placenode.py	- The PlaceNode class

===========
Install
===========

For installation instructions, please consult the provided html documentation.
(docs/index.html)

===========
The PDDLMemory Domain Representation
===========

+- Domain

	domain-template.pddl
	problem-template.pddl

	+- Chunk1
		+- facts
		+- goals

	+- Chunk2
		+- facts
		+- goals

	(+- base 
		+- facts
		+- goals )
...

The Domain consists of folders that represent Chunks and the domain and problem templates.

Every Chunk in the domain should have an extra folder with subfolders
for facts and goals. The facts folder should contain a .pdkb file, which
is a list of predicates. The goals folder can contain one or several goals
as .pdkb files, which are also lists of predicates.
The domain-folder should include a domain-template.pddl and a problem-template.pddl,
The problem template should contain the appropriate insertion marks. 
([[KNOWLEDGE BASE]], [[GOAL BASE]]) All the objects present in the world should be 
encoded in the problem template file.

The domain can contain a base node. The base node stores information which is never
forgotten. It can be used to store the robot's location or other essential fact
and/or goal knowledge.

