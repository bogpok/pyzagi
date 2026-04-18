
import sys
sys.path.append('D:/GitHub/pyzagi')

from src.pyzagi.pz_services_bizapi import *

bizagiEndpoints = BizagiServicesFactory.create()
bizagiEndpoints.list_services()
print(bizagiEndpoints.schema['oauth2'].paths['token'])