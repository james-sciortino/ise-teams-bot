#! /usr/bin/env python3
####
import sys
from manager import ise
import requests
import urllib3
from requests.auth import HTTPBasicAuth
import re
import xmltodict, json
from xml.etree import ElementTree as ET
import sys
sys.path.append('C:/Users/james.sciortino/OneDrive/James/Python/Network-Automation/ISE/ISE-Context-Bot/bots')
from custom_prompt_bot import CustomPromptBot
####
# Silence the insecure warning due to SSL Certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#### 
ise_host = ise["host"]
ise_ers = ise["ers"]
ers_admin = ise["ersadmin"]
ers_pwd = ise["erspass"]
cli_admin = ise["cliadmin"]
cli_pwd = ise["clipass"]
#### 
headers =   {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
####
api_headers =   {
    "Content-Type": "application/xml",
    "Accept": "application/xml"
}
####
payload = []
####
def ise_api(call):
    url = "https://{}:{}{}".format(ise_host, ise_ers, call)
    return url
####
def mac_selection():
    selection = input("Enter the MAC address of the Endpoint you want to manage! ")  
    return selection 
####
def mac_search(mac_str): # Search Endpoint by MAC and dump the available options on screen.
    ise_url = ise_api("endpoint?filter=mac.CONTAINS.{}".format(mac_str))
    response = requests.request("GET", ise_url, auth=HTTPBasicAuth(ers_admin, ers_pwd),
                                headers=headers, verify=False)
    body = response.text
    mac_addr = json.loads(body)["SearchResult"]["resources"]
    found_macs = []
    for mac in mac_addr:
        found_macs.append((mac)["name"])
    return found_macs
####
def general_menu(data):       # Present your menu options using the dictionary made from numbered_menu()
        for obj in data:
            print(obj)
        print("0: Exit")
        print(67 * "-")
        return obj
####
def ise_select(): # Select Endpoint by MAC
    details = []
    ise_api = "endpoint/name/{}".format(search)
    ise_url = "https://{}:{}{}".format(ise_host, ise_api)
    response = requests.request("GET", ise_url, auth=HTTPBasicAuth(ers_admin, ers_pwd),
                                headers=headers, data=payload, verify=False)
    body = response.text
    endpoint_id = json.loads(body)["ERSEndPoint"]
    endpoint_details = ((endpoint_id["id"]),(endpoint_id["name"]),(endpoint_id["mac"], (endpoint_id["staticGroupAssignment"])))
    return endpoint_details
####
def numbered_menu(items): # Create menu options. Result is a dictionary of each endpoint, and a dictionary of the number of endpoints!
    x = 1
    y = 0
    numbers = []
    new_menu = []
    for item in items:
        y = y + x
        numbers.append(int(y))
        new_menu.append(str(y) + ". " + item + "\r")
    menu_dict = dict(zip(numbers, items))
    return menu_dict, new_menu
####
def bulleted_menu(items): # Create menu options. Result is a dictionary of each endpoint, and a dictionary of the number of endpoints!
    new_menu = []
    for item in items:
        new_menu.append("- " + item + "\r")
    return new_menu
####
def menu_selection(selection, string, dict): # Define the logic behind the menu choices. Here we match the numeric value of your menu choice to the dictionary key of each site we created earlier. 
    max = len(string)
    min = 1
    add = range(min, max+1)
    total = []
    for i in add:
        total.append(i)
    # List comprehension
    numbers = [ int(x) for x in total]
    menu_loop=True
    while  menu_loop:  ## While loop which will keep going until loop = False   
        print(67 * "-")
        for number in numbers:
            if selection in numbers: 
                choice = dict[selection] #United States
                print(choice + " has been selected")
                print(67 * "-")
                print("Pulling data from ISE... ")
                print(67 * "-")
                return choice
                ## You can add your code or functions here
            elif selection == 0:
                menu_loop == False # This will make the while loop to end as not value of loop is set to False
                print("Exit has been selected")
                return exit()
            else:
                # Any integer inputs other than values 1-5 we print an error message
                input("Wrong option selected. Enter any key to try again..")
####
def endpoint_details(mac): # Search Endpoint by MAC and dump the available options on screen.
    ise_url = ise_api("endpoint/name/{}".format(mac))
    response = requests.request("GET", ise_url, auth=HTTPBasicAuth(ers_admin, ers_pwd),
                                headers=headers, data=payload, verify=False)
    body = response.text
    endpoint_details = json.loads(body)["ERSEndPoint"]
    for x in endpoint_details:
        endpoint_uuid = endpoint_details["id"]
        break
    return endpoint_uuid
####
def ip_search(ip_str): # Search Endpoint by MAC and dump the available options on screen.

    ise_api = "/admin/API/mnt/Session/ActiveList"
    ise_url = "https://{}{}".format(ise_host, ise_api)
    skip = (None, b'', u'', '{}', 'null')
    response = requests.request("GET", ise_url, auth=HTTPBasicAuth(cli_admin, cli_pwd),
                                headers=api_headers, data=payload, verify=False)
    root = ET.fromstring(response.text)
    radius_data = []
    radius_headers = []
    elements_str = ('framed_ip_address')    
    for element in root.iter():
        for item in elements_str:
            if item in str(element):
                radius_data.append(element.text)
                radius_headers.append(item)
    print(radius_data)
    print(radius_headers)

#f or element in root.iter():
#f           for item in elements_str:
#f               if item in str(element): 
#f                   if 'orig_calling_station_id' in str(element):
#f                       pass
#f                   else:
#f                       radius_data.append(element.text)
#f                       radius_headers.append(item)
#f                               # want to see all available element names? just iterate through tree with
#f                               # for element in tree.iter():
#f                               #   print(element)      
#f       session_dict = dict(zip(radius_headers, radius_data))


####
def endpoint_session(mac, id): # Search Endpoint by MAC and dump the available options on screen.
    ise_api = "/admin/API/mnt/Session/MACAddress/{}".format(mac)
    ise_url = "https://{}{}".format(ise_host, ise_api)
    skip = (None, b'', u'', '{}', 'null')
    response = requests.request("GET", ise_url, auth=HTTPBasicAuth(cli_admin, cli_pwd),
                                headers=api_headers, data=payload, verify=False)
    if response.content in skip:
        print("No active sessions available for this endpoint!")
        return False
    elif response.content not in skip:
        root = ET.fromstring(response.text)
        radius_data = []
        radius_headers = []
        elements_str = ('cts_security_group', 'endpoint_policy', 'acs_server','framed_ip_address', 'location', 'nas_port_id', 'vlan', 'user_name', 'identity_group', 'network_device_name', 'calling_station_id', 'authentication_method', 'authentication_protocol')
        for element in root.iter():
            for item in elements_str:
                if item in str(element): 
                    if 'orig_calling_station_id' in str(element):
                        pass
                    else:
                        radius_data.append(element.text)
                        radius_headers.append(item)
                                # want to see all available element names? just iterate through tree with
                                # for element in tree.iter():
                                #   print(element)      
        session_dict = dict(zip(radius_headers, radius_data))
        session_list = []
        print("Active session details for {}".format(mac))
        print(67 * " ")
        for x,y in session_dict.items():
            print("{}: {}".format(x,y))
            session_list.append("{}: {}".format(x,y))
        print("unique identifier: " + id)
        print(67 * "-")
        session_menu = bulleted_menu(session_list)
        print(session_menu)
        session_string = (''.join(map(str, session_menu)))
        return session_string, session_dict, session_list
####
def quarantine_policies():
    ise_api = "ancpolicy"
    ise_url = "https://{}:{}{}".format(ise_host, ise_ers, ise_api)
    response = requests.request("GET", ise_url, auth=HTTPBasicAuth(ers_admin, ers_pwd),
                                headers=headers, data=payload, verify=False)
    details = []
    reply = response.text
    quarantine_options = json.loads(reply)["SearchResult"]["resources"]
    for policy in quarantine_options:
        details.append(policy["id"])
    return details
####    
def anc_assign():
    anc_available = ('Assign a Policy', 'Revoke a Policy', 'Check Policy Status')
    anc_list = numbered_menu(anc_available)[1]
    anc_dictionary = anc_list[0]
    anc_string = (''.join(map(str, anc_list)))
    return anc_string, anc_dictionary, anc_list
####
def anc_uuid(mac):
    ise_url = ise_api("ancendpoint")
    response = requests.request("GET", ise_url, auth=HTTPBasicAuth(ers_admin, ers_pwd),
                                headers=headers, data=payload, verify=False)
    reply = response.text
    status = json.loads(reply)["SearchResult"]["resources"]
    anc_ids = []
    anc_status_list = []
    anc_status_mac = []
    anc_status_details = []
    for x in status:
        anc_ids.append(x["id"])
    for id in anc_ids:
        ise_url = ise_api("ancendpoint/{}".format(id))
        response = requests.request("GET", ise_url, auth=HTTPBasicAuth(ers_admin, ers_pwd),
                                headers=headers, data=payload, verify=False)
        reply = response.text
        anc_status_full = json.loads(reply)
        anc_status_details.append(anc_status_full)
        anc_status_mac.append(anc_status_full["ErsAncEndpoint"]["macAddress"])

        #stopped here
    anc_status = []
    if mac in anc_status_mac:
        for x in anc_status_details:
            if mac in x["ErsAncEndpoint"]["macAddress"]:
                anc_status.append(x["ErsAncEndpoint"]["macAddress"])
                anc_status.append(x["ErsAncEndpoint"]["policyName"])
                anc_id = x["ErsAncEndpoint"]["id"]
        ise_url = ise_api("ancendpoint/{}".format(anc_id))
        response = requests.request("GET", ise_url, auth=HTTPBasicAuth(ers_admin, ers_pwd),
                                headers=headers, data=payload, verify=False)
        anc_status_reply = response.text
        status_response = json.loads(anc_status_reply)
        for x in status_response:
            anc_status_list.append(str("Endpoint ID: " + status_response["ErsAncEndpoint"]["macAddress"]))
            anc_status_list.append(str("ANC Status: " + status_response["ErsAncEndpoint"]["policyName"]))
        anc_status_menu = bulleted_menu(anc_status_list)
        print(anc_status_menu)
        anc_status_string = (''.join(map(str, anc_status_menu)))
        print(anc_status_string)
        return anc_status_string
    elif mac not in anc_status_mac:
        print("Don't see it")
        return None


def quarantine_assign():  
    quarantine_available = quarantine_policies()
    quarantine_list = numbered_menu(quarantine_available)
    quarantine_dictionary = quarantine_list[0]
    quarantine_string = (''.join(map(str, quarantine_list[1])))
    return quarantine_string, quarantine_dictionary, quarantine_list
####
def search_pick(pick):
    search_dictionary = numbered_menu(pick)[0]
    search_list = numbered_menu(pick)[1]
    search_string = (''.join(map(str, search_list)))
    return search_string, search_dictionary, search_list
####
def act_pick():
    act_dictionary = {1: "Get Active Session Details", 2: "ANC Policy Menu", 3:"Change of Authorization Menu"}
    act_list= [1, "Get Active Session Details", 2, "ANC Policy Menu", 3, "Change of Authorization Menu"]
    act_string = ("1. Get Active Session Details\r2. ANC Policy Menu\r3. Change of Authorization Menu")
    return act_string, act_dictionary, act_list
####
def quarantine_put(policy, mac):
    mac.strip("")
    if policy==2:
        payload="{\r\n  \"OperationAdditionalData\" : {\r\n    \"additionalData\" : [ {\r\n      \"name\" : \"macAddress\",\r\n      \"value\" : \"" + mac + "\"} ]\r\n  }\r\n}\r\n"
        ise_url = ise_api("ancendpoint/clear")
        response = requests.request("PUT", ise_url, auth=HTTPBasicAuth(ers_admin, ers_pwd),
                                headers=headers, data=payload, verify=False)
        if response.status_code == 204:
            print("ANC policy revoked successfully!")
        else:
            print("ANC policy revocation failed!")
    elif policy!=2:
        payload="{\r\n  \"OperationAdditionalData\" : {\r\n    \"additionalData\" : [ {\r\n      \"name\" : \"macAddress\",\r\n      \"value\" : \"" + mac + "\"},\r\n    {\r\n       \"name\" : \"policyName\",\r\n      \"value\" : \"" + policy + "\"\r\n    } ]\r\n  }\r\n}\r\n"
        ise_url = ise_api("ancendpoint/apply")
        response = requests.request("PUT", ise_url, auth=HTTPBasicAuth(ers_admin, ers_pwd),
                                headers=headers, data=payload, verify=False)
        if response.status_code == 204:
            print("ANC policy applied successfully!")
        else:
            print("ANC policy failed to apply!")
####
def coa_assign():
    coa_available = ('Reauth', 'Port Bounce')
    coa_create = numbered_menu(coa_available)
    coa_dictionary = coa_create[0]
    coa_list = coa_create[1]
    coa_string = search_string = (''.join(map(str, coa_list)))
    return coa_string, coa_dictionary, coa_list
####
def coa_get(coa, mac):
    if coa==1:
        #ise_url = ise_api("admin/API/mnt/CoA/Reauth/NGN-BL-ISE1/{}/0".format(mac))
        ise_api = "/admin/API/mnt/CoA/Reauth/NGN-BL-ISE1/{}/0".format(mac)
        ise_url = "https://{}{}".format(ise_host, ise_api)
        print(ise_url)
        response = requests.request("GET", ise_url, auth=HTTPBasicAuth(cli_admin, cli_pwd),
                            headers=api_headers, verify=False)
        if response.status_code == 200:
            print("CoA Reath applied successfully!")
            print(response.text)
            return True
        else:
            print("CoA Reath failed!")
            return False
    elif coa==2:
        ise_api = "/admin/API/mnt/CoA/Disconnect/NGN-BL-ISE1/{}/0".format(mac)
        ise_url = "https://{}{}".format(ise_host, ise_api)
        print(ise_url)
        response = requests.request("GET", ise_url, auth=HTTPBasicAuth(cli_admin, cli_pwd),
                                headers=headers, data=payload, verify=False)
        if response.status_code == 200:
            print("CoA Reath applied successfully!")
            print(response.text)
            return True    
        else:
            print("CoA Port bounce failed!")
            print(response.text)
            return False
