from os.path import join

'''Network files for the initial ICCPS submission.'''
"""
DOUBLE_LOOP = join(
    "configs", "ICCPS", "double_loop", "double.net.xml"
)
GRID_3x3 = join(
    "configs", "ICCPS", "grid_3x3", "grid-3x3.net.xml"
)
GRID_5x5 = join(
    "configs", "ICCPS", "grid_5x5", "grid-5x5.net.xml"
)
GRID_7x7 = join(
    "configs", "ICCPS", "grid_7x7", "grid-7x7.net.xml"
)
GRID_9x9 = join(
    "configs", "ICCPS", "grid_9x9", "grid-9x9.net.xml"
)

BOSTON_DEPR = join(
    "configs", "ICCPS", "__old", "boston_inter", "boston.net.xml"
)
COMPLEX_DEPR = join(
    "configs", "ICCPS", "__old", "complex_inter", "complex_inter.net.xml"
)
SINGLE_LOOP_DEPR = join(
    "configs", "ICCPS", "__old", "single_loop", "single.net.xml"
)
"""

# '''Network files for the first resubmission.'''
# GRID_3x3 = join(
#     "configs", "SMARTCOMP", "grid-3x3.net.xml"
# )
# GRID_5x5 = join(
#     "configs", "SMARTCOMP", "grid-5x5.net.xml"
# )
# GRID_7x7 = join(
#     "configs", "SMARTCOMP", "grid-7x7.net.xml"
# )

# V2_GRID = join(
#     "configs", "SMARTCOMP", "grid-3x3.net.xml"
# )
# V2_SPIDER = join(
#     "configs", "SMARTCOMP", "spider.net.xml"
# )
# V2_RANDOM = join(
#     "configs", "SMARTCOMP", "rand.net.xml"
# )


# # new CA networks

# CA_allred_3x3 = join(
#     "configs", "CA_allred", "grid-3x3.net.xml"
# )
# CA_allred_5x5 = join(
#     "configs", "CA_allred", "grid-5x5.net.xml"
# )
# CA_allred_7x7 = join(
#     "configs", "CA_allred", "grid-7x7.net.xml"
# )


# '''

# Because a 4‑way stop has no traffic signal. 
# In SUMO, unsignalized intersections are represented as type="priority" (right‑of‑way is resolved by priority/requests), not type="traffic_light". 
# To make the center behave like a normal 4‑way stop, we removed the tlLogic and switched the junction to type="priority" and cleared tl/linkIndex from its connections.

# '''

# CA_4waystop_3x3 = join(
#     "configs", "CA_4waystop", "grid-3x3.net.xml"
# )
# CA_4waystop_5x5 = join(
#     "configs", "CA_4waystop", "grid-5x5.net.xml"
# )
# CA_4waystop_7x7 = join(
#     "configs", "CA_4waystop", "grid-7x7.net.xml"
# )




# CA_disconnected_3x3 = join(
#     "configs", "CA_disconnected", "grid-3x3.net.xml"
# )
# CA_disconnected_5x5 = join(
#     "configs", "CA_disconnected", "grid-5x5.net.xml"
# )
# CA_disconnected_7x7 = join(
#     "configs", "CA_disconnected", "grid-7x7.net.xml"
# )







