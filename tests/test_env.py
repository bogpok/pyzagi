import sys
import json
sys.path.append('D:/GitHub/pyzagi')
from src.pyzagi.__init__ import (
  __version__,
  ConnectionBPM,
  ProcessBPM,
  EnvironmentBPM,
  createbody
)

print(__version__)

def json_print_pretty(json_):
    print(json.dumps(json_, sort_keys=True, indent=4))


# === Test ===
sys.path.append('D:/GitHub/')
from mysecrets.biz.environment import baseURL, client, envName

md_dev = EnvironmentBPM(envName, baseURL, client)
md_dev.print_info()
# 1 Establish connection
md_dev_con = ConnectionBPM(md_dev.baseURL, md_dev.client)

# 2 Find process that you want to use 
# md_dev_con.get_processes()

# 3 Use process id of target process to create Process object
# use 'properties' section of response's json to fill 'startstructure'
md_supportdesk = ProcessBPM('c3948c9b-6b9f-4183-972b-e49a8488682a', md_dev_con,
                         ["md_claim.sTitle", "md_claim.Category", "md_claim.tDescription", "md_claim.sLocation", "md_claim.Importance"])

# 4 Then we should find all related entities to obtain
# print(md_supportdesk.related_entities.keys())
# dict_keys(['md Status', 'WFUSER', 'md Category', 'md Importance'])

# and their values
# json_print_pretty(md_supportdesk.related_entities['md Category'].get_rel_values())
# 1ec9c1b4-a3e1-4c8c-a7ce-d250e4b70ab6
# "Hardware issues"

# json_print_pretty(md_supportdesk.related_entities['md Importance'].values)

# 5 Creation and advancing

# How to use input parameters with data types:
# https://help.bizagi.com/platform/en/index.html?api_odata_inputs.htm

# 5.1 CREATE NEW CASE
# expert->authorization->New cases

md_supportdesk.start([
    "started from api",
    md_supportdesk.related_entities['md Category'].values["Hardware issues"]["value"],
    "Desc",
    "Location",
    md_supportdesk.related_entities['md Importance'].values["Medium"]["value"]
])

# 5.2 Advance task through task

# Get inbox to look over cases pending for user
# json_print_pretty(md_dev_con.get_cases())

# this one will show parameters WITH VALUES
# json_print_pretty(md_dev_con.get_cases(406))

# Get workitems for case (step 1)
# json_print_pretty(md_dev_con.get_workitems(409))
# this will give pending tasks with parameters, indicating which are required 
# but it will not show if they already have any value
# for one item
# json_print_pretty(md_dev_con.get_workitems(406, 2471))

# generate list of parameters with values mapped from case info
# json_print_pretty(md_dev_con.get_workitem_params(409, 2489))
# this will help to fill UI and understand what we need to provide as input to advance the case by this action

# to advance the case
# https://help.bizagi.com/platform/en/index.html?api_odata_completewi.htm

# FIRST STEP (set meeting)
""" md_dev_con.post_next(409, 2487,
                     createbody(["startParameters"], 
                                ["md_claim.dExecutiondate"], 
                                ["2024-2-28"])) """

# try to turn web administration for param entity to check

# TODO 
# flow / process structure???






