# ISE API Documentation

*Explanation of API calls needed to support the automated ANC quarantine process*

---

## Purpose
The purpose of this readme file is to explain the difference between ISE's available APIs (Monitoring vs ERS) 
and to document all of the necessary API calls for the automated ANC quarantine process.

Cisco has documented these API calls for ISE 2.7 on their [Developer Portal](https://developer.cisco.com/docs/identity-services-engine/2.7/).

## Intended Audience
These API calls are intended for any InfoSec or Automation engineer responsible for automating ISE API calls, including:
* Apply ANC Policy
* Remove ANC Policy
* Check ANC Policy Status
* Search for Endpoints
* Issue a Change of Authorization Reauth
* Issue a Change of Authorization Disconnect

---
## Monitoring REST API
Allows you to locate, monitor, and accumulate important real-time, session-based information stored in individual endpoints in a network. You can access this information through a *Monitoring node*.

### Use-Cases
* Search for endpoints by MAC address
* Issue a Change of Authorization

### Features
* XML headers
* XML response
* Basic Authentication using Admin CLI credentials *(defined on ISE CLI)*
* Listens on TCP 443
* Queries only the Monitoring Nodes

*Quick Note: A Monitoring Node (or, MnT node) is an ISE "persona" assigned to a maximum of two ISE nodes in your deployment. It role is to act as the log collector and store log messages from the Administration and Policy Service nodes in a network. This persona provides advanced monitoring and troubleshooting tools that you can use to effectively manage a network and resources. A node with this persona aggregates and correlates the data that it collects, and provides you with meaningful reports.*

## Relevant API Calls

### [View Active Sessions](https://developer.cisco.com/docs/identity-services-engine/2.7/#!using-api-calls-for-session-management/active-sessions-list)
#### Function
* Search all **active endpoint sessions** available on ISE
#### Purpose
* Verify the endpoint has an active session in ISE
* Find an IP address, switch, or PSN associated to a MAC address.
* Useful to peform a reverse lookup for an endpoint. For example, when you need to find an endpoint by IP address instead of MAC address.

#### Headers
* Content-Type: application/xml
* Accept: application/xml
* Authorization: Basic *("CLI Credentials")*
#### HTTP Method
* GET
#### URI
```console
https://{ise-pan-fqdn}/admin/API/mnt/Session/ActiveList
```
*Note:  You must carefully enter each API call in the URL Address field of a target node, because these calls are case-sensitive. The use of “mnt” in the API call convention represents a Cisco Monitoring ISE node.*

*Note: Inactive Sessions are not listed!*
#### Response
* This output displays all of the **active endpoint sessions** within an ISE deployment. This ISE deployment only has 5 Active endpoint sessions.  

```console
<activeSessionList noOfActiveSession="5">
-
<activeSession>
<calling_station_id>00:0C:29:FA:EF:0A</calling_station_id>
<server>HAREESH-R6-1-PDP2</server>
</activeSession>
-
<activeSession>
<calling_station_id>70:5A:B6:68:F7:CC</calling_station_id>
<server>HAREESH-R6-1-PDP2</server>
</activeSession>
-
<activeSession>
<user_name>tom_wolfe</user_name>
<calling_station_id>00:14:BF:5A:0C:03</calling_station_id>
<nas_ip_address>10.203.107.161</nas_ip_address>
<nas_ipv6_address>2001:cdba::3257:9652</nas_ipv6_address>
<acct_session_id>00000032</acct_session_id>
<server>HAREESH-R6-1-PDP2</server>
</activeSession>
-
<activeSession>
<user_name>graham_hancock</user_name>
<calling_station_id>00:50:56:8E:28:BD</calling_station_id>
<nas_ip_address>10.203.107.161</nas_ip_address>
<nas_ipv6_address>2001:cdba::3257:9652</nas_ipv6_address>
<framed_ipv6_address>
<ipv6_address>200:cdba:0000:0000:0000:0000:3257:9652</ipv6_address>
<ipv6_address> 2001:cdba:0:0:0:0:3257:9651</ipv6_address>
<ipv6_address>2001:cdba::3257:9652</ipv6_address>
</framed_ipv6_address>
<acct_session_id>0000002C</acct_session_id>
<audit_session_id>0ACB6BA10000002A165FD0C8</audit_session_id>
<server>HAREESH-R6-1-PDP2</server>
</activeSession>
-
<activeSession>
<user_name>ipepvpnuser</user_name>
<calling_station_id>172.23.130.89</calling_station_id>
<nas_ip_address>10.203.107.45</nas_ip_address>
<nas_ipv6_address>2001:cdba::357:965</nas_ipv6_address>
<framed_ipv6_address>
<ipv6_address>200:cdba:0000:0000:0000:0000:3157:9652</ipv6_address>
<ipv6_address> 2001:cdba:0:0:0:0:3247:9651</ipv6_address>
<ipv6_address>2001:cdba::3257:962</ipv6_address>
</framed_ipv6_address>
<acct_session_id>A2000070</acct_session_id>
<server>HAREESH-R6-1-PDP2</server>
</activeSession>
</activeSessionList>
```

---

### [MAC Address Search](https://developer.cisco.com/docs/identity-services-engine/2.7/#!using-api-calls-for-session-management/invoking-the-macaddress-api-call) 
#### Function
* View an endpoint's active session information by querying its MAC address.
#### Purpose
* Target an endpoint to obtain to obtain its RADIUS information, including IP Address, NAD, Location, UserName, and more.
#### Headers
* Content-Type: application/xml
* Accept: application/xml
* Authorization: Basic *("CLI Credentials")*
#### HTTP Method
* GET
#### URI
*Note: You must include the primary MnT node for this API call! There are only 2 MnT nodes in each ISE deployment and the primary MnT node should never change, so this should be predictiable.*
```console
https://{ise-pan-fqdn}/admin/API/mnt/Session/MACAddress/{endpoint-mac-address}
```
*Note:  Make sure that you specify the MAC address using the XX:XX:XX:XX:XX:XX format. The MAC address input is case sensitive. Only uppercase characters are accepted for the MAC address input.*

*Note:  You must carefully enter each API call in the URL Address field of a target node because these calls are case-sensitive. The use of “mnt” in the API call convention represents a Cisco Monitoring ISE node.*

#### Response
```console
<sessionParameters>
<passed xsi:type="xs:boolean">true</passed>
<failed xsi:type="xs:boolean">false</failed>
<user_name>hunter_thompson</user_name>
<nas_ip_address>10.203.107.161</nas_ip_address>
<nas_ipv6_address>2001:cdba::357:965</nas_ipv6_address>
<framed_ipv6_address>
<ipv6_address>200:cdba:0000:0000:0000:0000:3157:9652</ipv6_address>
<ipv6_address> 2001:cdba:0:0:0:0:3247:9651</ipv6_address>
<ipv6_address>2001:cdba::3257:962</ipv6_address>
</framed_ipv6_address>
<calling_station_id>00:14:BF:5A:0C:03</calling_station_id>
<nas_port>50115</nas_port>
<identity_group>Profiled</identity_group>
<network_device_name>Core-Switch</network_device_name>
<acs_server>HAREESH-R6-1-PDP2</acs_server>
<authen_protocol>Lookup</authen_protocol>
-
<network_device_groups>
Device Type#All Device Types,Location#All Locations
</network_device_groups>
<access_service>RADIUS</access_service>
<auth_acs_timestamp>2010-12-15T02:11:12.359Z</auth_acs_timestamp>
<authentication_method>mab</authentication_method>
-
<execution_steps>
11001,11017,11027,15008,15048,15004,15041,15004,15013,24209,24211,22037,15036,15048,15048,15004,15016,11022,11002
</execution_steps>
<audit_session_id>0ACB6BA1000000351BBFBF8B</audit_session_id>
<nas_port_id>GigabitEthernet1/0/15</nas_port_id>
<nac_policy_compliance>Pending</nac_policy_compliance>
<auth_id>1291240762077361</auth_id>
<auth_acsview_timestamp>2010-12-15T02:11:12.360Z</auth_acsview_timestamp>
<message_code>5200</message_code>
<acs_session_id>HAREESH-R6-1-PDP2/81148292/681</acs_session_id>
<service_selection_policy>MAB</service_selection_policy>
<identity_store>Internal Hosts</identity_store>
-
<response>

{UserName=00-14-BF-5A-0C-03; User-Name=00-14-BF-5A-0C-03; State=ReauthSession:0ACB6BA1000000351BBFBF8B; Class=CACS:0ACB6BA1000000351BBFBF8B:HAREESH-R6-1-PDP2/81148292/681; Termination-Action=RADIUS-Request; cisco-av-pair=url-redirect-acl=ACL-WEBAUTH-REDIRECT; cisco-av-pair=url-redirect=https://HAREESH-R6-1-PDP2.cisco.com:8443/guestportal/gateway?sessionId=0ACB6BA1000000351BBFBF8B&action=cwa; cisco-av-pair=ACS:CiscoSecure-Defined-ACL=#ACSACL#-IP-ACL-DENY-4ced8390; }
</response>
<service_type>Call Check</service_type>
<use_case>Host Lookup</use_case>
<cisco_av_pair>audit-session-id=0ACB6BA1000000351BBFBF8B</cisco_av_pair>
<acs_username>00:14:BF:5A:0C:03</acs_username>
<radius_username>00:14:BF:5A:0C:03</radius_username>
<selected_identity_store>Internal Hosts</selected_identity_store>
<authentication_identity_store>Internal Hosts</authentication_identity_store>
<identity_policy_matched_rule>Default</identity_policy_matched_rule>
<nas_port_type>Ethernet</nas_port_type
<selected_azn_profiles>CWA</selected_azn_profiles>
-
<other_attributes>
ConfigVersionId=44,DestinationIPAddress=10.203.107.162,DestinationPort=1812,Protocol=Radius,Framed-MTU=1500,EAP-Key-Name=,CPMSessionID=0ACB6BA1000000351BBFBF8B,CPMSessionID=0ACB6BA1000000351BBFBF8B,EndPointMACAddress=00-14-BF-5A-0C-03,HostIdentityGroup=Endpoint Identity Groups:Profiled,Device Type=Device Type#All Device Types,Location=Location#All Locations,Model Name=Unknown,Software Version=Unknown,Device IP Address=10.203.107.161,Called-Station-ID=04:FE:7F:7F:C0:8F
</other_attributes>
<response_time>77</response_time>
<acct_id>1291240762077386</acct_id>
<acct_acs_timestamp>2010-12-15T02:12:30.779Z</acct_acs_timestamp>
<acct_acsview_timestamp>2010-12-15T02:12:30.780Z</acct_acsview_timestamp>
<acct_session_id>00000038</acct_session_id>
<acct_status_type>Interim-Update</acct_status_type>
<acct_session_time>78</acct_session_time>
<acct_input_octets>13742</acct_input_octets>
<acct_output_octets>6277</acct_output_octets>
<acct_input_packets>108</acct_input_packets>
<acct_output_packets>66</acct_output_packets>
-
<acct_class>
CACS:0ACB6BA1000000351BBFBF8B:HAREESH-R6-1-PDP2/81148292/681
</acct_class>
<acct_delay_time>0</acct_delay_time>
<started xsi:type="xs:boolean">false</started>
<stopped xsi:type="xs:boolean">false</stopped>
</sessionParameters>
```

---

### [Issue a Change of Authorization (CoA) Reauth](https://developer.cisco.com/docs/identity-services-engine/2.7/#!using-change-of-authorization-rest-apis/session-reauthentication-api-call)

#### Function
* Issue a Change of Authorization to force an endpoint to reauthenticate to ISE.
* The reauth CoA instructs the NAD to initate a new authentication to the endpoint by sending another EAPoL Start message to the endpoint.
* The new authentication maintains the same authentication session ID. 
#### Purpose
* Target an endpoint for reauthentication to ISE in order to apply a new auth-z policy, or assign a new logical identity group.
* In some scenarios, CoA may be needed to ensure an ANC policy is applied.
#### Headers
* Content-Type: application/xml
* Accept: application/xml
* Authorization: Basic ("CLI Credentials")
#### HTTP Method
* GET
#### Reauth Type
* REAUTH_TYPE_DEFAULT = 0
* REAUTH_TYPE_LAST = 1
* REAUTH_TYPE_RERUN = 2
#### URI
*Note: You must include the primary MnT node for this API call! There are only 2 MnT nodes in each ISE deployment, and the primary MnT node should never change, so this should be predictiable.*
```console
https://{ise-pan-fqdn}/admin/API/mnt/CoA/Reauth/{ise-mnt-hostname}/{endpoint-mac-address}/{reauth-type}
```
#### Response

```console
-
<remoteCoA requestType="reauth">
<results>true</results>
</remoteCoA>
```
---
### [Issue a Change of Authorization (CoA) Disconnect](https://developer.cisco.com/docs/identity-services-engine/2.7/#!using-change-of-authorization-rest-apis/session-disconnect-api-call)

#### Function
* Issue a Change of Authorization to an endpoint to force disconnect and reconnect (effectively forcing it to reauthenticate).
* The Port Bounce coa shuts down the switch port and then performs a no shutdown to renable it. this causes a link state to change, which simulates unplugigng and plugigng in of the network cable.
* The benefit of this type of CoA is that many devices try to renew their DHCP-assigned IP addresses when the link state changes. 
* This is most useful for headless devices and IoT endpoints!
#### Purpose
* Target an endpoint for reauthentication to ISE in order to apply a new auth-z policy, or assign a new logical identity group.
* In some scenarios, CoA may be needed to ensure that an ANC policy is applied.
#### Headers
* Content-Type: application/xml
* Accept: application/xml
* Authorization: Basic *("CLI Credentials")*
#### HTTP Method
* GET
#### Reauth Type
* DYNAMIC_AUTHZ_PORT_DEFAULT = 0
* DYNAMIC_AUTHZ_PORT_BOUNCE = 1
* DYNAMIC_AUTHZ_PORT_SHUTDOWN = 2
#### URI
```console
https://{ise-pan-fqdn}/admin/API/mnt/CoA/Disconnect/{ise-mnt-hostname}/{endpoint-mac-address}/0
```
#### Response

```console
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xs:schema version="1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema">
<xs:element name="remoteCoA" type="coAResult"/>
<xs:complexType name="coAResult">
<xs:sequence>
<xs:element name="results" type="xs:boolean" minOccurs="0"/>
</xs:sequence>
<xs:attribute name="requestType" type="xs:string"/>
</xs:complexType>
</xs:schema>
```
---
## External RESTful Services (ERS) API
ERS APIs are based on HTTPS protocol and REST methodology and uses port 9060. ERS is designed to allow external clients to perform CRUD (Create, Read, Update, Delete) operations on Cisco ISE resources. 

### Use-Cases
* View, Assign, and Clear ANC Policies

### Features
* JSON headers
* JSON response
* HTTP GET, POST, DELETE, PUT Methods
* Basic Authentication using ERS credentials (defined on ISE GUI)
* Listens on TCP 9060
* Queries the Policy Administration Node

*Quick Note: A Cisco ISE node with the Policy Administration persona allows you to perform all administrative operations on Cisco ISE. It handles all system-related configurations that are related to functionality such as authentication, authorization, and accounting. In a distributed deployment, you can have a maximum of two nodes running the Administration persona. The Administration persona can take on the standalone, primary, or secondary role.*

## Relevant API Calls

### [View All ANC Endpoints](https://developer.cisco.com/docs/identity-services-engine/2.7/#!anc-endpoint/api-reference)

#### Function
* View all endpoints that have been assigned to a ANC quarantine policy.
#### Purpose
* Verify an ANC policy has been applied successfully to a specific endpoint.
#### Headers
* Content-Type: application/json
* Accept: application/json
* Authorization: Basic *("ERS Credentials")*
#### HTTP Method
* GET
#### URI
```console
https://{ise-pan-fqdn}:9060/ers/config/ancendpoint
```
#### Response
```console
HTTP Status: 200 (OK)
Content:
XML <?xml version="1.0" encoding="UTF-8"?> &ltns0:searchResult xmlns:ns0="v2.ers.ise.cisco.com" xmlns:ns1="ers.ise.cisco.com" xmlns:ers-v2="ers-v2" total="2"> &ltns0:nextPage rel="next" href="link-to-next-page" type="application/xml"/> &ltns0:previousPage rel="previous" href="link-to-previous-page" type="application/xml"/> &ltns0:resources> &ltns1:resource description="description1" id="id1" name="name1"/> &ltns1:resource description="description2" id="id2" name="name2"/> </ns0:resources> </ns0:searchResult>
JSON
{
"SearchResult" : {
"total" : 2,
"resources" : [ {
"id" : "id1",
"name" : "name1",
"description" : "description1"
}, {
"id" : "id2",
"name" : "name2",
"description" : "description2"
} ],
"nextPage" : {
"rel" : "next",
"href" : "link-to-next-page",
"type" : "application/xml"
},
"previousPage" : {
"rel" : "previous",
"href" : "link-to-previous-page",
"type" : "application/xml"
}
}
```
---
### [Assign ANC Policy to an Endpoint](https://developer.cisco.com/docs/identity-services-engine/2.7/#!anc-endpoint/api-reference)

#### Function
* Assign an endpoint to an ANC Quarantine policy.
#### Purpose
* Quarantine an endpoint with an appropriate ANC policy for restricted access.
#### Headers
* Content-Type: application/json
* Accept: application/json
* Authorization: Basic *("ERS Credentials")*
#### HTTP Method
* PUT
#### URI
```console
https://{ise-pan-fqdn}:9060/ers/config/ancendpoint
```
#### Body
*You must provide the following .json body with your HTTP PUT request, including the MAC address and name of the appropriate ANC Policy to be assigned*
```console
{
  "OperationAdditionalData" : {
    "additionalData" : [ {
      "name" : "macAddress",
      "value" : "D4:BE:D9:86:35:1F"},
    {
       "name" : "policyName",
      "value" : "ANC_Quarantine"
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
### [Clear ANC Policy from an Endpoint](https://developer.cisco.com/docs/identity-services-engine/2.7/#!anc-endpoint/api-reference)

#### Function
* Clear an ANC policy from an endpoint in quarantine.
#### Purpose
* Remove ANC Quarantine policy from an endpoint to re-establish full network access.
#### Headers
* Content-Type: application/json
* Accept: application/json
* Authorization: Basic *("ERS Credentials")*
#### HTTP Method
* PUT
#### URI
```console
https://{ise-pan-fqdn}:9060/ers/config/ancendpoint/clear
```
#### Body
*You must provide the following .json body with your HTTP PUT request, including the MAC address and name of the appropriate ANC Policy to be removed*
```console
{
  "OperationAdditionalData" : {
    "additionalData" : [ {
      "name" : "macAddress",
      "value" : "D4:BE:D9:86:35:1F"},
    {
       "name" : "policyName",
      "value" : "ANC_Quarantine"
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

### Authors
Please contact me with questions or comments.
- James Sciortino - james.sciortino@outlook.com

# License
This project is licensed under the terms of the MIT License.
