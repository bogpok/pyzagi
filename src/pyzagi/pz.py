import requests
import json
from typing import Union

from .pztools import createbody

class EnvironmentBPM:
  """
  Describes environment setup
  client : dict
  keys REQUIRED -> "id", "secret", "username"
  """
  def __init__(self, name: str, baseURL: str, client: dict):
    self.name = name
    self.baseURL = baseURL
    self.client = client
  def print_info(self):
    print(self.name, self.baseURL, self.client)

class ConnectionBPM:
  """
    Initiates and holds connection to the BPM system

    baseURL : str
      Link to your Bizagi project
    client['id'], client['secret']
      Authentication details
    timeout : int
      timeout for requests in seconds
  """
  def __init__(self, baseURL: str, client: dict, timeout: int = 30):
    
    self.baseURL = baseURL
    self.auth = (client['id'], client['secret'])

    self.timeout = timeout

    self.endpoints = {
      # AUTH
      'token': '/oauth2/server/token',
      # METADATA
      'getprocesses': '/odata/metadata/processes',
      # DATA
      'entities': "/odata/data/entities",
      'cases': "/odata/data/cases",
    }

    print('\n=> Initiating connection to Bizagi BPM...')
    try:
      self._gettoken()  
    except:
      raise ConnectionError('\n\tSomething went wrong with the connection.\n\tCheck the baseURL and BIZAGI server availability') 
    else:
      self.headers = {
          "Authorization": self.BTOKEN
      }
    print('Successfully connected to', baseURL, "\n")


  # GETS
  def _gettoken(self):
    body = {
        'grant_type':'client_credentials',
        'scope':'api'
    }  
    tokenr = requests.post(self.baseURL+self.endpoints['token'],
                               data=body,
                               auth=self.auth)   
    self.BTOKEN = f"Bearer {tokenr.json()['access_token']}" 

  def get_processes(self) -> list:
    """METADATA/PROCESSES

    responds as
    {@odata.context, @odata.totalCount, value}
    'value' has its own structure:
      ['@odata.id', 'id', 'name', 'displayName', 
      'entityId', 'parameters', 'template', 
      'processId', 'processType']

    Output: values
    """
    r = requests.get(self.baseURL+self.endpoints['getprocesses'],
                     headers=self.headers)   
    
    return r.json()['value']
    
  def get_process_names(self, lpi = None) -> list:
      """
      lpi - lookup index: get process info from index provided
      """
      processes_value = self.get_processes()      
      pr_names = []
      for process in processes_value:          
          pr_names.append((process['name'], process['id']))

      print('\nProcesses structure:')
      print(processes_value[0].keys())
      print('\nLOOCKUP')
      print('Name: ', processes_value[0]['name'])
      print(processes_value[0]['@odata.id'])

      if lpi == None:      
        return pr_names
      else:
        return pr_names[lpi]

  def get_oneprocess(self, processid):    
      end = f'({processid})'
      link = self.baseURL+self.endpoints['getprocesses'] + end
      r = requests.get(link, headers=self.headers)
      return r.json()["value"]
  
  def get_related_ents(self, processid, asstring = False):
    """DATA/RELATEDENTITIES
    """
    end = f'/odata/data/processes({processid})/relatedEntities'
    r = requests.get(self.baseURL+end,
                      headers=self.headers)    
    if asstring:
      return r.text
    else:
      return r.json()["value"]
  
  def get_related_ent_values(self, processid, entityid, asstring = False):
    """DATA/RELATEDENTITIES
    """
    end = f'/odata/data/processes({processid})/relatedEntities({entityid})/values'
    r = requests.get(self.baseURL+end,
                      headers=self.headers)    
    if asstring:
      return r.text
    else:
      return r.json()["value"]

  def get_entities(self, entityid = None):    
      """DATA/ENTITIES
      """      
      if entityid == None:
        link = self.baseURL + self.endpoints['entities'][1:]
        print("\nGet DATA/ENTITIES:", link)
        r = requests.get(link,
                        headers=self.headers)    
        return r.json()['value']
      else:
        link = self.baseURL + self.endpoints['entities'][1:]+f"({entityid})"        
        r = requests.get(link,
                        headers=self.headers) 
        return r.json()
      
  def search_entity(self, names):
      """Find entity by keyword in a name"""      
      entities = self.get_entities()
      for ent in entities:    
          for name in names:
            print(f"\nSearching for {name} in entities...")
            if ent['name'].lower().find(name) != -1:
              print("Found! Entity info:")
              print(ent)
  
  def get_entity_values(self, entityid):
    link = self.baseURL + self.endpoints['entities'] + f'({entityid})/values'
    print("\nGet values for entity:", link)
    r = requests.get(link,
                     headers=self.headers)    
    return r.json()

  def get_cases(self, caseid: Union[str, int] = None):
    """ DATA/CASES
    Shows inbox for authenticated user
    or info from one case if caseid is specified
    """
    if caseid != None:
      # caseid should be str or int, eg. 101 or "101"
      link = self.baseURL + self.endpoints['cases'] + \
            f"({caseid})"
      r = requests.get(link,
                       headers=self.headers)  
      return r.json()
    else:
      r = requests.get(self.baseURL + self.endpoints['cases'],
                      headers=self.headers)  
      return r.json()["value"]
    
  def get_cases_wi_related(self, caseid, workitemid, relatedid):
    link = self.baseURL + self.endpoints["cases"] + f"({caseid})/workitems({workitemid})" \
           + f"/relatedEntities({relatedid})"  
    r = requests.get(link,
                      headers=self.headers)  
    return r.json()    

  def get_workitems(self, caseid: Union[str, int], workitemid: Union[str, int] = None):
    # caseid should be str or int, eg. 101 or "101"
    if workitemid == None:
      link = self.baseURL + self.endpoints['cases'] + \
            f"({caseid})/workitems"
      r = requests.get(link,
                        headers=self.headers)  
      return r.json()
    else:
      link = self.baseURL + self.endpoints['cases'] + \
            f"({caseid})/workitems({workitemid})"
      r = requests.get(link,
                        headers=self.headers)  
      return r.json()

  def get_parameter_val(self, caseid: Union[str, int], workitemid: Union[str, int], paramid):
    link = self.baseURL + self.endpoints['cases'] + \
            f"({caseid})/workitems({workitemid})/parameter_values/{paramid}"
    r = requests.get(link,
                     headers=self.headers)
    return r.json()

  def get_workitem_params(self, caseid: Union[str, int], workitemid: Union[str, int]):
    """
    maps parameters of workitem with their current value
    by default get workitems will not show if they already have any value

    BIZAGI SETTING
    Turn on exposed attributes for process entity!
    """
    forcase = self.get_cases(caseid)

    caseparams_d = {}
    for casep in forcase["parameters"]: 
      key = casep['xpath'] 
      if "." in key:
        # for parameter entity save only "sCode"
        entityName, attrib = key.split(".")
        if attrib == "sCode":
          key = entityName
        else:
          key = None

      if key != None:
        caseparams_d[key] = casep

    workitemparams = self.get_workitems(caseid, workitemid)["parameters"] # list of dicts
      
    # load values    
    for i in range(len(workitemparams)):
      """
      caseparams_d: DICT
        key:
          {value, xpath_without_processentityname}

      workitemparams: LIST  
        [{id, name, type, xpath}]
      """
      # MAP "md_claim.sTitle" to "sTitle"
      cp_xpath = workitemparams[i]["xpath"].split(".")[1]
      workitemparams[i]["value"] = caseparams_d[cp_xpath]["value"]

    return workitemparams
    

  def get_workitem_related(self, caseid, workitemid, relatedid=None, showvalues=False):
    if relatedid == None:
      link = self.baseURL + self.endpoints['cases'] + \
              f"({caseid})/workitems({workitemid})/relatedEntities"
      r = requests.get(link,
                      headers=self.headers) 
      return r.json()["value"]
    else:
      link = self.baseURL + self.endpoints['cases'] + \
                f"({caseid})/workitems({workitemid})/relatedEntities({relatedid})"
      if showvalues:
        link += "/values"
      
      r = requests.get(link,
                      headers=self.headers) 
      return r.json()
    
  def get_case_navigations(self, caseid):
    link = self.baseURL + self.endpoints['cases'] + f"({caseid})" + "/navigations"
    r = requests.get(link,
                      headers=self.headers) 
    return r.json()
  
  


  # POSTS
  def _post_handler(self, link, body, headers):
    try:
        r = requests.post(link,
                      data=json.dumps(body),
                      headers=headers,
                      timeout=self.timeout)          
        print(' Status:', r.status_code, "/ Details:\n", r.text)
        return r.text
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

  def post_start(self, processid, body, headers=None):
    """ start process with 'processid' """
    if headers is None:
      headers = self.headers
      headers['Content-Type'] = 'application/json'

    link = self.baseURL+f'/odata/data/processes({processid})/start'
    print('\n=> Starting: ', link)    
    
    return self._post_handler(link, body, headers)

  def post_next(self, caseid: Union[str, int], workitemid: Union[str, int], body, headers=None):
    """ advance caseid with workitemid """
    if headers is None:
      headers = self.headers
      headers['Content-Type'] = 'application/json'
    
    link = self.baseURL + self.endpoints['cases'] + \
            f"({caseid})/workitems({workitemid})/next"
    print(f"=> Advancing case-{caseid} with workitem-{workitemid}")

    return self._post_handler(link, body, headers)
    
  
    
