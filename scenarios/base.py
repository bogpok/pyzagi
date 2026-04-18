"""Baseground for all scenarios"""
import sys
import json
sys.path.append('D:/GitHub/pyzagi')
from src.pyzagi.__init__ import (
  __version__,
  ConnectionBPM,
  ProcessBPM,
  EnvironmentBPM,
  StandaloneEntityBPM,
  createbody,
  json_print_pretty,
  print_attribs
)

print("\npyzagi version: "+__version__)
# Load environment specific values
sys.path.append('D:/GitHub/')
from mysecrets.biz.environment import baseURL, client, envName

# Establish connection
md_dev = EnvironmentBPM(envName, baseURL, client)
md_dev.print_info()

md_dev_con = ConnectionBPM(md_dev.baseURL, md_dev.client)