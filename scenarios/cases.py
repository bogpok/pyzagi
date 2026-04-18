""" ODATA Cases Usage"""
from base2 import *

# Get inbox to look over cases pending for user
""" json_print_pretty(md_dev_con.cases()) """

# this one will show parameters WITH VALUES
json_print_pretty(md_dev_con.cases(412))

# Get workitems for case (step 1)
""" json_print_pretty(md_dev_con.get_workitems(551)) """
# this will give pending tasks with parameters, indicating which are required 
# but it will not show if they already have any value
# for one item
# json_print_pretty(md_dev_con.get_workitems(406, 2471))

# generate list of parameters with values mapped from case info
""" json_print_pretty(md_dev_con.get_workitem_params(551, 3504)) """
# this will help to fill UI and understand what we need to provide as input to advance the case by this action

# to advance the case
# https://help.bizagi.com/platform/en/index.html?api_odata_completewi.htm

# FIRST STEP (set meeting)
""" 
md_dev_con.post_next(409, 2487,
                     createbody(["startParameters"], 
                                ["md_claim.dExecutiondate"], 
                                ["2024-2-28"]))
"""


# NAVIGATIONS
