import sys
sys.path.append('D:/GitHub/')
from pyzagi import *


# === Test ===
sys.path.append('C:\\Users\\Bogdan\\Documents\\src\\py\\beezaga')
import passcodes as pc

bizagibpm = ConnectionBPM(
	pc.baseURL,
	pc.clientid,
	pc.clientsecret
)

body_simpleRequest = {
      "startParameters": [
        {
          "xpath": "Simplerequest.Requestdata.Startdate",
          "value": "2023-08-28"
        },
        {
          "xpath": "Simplerequest.Requestdata.Enddate",
          "value": "2023-09-05"
        },
        {
          "xpath": "Simplerequest.Requestdata.Commentary",
          "value": "Sent from Python =)"
        },
           
      ]
    }  					
print(bizagibpm.post_start(body = body_simpleRequest))

# print(oneprocess(headers,'939babe9-54ac-47de-b692-1a29b16dbb14'))