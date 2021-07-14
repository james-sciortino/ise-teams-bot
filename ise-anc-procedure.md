# ISE ANC Automation API Guidelines

*Explanation of API calls needed to support the automated ANC quarantine process*

---

## Purpose
The purpose of this readme file is to explain the API calls need to execute an ANC quarantine policy, in order.

Cisco has documented these API calls for ISE 2.7 on their [Developer Portal](https://developer.cisco.com/docs/identity-services-engine/2.7/).

---
## Prerequisites
You must know the MAC address of the endpoint.
You must know the ANC policy you wish to assign to the endpoint. There are three (3) ANC policies:
* ANC_No_Access
* ANC_Quarantine_Internal_Remediation
* ANC_Quarantine_With_Internet_Only

## Step 1 -[Assign the endpoint to the ANC Policy.](https://developer.cisco.com/docs/identity-services-engine/2.7/#!anc-endpoint/api-reference)
#### Headers
* Content-Type: application/json
* Accept: application/json
* Authorization: Basic
#### HTTP Method
* PUT
#### URI
```console
https://{ise-pan-fqdn}:9060/ers/config/ancendpoint
```
#### Body
*You must provide the following .json body with your HTTP PUT request, including the MAC address and name of the appropriate ANC Policy to be assigned*
*The MAC address must be provided in a colon-seperated format*
*The ANC Policy must be provided exactly as it is named in ISE*

## Apply the ANC_No_Access Policy
```console
{
  "OperationAdditionalData" : {
    "additionalData" : [ {
      "name" : "macAddress",
      "value" : "D4:BE:D9:86:35:1F"},
    {
       "name" : "policyName",
      "value" : "ANC_No_Access"
    } ]
  }
}
```
## Apply the ANC_Quarantine_Internal_Remediation Policy
```console
{
  "OperationAdditionalData" : {
    "additionalData" : [ {
      "name" : "macAddress",
      "value" : "D4:BE:D9:86:35:1F"},
    {
       "name" : "policyName",
      "value" : "ANC_Quarantine_Internal_Remediation"
    } ]
  }
}
```
## Apply the ANC_Quarantine_With_Internet_Only Policy
```console
{
  "OperationAdditionalData" : {
    "additionalData" : [ {
      "name" : "macAddress",
      "value" : "D4:BE:D9:86:35:1F"},
    {
       "name" : "policyName",
      "value" : "ANC_Quarantine_With_Internet_Only"
    } ]
  }
}
```
#### Response
```console
HTTP Status: null
Content:
N/A
```
---

## Step 2 -  [Verify the endpoint has been assigned to the ANC Quarantine policy.](https://developer.cisco.com/docs/identity-services-engine/2.7/#!anc-endpoint/api-reference)

## Part 1
#### Purpose
* Returns a list of *all* endpoints that are currently assigned to an ANC policy.
* The UUID (or, *id*) for each endpoint is listed in the response for this API call. 
* This *id* is needed in Step 2 - Part 2 (below)
#### Headers
* Content-Type: application/json
* Accept: application/json
* Authorization: Basic
#### HTTP Method
* GET
#### URI
```console
https://{ise-pan-fqdn}:9060/ers/config/ancendpoint
```
#### Response
```console
{
    "SearchResult": {
        "total": 1,
        "resources": [
            {
                "id": "6caf3e58-53b3-4bbd-9594-d3678aa08fc1",
                "link": {
                    "rel": "self",
                    "href": "https://{ise-pan-fqdn}:9060/ers/config/ancendpoint/6caf3e58-53b3-4bbd-9594-d3678aa08fc1",
                    "type": "application/json"
                }
            }
        ]
    }
}
```

### Part 2
#### Purpose
* Loop through each UUID (or, *id*)
* Find the targeted MAC address to ensure that is assigned to the ANC_No_Access policy
#### Headers
* Content-Type: application/json
* Accept: application/json
* Authorization: Basic
#### HTTP Method
* GET
#### URI
```console
https://{ise-pan-fqdn}:9060/ers/config/ancendpoint/{id}
```

#### Response
```console
{
    "ErsAncEndpoint": {
        "id": "6caf3e58-53b3-4bbd-9594-d3678aa08fc1",
        "macAddress": "D4:BE:D9:86:35:1F",
        "policyName": "ANC_No_Access",
        "link": {
            "rel": "self",
            "href": "https://{ise-pan-fqdn}:9060/ers/config/ancendpoint/6caf3e58-53b3-4bbd-9594-d3678aa08fc1",
            "type": "application/json"
        }
    }
}
```
---

## Step 3 - [Remove the ANC Quarantine policy.](https://developer.cisco.com/docs/identity-services-engine/2.7/#!anc-endpoint/api-reference)
#### Purpose
* Removes the endpoint from the ANC policy
#### Headers
* Content-Type: application/json
* Accept: application/json
* Authorization: Basic
#### HTTP Method
* GET
#### URI
```console
https://{ise-pan-fqdn}:9060/ers/config/ancendpoint/clear
```
#### Response
```console
{
    "SearchResult": {
        "total": 1,
        "resources": [
            {
                "id": "6caf3e58-53b3-4bbd-9594-d3678aa08fc1",
                "link": {
                    "rel": "self",
                    "href": "https://{ise-pan-fqdn}:9060/ers/config/ancendpoint/6caf3e58-53b3-4bbd-9594-d3678aa08fc1",
                    "type": "application/json"
                }
            }
        ]
    }
}
```

### Authors
Please contact me with questions or comments.
- James Sciortino - james.sciortino@outlook.com

# License
This project is licensed under the terms of the MIT License.
