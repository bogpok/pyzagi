from scenarios.base import *


# Entity operations
"""

BIZAGI STUDIO CONFIG:
mdm__CTMSettings was created as parameter entity 
and it's settings was set for web administration

"""
# Get entity from array
CTMSettingsEntity = md_dev_con.get_entity_object(1, Model=StandaloneEntityBPM)

# Show values
CTMSettingsEntity.get_values() 


# Create new value
""" 
CTMSettingsEntity.post_create([
    'testname', 'testcode', 'testvalue', 'false'
]) 
"""
