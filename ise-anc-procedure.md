# ISE ANC Automation API Procedure

*Explanation of API calls needed to support the automated ANC quarantine process*

---

## About
The purpose of this procedural document is to explain the API calls need to execute an ANC quarantine policy, in order.
These steps should match KB article for ANC Quarantine.

For additional technical details on Cisco ISE API, navigate to Cisco's [Developer Portal](https://developer.cisco.com/docs/identity-services-engine/2.7/).

---
## Prerequisites
1. You must know the MAC address of the endpoint.
2. You must know the ANC policy you wish to assign to the endpoint. There are three (3) ANC policies:
* ANC_No_Access
* ANC_Quarantine_Internal_Remediation
* ANC_Quarantine_With_Internet_Only

## Step 1 -[Assign the endpoint to the ANC Policy.](https://developer.cisco.com/docs/identity-services-engine/2.7/#!anc-endpoint/apply)
#### Headers
* Content-Type: application/json
* Accept: application/json
* Authorization: Basic
#### HTTP Method
* PUT
#### URI
```console
https://{ise-pan-fqdn}:9060/ers/config/ancendpoint/apply
```
#### Body
*NOTE:*
*You must provide the following .json body with your HTTP PUT request, including the MAC address and name of the appropriate ANC Policy to be assigned*
*The MAC address should be colon seperated, e.g: D4:BE:D9:3D:25:E2*
*The ANC Policy must be provided exactly as it is named in ISE, e.g: ANC_No_Access*

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

## Step 2 -  [Verify the endpoint has been assigned to the ANC Quarantine policy.](https://developer.cisco.com/docs/identity-services-engine/2.7/#!anc-endpoint/get-all)

## Part 1
#### Purpose
* Returns a list of *all* endpoints that are currently assigned to an ANC policy.
* The UUID (or, *id*) for each endpoint is listed in the response of this API call. 
* The UUID (or, *id*) is needed for verification of the endpoint in Step 2 - Part 2 (below)
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
* Find the targeted MAC address to ensure that is assigned to the appropriate ANC Policy.
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

