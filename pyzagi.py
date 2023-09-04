import requests
from passcodes import baseURL, clientid, clientsecret
bizagiAPIactions = {
    'getprocesses': '/odata/metadata/processes',
    'token': '/oauth2/server/token',
    'entities': "/odata/data/entities"
}

def gettoken():
    body = {
        'grant_type':'client_credentials',
        'scope':'api'
    }
    tokenr = requests.post(baseURL+bizagiAPIactions['token'],
                           data=body,
                           auth=(clientid, clientsecret))    
    return tokenr.json()['access_token']
    
def getprocesses(headers, lookupid = -1):
    r = requests.get(baseURL+bizagiAPIactions['getprocesses'],
                     headers=headers)
    pr_names = ''
    for proc in r.json()['value']:
        """
        dict_keys(
            ['@odata.id', 'id', 'name', 'displayName', 
            'entityId', 'parameters', 'template', 
            'processId', 'processType']
        )
        """
        pr_names += proc['name'] + '\n'
    print('\nProcesses structure:')
    print(r.json()['value'][0].keys())
    print('\nLookup:')
    print('Name: ', r.json()['value'][lookupid]['name'])
    print(r.json()['value'][lookupid]['@odata.id'])
    print()
    return pr_names

def oneprocess(headers, prid='a88c3aab-a94b-49c5-b83b-5b845d721d86'):    
    end = f'processes({prid})'
    link = baseURL+'odata/metadata/' + end
    r = requests.get(link,
                     headers=headers)
    print(r.text)

# OUTPUT:
{
  "@odata.context": ".../odata/metadata/$metadata#processes(a88c3aab-a94b-49c5-b83b-5b845d721d86)",
  "@odata.id": ".../odata/metadata/processes(a88c3aab-a94b-49c5-b83b-5b845d721d86)",
  "id": "a88c3aab-a94b-49c5-b83b-5b845d721d86",
  "name": "Simplerequest",
  "displayName": "Simple request",
  "entityId": "04ef0912-b730-492e-9724-b0b24c503859",
  "parameters": [
    {
      "id": "25c94f6c-c653-46c4-8983-eb50a3dc39df",
      "name": "Start date",
      "xpath": "Simplerequest.Requestdata.Startdate",
      "type": "DateTime"
    },
    {
      "id": "47b7ded1-ad53-4140-b4b8-2cf7b3c38bf3",
      "name": "End date",
      "xpath": "Simplerequest.Requestdata.Enddate",
      "type": "DateTime"
    },
    {
      "id": "16dc7670-cc3f-4f43-8a99-19d2e9f7c79f",
      "name": "Country",
      "xpath": "Simplerequest.Requestdata.City.Country",
      "type": "Entity"
    },
    {
      "id": "efdf136a-549b-46e1-9fa4-6b18b8c04608",
      "name": "City",
      "xpath": "Simplerequest.Requestdata.City",
      "type": "Entity"
    },
    {
      "id": "bdbde85f-b395-4611-9a3e-f20fae9e025a",
      "name": "Commentary",
      "xpath": "Simplerequest.Requestdata.Commentary",
      "type": "VarChar"
    }
  ],
  "template": [],
  "processId": 37,
  "processType": "Process"
}

def getents(headers):    
    end = bizagiAPIactions['entities']
    link = baseURL + end
    r = requests.get(link,
                     headers=headers)    
    for ent in r.json()['value']:        
        if ent['name'].lower().find('city') != -1 or ent['name'].lower().find('country') != -1:
            print(ent)  
    
# OUTPUT (Country)
{'@odata.id': '.../odata/data/entities(eb188de4-f35e-4fc9-bac1-383cf1231c88)',
  'id': 'eb188de4-f35e-4fc9-bac1-383cf1231c88', 
  'name': 'Country', 
  'displayName': 'Country',
  'type': 'Parameter', 
  'template': [{'name': 'Code', 'xpath': 'Code', 'type': 'VarChar'}, 
               {'name': 'Name', 'xpath': 'Name', 'type': 'VarChar'}, 
               {'name': 'Disabled', 'xpath': 'Disabled', 'type': 'Boolean'}]}