class ProcessBPM:
  def __init__(self, processid: str, connection: ConnectionBPM,
               startstructure:list[str]):
    self.id = processid
    self.connection = connection
    self.headers = connection.headers
    self.headers['Content-Type'] = 'application/json'

    self.structures = {}
    self.clearbody()

    self.setstartstructure(startstructure)

    self.related_entities = {}
    self.load_related()

  def setstructure(self, name:str, structure:list[str]):
    self.structures[name] = structure

  def setstartstructure(self, structure:list[str]):
    self.setstructure('start', structure)

  def setstartbody(self, values:list[str]):
    self.body = createbody(["startParameters"], self.structures['start'], values)

  def clearbody(self):
    self.body = ""

  def start(self, values:list[str]):
    self.setstartbody(values)
    # POST START
    print(self.connection.post_start(processid=self.id, body=self.body, headers=self.headers))
    self.clearbody()

  def get_info(self):
    return self.connection.get_oneprocess(self.id)
  
  def get_related(self, asstring = False):
    return self.connection.get_related_ents(self.id, asstring)
  
  def load_related(self):
    related = self.get_related()
    for ent in related:
      ent['odataid'] = ent['@odata.id']
      del ent['@odata.id']
      self.related_entities[ent['name']] = EntityBPM(**ent, parentProcess = self)


class EntityBPM:
  def __init__(self, id, name, xpath, odataid, parentProcess: ProcessBPM):
    self.id = id
    self.name = name
    self.xpath = xpath
    self.odataid = odataid
    self.parentProcess = parentProcess
    
    self.values = {}
    self.load_values()

  def get_values(self):
    """
    Get values for entity: https://dev-demo1-mdcloud.bizagi.com//odata/data/entities(761dd1a6-af51-477e-baf7-dea0b7d0305c)/values
    {'code': '500', 'type': 'ODataException', 'status': 'InternalServerError', 'message': 'Entity metadata not found. Entity ID: -1.'}
    """
    return self.parentProcess.connection.get_entity_values(self.id)
  
  def get_rel_values(self):
    # print(f"\nRelated values for ({self.name}):")
    return self.parentProcess.connection.get_related_ent_values(self.parentProcess.id, self.id)
  
  def load_values(self):
    values = self.get_rel_values()
    for value in values:
      self.values[value["label"]] = value







