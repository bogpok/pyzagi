import pyodata
import requests

from scenarios.base import *

SERVICE_URL = baseURL + "/odata/data"

session = requests.Session()
print(client)
session.auth = (client['id'],client['secret'])
theservice = pyodata.Client(SERVICE_URL, session)