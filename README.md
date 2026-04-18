# Overview

**pyzagi** [WIP] is Bizagi ODATA API handler for Python

## Changelog
### 0.2.0
- Refatored to match common design patterns
- Scenarios are described as part of manual for usage

### 0.1.0
- ProcessBPM has more attributes and methods, allowing to bind related entities
- EntityBPM is a new class for entities and their values
- EnvironmentBPM is a new class to hold environment specific attributes
- New methods: get_cases, workitems, workitem/next


## Quick start guide

### Establishing connection
First thing to do is make connection object, which will be used as main interface for calls

```py
connection = ConnectionBPM(
	baseURL,
	clientid,
	clientsecret
)
```

### Process object
With known process id you can create ProcessBPM object. It is helful to use this object for operations with process, e.g. start, show related entities, etc.

```py
simpleRequest = ProcessBPM(
  processid = 'a88c3aab-a94b-49c5-b83b-5b845d721d86',
  connection = connection,
  startstructure = [
    "Simplerequest.Requestdata.Startdate",
    "Simplerequest.Requestdata.Enddate",
    "Simplerequest.Requestdata.Commentary",
  ]
) 
```
The `startstructure` property will create a base for `startParameters` when making `process/start` request.

#### Case creation (process/start)

```py
simpleRequest.start([
  "2023-08-28",
  "2023-09-05",
  "Sent from Python =)"
])

"""
This will set following request body and send the request:
"""

simpleRequest.body = {
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
```




## TODO 
- flow / process structure???
- full coverage
- design patterns
- unittests
- get values as table
