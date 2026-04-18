"""Baseground for all scenarios"""
import sys
import json
sys.path.append('D:/GitHub/pyzagi')
from src.pyzagi.__init__ import (
  __version__,
  BizagiServicesFactory,

  json_print_pretty,
)
from src.pyzagi.pz_connectionbpm import ConnectionBPM
print("\npyzagi version: "+__version__)

# Load environment specific values
sys.path.append('D:/GitHub/')
from mysecrets.biz.environment import baseURL, client, envName

# Establish connection
bizapi = BizagiServicesFactory.create()
md_dev_con = ConnectionBPM(baseURL=baseURL, client=client, ServiceAPI=bizapi)
