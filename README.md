# PDDLMemory

A short-term memory module for AI planning

PDDLMemory is an attempt to integrate a short-term memory system similar to those found in natural cognitive systems (i.e. human short-term memory) into classical AI planning. Classical AI planning deals with the problem of finding a plan (i.e. a sequence of valid actions or planning steps) within the space of possible action sequences (...) or that of valid plans (...). The planning problem (or task?) is described in terms of an initial world state and a goal state that is to be achieved (what else?). Within a classical setting a planner searches for a solution to the problem (i.e. a valid plan)
using all the information that is provided, i.e. everything which is known about the world.

In PDDLMemory the information which is known about the world is clustered into chunks. Only a subset of chunks (active chunks) is provided to the planner for (commiting) the search. This approach which combines ideas from human memory research (see Cowan et al) and planning with partial information (see open world planning) aims to prevent the combinatorial explosion usually associated with classical planning problems of a realistic scale. While finding optimal plans is not the primary goal of PDDLMemory, we strive for generating plans of high quality [while] maintaining a reasonable level of cognitive plausibility by adhering to limitations of natural cognitive systems (such as short-term memory capacity).

The base implementation of PDDLMemory can be found in this repository together with detailed and easy-to-follow (but admittedly not very straightforward) installation instructions. If you come from a planning background and are interested in experimenting with the module (wwhich we higly encourage), it would be best to contact the author and exchange additional information.

The PDDLMemory module is part of the [PDDL Toolbox] together with [MyPDDL], a modular knowledge engineering tool for PDDL.

For further info on the module also check out the README file within the module folder.