## Step 3 - [Validate the Endpoint's RADIUS Session Info.](https://developer.cisco.com/docs/identity-services-engine/2.7/#!using-api-calls-for-session-management/invoking-the-activelist-api-call)
#### Purpose
* Equivalent to checking ISE Live Logs, to be sure the endpoint has been reauthorized with the ANC policy.
#### Headers
* Content-Type: application/xml
* Accept: application/xml
* Authorization: Basic
#### HTTP Method
* PUT
#### URI
```console
https://{ise-pan-fqdn}/admin/API/mnt/Session/MACAddress/{mac-address}
```
*Note: The MAC address should be colon seperated, e.g: D4:BE:D9:3D:25:E2*
#### Response
```console
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sessionParameters>
    <passed xsi:type="xs:boolean" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">false</passed>
    <failed xsi:type="xs:boolean" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">true</failed>
    <user_name>D4:BE:D9:3D:25:E2</user_name>
    <nas_ip_address>10.16.150.65</nas_ip_address>
    <failure_reason>15039 Rejected per authorization profile</failure_reason>
    <calling_station_id>D4:BE:D9:3D:25:E2</calling_station_id>
    <orig_calling_station_id>D4-BE-D9-3D-25-E2</orig_calling_station_id>
    <cpmsession_id>4196100A00000015A5844252</cpmsession_id>
    <destination_ip_address>10.16.8.14</destination_ip_address>
    <device_ip_address>10.16.150.65</device_ip_address>
    <identity_group>Workstation</identity_group>
    <network_device_name>yrt-2700-fl0-fe1-1</network_device_name>
    <acs_server>NGN-BL-ISE1</acs_server>
    <authentication_method>mab</authentication_method>
    <authentication_protocol>Lookup</authentication_protocol>
    <framed_ip_address>10.16.156.104</framed_ip_address>
    <auth_acs_timestamp>2021-07-14T16:07:48.723-05:00</auth_acs_timestamp>
    <execution_steps>11001,11017,11027,15049,15008,15048,15041,15013,24209,24211,22037,24715,15036,15048,15016,15039,11003</execution_steps>
    <response>{RadiusPacketType=AccessReject; AuthenticationResult=Passed; UserName=D4:BE:D9:3D:25:E2; }</response>
    <audit_session_id>4196100A00000015A5844252</audit_session_id>
    <nas_port_id>GigabitEthernet1/0/8</nas_port_id>
    <posture_status></posture_status>
    <selected_azn_profiles>DenyAccess</selected_azn_profiles>
    <service_type>Call Check</service_type>
    <message_code>5400</message_code>
    <auth_acsview_timestamp>2021-07-14T16:07:48.723-05:00</auth_acsview_timestamp>
    <auth_id>1623274324531193</auth_id>
    <identity_store>Internal Endpoints</identity_store>
    <response_time>10</response_time>
    <framed_ipv6_address>
        <ipv6_address></ipv6_address>
        <ipv6_address>fe80::3ce5:8ad1:dc5c:5636</ipv6_address>
    </framed_ipv6_address>
    <other_attr_string>:!:ConfigVersionId=99:!:Device Port=57919:!:DestinationPort=1812:!:RadiusPacketType=AccessRequest:!:Protocol=Radius:!:NAS-Port=50108:!:Framed-MTU=1468:!:EAP-Key-Name=:!:OriginalUserName=d4bed93d25e2:!:NetworkDeviceProfileId=b0699505-3150-4215-a80e-6753d45bf56c:!:IsThirdPartyDeviceFlow=false:!:AcsSessionID=NGN-BL-ISE1/414922244/4706:!:UseCase=Host Lookup:!:SelectedAuthenticationIdentityStores=Internal Endpoints:!:IdentityPolicyMatchedRule=MAB:!:AuthorizationPolicyMatchedRule=Quarantine_Policy_Blacklist_Access-Reject:!:EndPointMACAddress=D4-BE-D9-3D-25-E2:!:ISEPolicySetName=Bender_Lab_Wired_MAB:!:IdentitySelectionMatchedRule=MAB:!:DTLSSupport=Unknown:!:HostIdentityGroup=Endpoint Identity Groups:Profiled:Workstation:!:Network Device Profile=Cisco:!:Location=Location#All Locations:!:Device Type=Device Type#All Device Types:!:IPSEC=IPSEC#Is IPSEC Device#No:!:StepData="5= Normalised Radius.RadiusFlowType","7=Internal Endpoints","13= Session.ANCPolicy"=StepData:!:RADIUS Username=D4:BE:D9:3D:25:E2:!:Device IP Address=10.16.150.65:!:CPMSessionID=4196100A00000016A6D501B4:!:Called-Station-ID=00:EA:BD:16:EC:C7:!:CiscoAVPair=cts-pac-opaque=****,service-type=Call Check,audit-session-id=4196100A00000016A6D501B4,method=mab,client-iif-id=375698430</other_attr_string>
    <acct_id>1623274324530546</acct_id>
    <acct_acs_timestamp>2021-07-14T16:05:36.820-05:00</acct_acs_timestamp>
    <acct_acsview_timestamp>2021-07-14T16:05:36.820-05:00</acct_acsview_timestamp>
    <acct_session_id>00000053</acct_session_id>
    <acct_status_type>Stop</acct_status_type>
    <acct_session_time>749</acct_session_time>
    <acct_input_octets>251</acct_input_octets>
    <acct_output_octets>0</acct_output_octets>
    <acct_input_packets>2</acct_input_packets>
    <acct_output_packets>0</acct_output_packets>
    <acct_terminate_cause>Admin Reset</acct_terminate_cause>
    <acct_authentic>Remote</acct_authentic>
    <acct_delay_time>0</acct_delay_time>
    <event_timestamp>1626296503</event_timestamp>
    <started xsi:type="xs:boolean" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">true</started>
    <stopped xsi:type="xs:boolean" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">false</stopped>
    <endpoint_policy>Microsoft-Workstation</endpoint_policy>
</sessionParameters>
```


## Step 4 - [Clear the ANC Quarantine policy.](https://developer.cisco.com/docs/identity-services-engine/2.7/#!anc-endpoint/api-reference)
#### Purpose
* Removes the endpoint from the ANC policy
#### Headers
* Content-Type: application/json
* Accept: application/json
* Authorization: Basic
#### HTTP Method
* PUT
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
