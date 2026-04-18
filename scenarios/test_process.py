
from scenarios.base import *


# Find process that you want to use 
print("List of processes:")
json_print_pretty(md_dev_con.get_processes())

# Use process id of target process to create Process object
# use 'properties' section of response's json to fill 'startstructure'
md_supportdesk = ProcessBPM('c3948c9b-6b9f-4183-972b-e49a8488682a', md_dev_con,
                         ["md_claim.sTitle", 
                          "md_claim.Category", 
                          "md_claim.tDescription", 
                          "md_claim.sLocation", 
                          "md_claim.Importance",
                          "md_claim.currAmount"])

# Then we should find all related entities to obtain
# print(md_supportdesk.related_entities.keys())
# dict_keys(['md Status', 'WFUSER', 'md Category', 'md Importance'])

# and their values
# json_print_pretty(md_supportdesk.related_entities['md Category'].get_rel_values())
# 1ec9c1b4-a3e1-4c8c-a7ce-d250e4b70ab6
# "Hardware issues"

# json_print_pretty(md_supportdesk.related_entities['md Importance'].values)

# Creation and advancing

# How to use input parameters with data types:
# https://help.bizagi.com/platform/en/index.html?api_odata_inputs.htm

# CREATE NEW CASE
# expert->authorization->New cases

""" md_supportdesk.start([
    "started from api",
    md_supportdesk.related_entities['md Category'].values["Hardware issues"]["value"],
    "Desc",
    "Location",
    md_supportdesk.related_entities['md Importance'].values["Medium"]["value"],
    "199" #currAmount
])
 """





