# PDDLMemory

A short-term memory module for AI planning

PDDLMemory is an attempt to integrate a short-term memory system similar to those found in natural cognitive systems (i.e. human short-term memory) into classical AI planning. Classical AI planning deals with the problem of finding a plan (i.e. a sequence of valid actions or planning steps) within the space of possible world states (state space search) or that of valid plans (plan state search). The planning task consists of a logical description of the initial situation, a set of possible actions and a goal state that is to be achieved. Within a classical setting a planner searches for a solution to the problem (i.e. a valid plan) using all the information that is provided, i.e. everything which is known about the world.

In PDDLMemory the information which is known about the world is clustered into chunks. Only a subset of chunks (active chunks) is provided to the planner for conducting search. This approach which combines ideas from human memory research (see Cowan, 1999) and planning with partial observability (see open world assumption, e.g. Talamadupula et al., 2010) aims to prevent the combinatorial explosion usually associated with classical planning problems of a realistic scale. While finding optimal plans is not the primary goal of PDDLMemory, we strive for generating plans of high quality and maintaining a reasonable level of cognitive plausibility by adhering to limitations of natural cognitive systems (such as short-term memory capacity).

  The base implementation of PDDLMemory can be found in this repository together with detailed and easy-to-follow (but admittedly not very straightforward) [installation instructions](https://pddlmemory.github.io/pddlmemory). If you come from a planning background and are interested in experimenting with the module (which we higly encourage), it would be best to contact the [author](mailto:ivo.chichkov@hotmail.com) and exchange additional information.

The PDDLMemory module is part of the [PDDL Toolbox (todo: add link)](http://about:blank) together with [MyPDDL](https://github.com/Pold87/myPDDL), a modular knowledge engineering tool for PDDL.

For further info on the module also check out the README file within the module folder.
