from config_utils import getChunkList

# The main module path (points to the PDDLMemory/pddlmemory folder)
pddlmemory_path = "/home/user/PDDLMemory/pddlmemory/"

##############################################################################

### PATHS & SYS CONFIG ###

# The path where the generated files are stored (write access needed)
output_path = pddlmemory_path + "output/"

# Determines whether the planner output is printed
print_planner_output = True

# Determines whether the parsed plan is printed
print_plan_steps = True

# Debug mode
DEBUG = False

### END PATHS & SYS CONFIG ###

##############################################################################

### PDDLMEMORY CONFIG ###

# Defines the number of items that can be activated at the same time. (>= 1, int)
activation_limit = 4

# Strategy: directed-rehearsal
# The number of maximum iterations (i.e planner runs)
maximum_iterations = 100

# Strategy: directed-rehearsal
# The strengthening factor of for relevant items during activation (>= 1, int)
strengthening_factor = 2

### END PDDLMEMORY CONFIG ###

##############################################################################

### CURRENT DOMAIN CONFIG ###
# Contains the path where the current domain and problem files are stored.
# Make sure that the pddl templates contain the right insertion marks.
# (e.g. [[KNOWLEDGE BASE]], [[GOAL BASE]])

# the current domain name
current_domain_name = "appartment"

# the current domain path
current_domain_path = pddlmemory_path + "domains/" + current_domain_name + "/"

current_domain_node_ids = getChunkList(current_domain_path)

### END CURRENT DOMAIN CONFING ###

##############################################################################

### EXTERNAL TOOLS ###

# The path for the default planner
planner_path = pddlmemory_path + "external/ff/ff"

### END EXTERNAL TOOLS ###