def get_country(headers):
    end = '/odata/data/entities(eb188de4-f35e-4fc9-bac1-383cf1231c88)/values'
    link = baseURL + end
    r = requests.get(link,
                     headers=headers)    
    return r.text

# Country values (one value example with full structure)
{
  "@odata.context": "https://dev-bizenv3-presalesea08.bizagi.com/odata/data/$metadata#entities(eb188de4-f35e-4fc9-bac1-383cf1231c88)/values",
  "@odata.totalCount": 3,
  "value": [
    {
      "@odata.id": "https://dev-bizenv3-presalesea08.bizagi.com/odata/data/entities(eb188de4-f35e-4fc9-bac1-383cf1231c88)/values(c8127415-66c3-45a3-b6ce-af99fe146a00)",  
      "id": "c8127415-66c3-45a3-b6ce-af99fe146a00",
      "parameters": [
        {
          "xpath": "Code",
          "value": "Spain"
        },
        {
          "xpath": "Name",
          "value": "Spain"
        },
        {
          "xpath": "dsbl",
          "value": False
        }
  ]}]}
    

def get_city(headers):
  end = "/odata/data/processes(a88c3aab-a94b-49c5-b83b-5b845d721d86)/relatedEntities(2af0f2a4-f72e-4c6b-8a9d-c392d14959db)/values"  
      
  #end = '/odata/data/entities(73fa9934-705f-4aea-a754-5a15a0aeb121)/values'
  link = baseURL + end
  r = requests.get(link,
                    headers=headers)    
  return r.text

def post_StartTAMS(headers):
  import json
  headers['Content-Type'] = 'application/json'
  end = 'odata/data/processes(939babe9-54ac-47de-b692-1a29b16dbb14)/start'
  print('\n=> starting: ', end)
  params = []
  body = {
    "startParameters": [
       
    ]
  }  
  r = requests.post(baseURL+end,
                    data=json.dumps(body),
                    headers=headers) 

  {"code":"500","type":"ODataException","status":"InternalServerError","message":"Could not create case for process id '939babe9-54ac-47de-b692-1a29b16dbb14'. Entity metadata not found. Entity ID: -1."}
     
  return r.text



def post_start(headers, processid = 'a88c3aab-a94b-49c5-b83b-5b845d721d86'):
  import json
  headers['Content-Type'] = 'application/json'

  end = f'/odata/data/processes({processid})/start'
  print('\n=> starting: ', end)
  spainid = "c8127415-66c3-45a3-b6ce-af99fe146a00"
  madridid = "87f59e55-ad84-4a64-b8d8-f9a3dbe051a7"
  body = {
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
  r = requests.post(baseURL+end,
                    data=json.dumps(body),
                    headers=headers)    
  return r.text

def getrelatedents(headers, processid = 'a88c3aab-a94b-49c5-b83b-5b845d721d86'):
  end = f'/odata/data/processes({processid})/relatedEntities'
  r = requests.get(baseURL+end,
                    headers=headers)    
  return r.text    
# Output
{
  "@odata.context": "https://dev-bizenv3-presalesea08.bizagi.com/odata/data/$metadata#processes(a88c3aab-a94b-49c5-b83b-5b845d721d86)/relatedEntities",
  "value": [
    {
      "@odata.id": "https://dev-bizenv3-presalesea08.bizagi.com/odata/data/processes(a88c3aab-a94b-49c5-b83b-5b845d721d86)/relatedEntities(2af0f2a4-f72e-4c6b-8a9d-c392d14959db)",  
      "id": "2af0f2a4-f72e-4c6b-8a9d-c392d14959db",
      "name": "City",
      "xpath": "Simplerequest.Requestdata.City"
    }
  ]
}

BTOKEN = f"Bearer {gettoken()}"
headers = {
    "Authorization": BTOKEN
}


# === Test ===

print(post_start(headers))
# print(post_StartTAMS(headers))
# print(oneprocess(headers,'939babe9-54ac-47de-b692-1a29b16dbb14'))



""" # dict_keys of 'getprocesses' response:
(['@odata.context', '@odata.totalCount', 'value'])
# where 'value' is a list of available processes from the provided Bizagi project

# dict_keys of response.json()['value'][i]:
(['@odata.id', 'id', 'name', 
  'displayName', 'entityId', 'parameters',
  'template', 'processId', 'processType']) """