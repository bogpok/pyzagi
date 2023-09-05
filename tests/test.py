import sys
sys.path.append('D:/GitHub/')
from pyzagi.src import *


# === Test ===

from mysecrets.pztg.passcodes import baseURL, clientid, clientsecret

bizagibpm = ConnectionBPM(
	baseURL,
	clientid,
	clientsecret
)
simpleRequest = Process(
  processid = 'a88c3aab-a94b-49c5-b83b-5b845d721d86',
  connection = bizagibpm,
  startstructure = [
    "Simplerequest.Requestdata.Startdate",
    "Simplerequest.Requestdata.Enddate",
    "Simplerequest.Requestdata.Commentary",
  ]
) 

simpleRequest.start([
  "2023-08-28",
  "2023-09-05",
  "Sent from Python =)"
])

# body_simpleRequest = {
#       "startParameters": [
#         {
#           "xpath": "Simplerequest.Requestdata.Startdate",
#           "value": "2023-08-28"
#         },
#         {
#           "xpath": "Simplerequest.Requestdata.Enddate",
#           "value": "2023-09-05"
#         },
#         {
#           "xpath": "Simplerequest.Requestdata.Commentary",
#           "value": "Sent from Python =)"
#         },
           
#       ]
#     }  					


# print(oneprocess(headers,'939babe9-54ac-47de-b692-1a29b16dbb14'))


# spainid = "c8127415-66c3-45a3-b6ce-af99fe146a00"
# madridid = "87f59e55-ad84-4a64-b8d8-f9a3dbe051a7"
