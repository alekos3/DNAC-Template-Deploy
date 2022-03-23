#!/usr/bin/env python3

import requests
import time
import pprint
import urllib3
urllib3.disable_warnings()


def getAuthToken(env):
    """
	Intent-based Authentication API call
	The token obtained using this API is required to be set as value to the X-Auth-Token HTTP Header
	for all API calls to Cisco DNA Center.
	:param env:
	:return: Token STRING
	"""
    url = '{}/dna/system/api/v1/auth/token'.format(env['base_url'])
    # Make the POST Request
    response = requests.post(url, auth=(env['username'], env['password']), verify=False)

    # Validate Response
    if 'error' in response.json():
        print('ERROR: Failed to retrieve Access Token!')
        print('REASON: {}'.format(response.json()['error']))

    else:
        return response.json()['Token']  # return only the token

def get_Devices_By_Platform(env, platform_Id):
    url = '{}/dna/intent/api/v1/network-device'.format(env['base_url'])
    headers = {
        'x-auth-token': env['token'],
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    devList = []
    query_string_params = platform_Id# GET Target Devices from env file
    response = requests.get(url, headers=headers,
                            params=query_string_params, verify=False)
    for item in response.json()['response']:
        devList.append({'hostName':item['hostname'],'type': 'MANAGED_DEVICE_UUID','id':item['id']})#structure the list to the format of targetInfo

    return devList

def get_Dnac_Devices(env):
    url = '{}/dna/intent/api/v1/network-device'.format(env['base_url'])
    headers = {
        'x-auth-token': env['token'],
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    # Make the GET Request
    response = requests.get(url, headers=headers, verify=False)

    # Validate Response
    if 'error' in response.json():
        print('ERROR: Failed to retrieve Network Devices!')
        print('REASON: {}'.format(response.json()['error']))
        return []
    else:
        return response.json()['response']  # return the list of dnac devices

    # Need the response to check task progress
    return response


def get_Project_names(env):
    url = "{}/dna/intent/api/v1/template-programmer/template".format(env["base_url"])
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, verify=False)
    project = []

    for line in response.json():
        if line['projectName'] not in project:
            project.append(line['projectName'])

    return project


def get_Template_ID(env, project):
    url = "{}/dna/intent/api/v1/template-programmer/template".format(env["base_url"])
    template = []
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, verify=False)

    #print(json.dumps(response.json(), indent=4))
    for line in response.json():
        if project in str(line): #Get template ID from desired project
            template.append(dict(line)['name'])
            template.append(dict(line)['templateId'])

    return template

############BELOW IS THE DEPLOY TEMPLATE###############################
def deploy_Template(env, template_id, devices): #hostname, device_id,
    url = "{}/dna/intent/api/v1/template-programmer/template/deploy".format(env["base_url"])
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
    }
    #devices = json.loads(get_Devices_By_Platform(env))
    payload = {
        "targetInfo": devices, #within this variable we can pass up to 100 devices to be provisioned at once
        "templateId": template_id
    }

    # Make POST request
    response = requests.post(url, headers=headers, json=payload, verify=False)

    # Check deployment status
    if response.status_code == 200 or response.status_code == 202:
        pprint.pprint(response.json())

        if "not deploying" in response.json()["deploymentId"]:
            print("Device %s not applicable for deployment of template %s. Hence, not deploying" % (
                'hostname', template_id))
        else:
            print("Successfully deployed template %s to %s" % (template_id, 'hostname'))

            while True:
                if "IN_PROGRESS" == check_Deployment_Status(env,
                                                            response.json()["deploymentId"].partition(
                                                                "Template Deployemnt Id: ")[2]):
                    time.sleep(2)
                    continue
                else:
                    break

            return response.json()

    else:
        print("Did not deploy template %s to %s" % (template_id, response.status_code))#If failed show failed devices


def get_Task(env, task_id):
    url = "{}/dna/intent/api/v1/task/{}".format(env["base_url"], task_id)
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
    }

    # Make GET request
    response = requests.get(url, headers=headers, verify=False)

    return response.json()  # return response with information about specific task


# Need a way to check if deployment of template to device was successful
def check_Deployment_Status(env, deployment_id):
    url = "{}/dna/intent/api/v1/template-programmer/template/deploy/status/{}".format(env["base_url"], deployment_id)
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
    }

    # Make GET request
    response = requests.get(url, headers=headers, verify=False)
    pprint.pprint(response.json())

    return response.json()["devices"][0]["status"]  # return the deployment status

