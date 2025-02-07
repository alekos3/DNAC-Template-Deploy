#!/usr/bin/env python3
__author__ = "Alexios Nersessian"
__copyright__ = "Copyright 2025, Cisco"
__email__ = "anersess@cisco.com"
__version__ = "v2.0"
import requests


def get_auth_token(env):
    url = "{}/dna/system/api/v1/auth/token".format(env["base_url"])
    # Make the POST Request
    response = requests.post(url, auth=(env["username"], env["password"]), verify=False)

    # Validate Response
    if "error" in response.text:
        print("ERROR: Failed to retrieve Access Token!")
        print("REASON: {}".format(response.json()["error"]))

    else:
        return response.json()["Token"]  # return only the token


def get_device_list(env, platform_id=None):
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    device_list = []
    offset = 1
    limit = 500  # Do NOT exceed 500 as the limit (Per CC documentation)

    while True:
        if platform_id:
            url = f"{env['base_url']}/dna/intent/api/v1/network-device?platformId={platform_id}&offset={offset}&limit={limit}"
        else:
            url = f"{env['base_url']}/dna/intent/api/v1/network-device?&offset={offset}&limit={limit}"
        response = requests.get(url, headers=headers, verify=False)

        if response.json().get("response"):
            device_list.extend(response.json()["response"])
            offset += limit
        else:
            break
    return device_list


def get_project_names(env):
    url = "{}/dna/intent/api/v1/template-programmer/template".format(env["base_url"])
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, verify=False)
    project = []

    for line in response.json():
        if line["projectName"] not in project:
            project.append(line["projectName"])

    return project


def get_template_id(env, project):
    url = "{}/dna/intent/api/v1/template-programmer/template".format(env["base_url"])
    templates = []
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, verify=False)

    for line in response.json():
        if project in str(line):  # Get template ID from desired project
            templates.append((dict(line)["name"], dict(line)["templateId"]))

    return templates


def deploy_template(env, template_id, devices):
    url = f"{env['base_url']}/dna/intent/api/v1/template-programmer/template/deploy"
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
    }

    payload = {
        "forcePushTemplate": True,
        "targetInfo": devices,
        "templateId": template_id
    }

    # Make POST request
    response = requests.post(url, headers=headers, json=payload, verify=False)

    return response.json().get("deploymentId")


def get_task(env, task_id):
    url = "{}/dna/intent/api/v1/task/{}".format(env["base_url"], task_id)
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
    }

    # Make GET request
    response = requests.get(url, headers=headers, verify=False)

    return response.json()  # return response with information about specific task


def check_deployment_status(env, deployment_id):
    url = f"{env['base_url']}/dna/intent/api/v1/template-programmer/template/deploy/status/{deployment_id}"
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers, verify=False)

    return response.json()["devices"]  # return the deployment status


def get_device_info_by_id(env, dev_id):
    url = f"{env['base_url']}/dna/intent/api/v1/network-device/{dev_id}/"

    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.request("GET", url, headers=headers, verify=False)

    return response.json()


def create_tag(env, name):
    url = f"{env['base_url']}/dna/intent/api/v1/tag"

    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {"name": name}

    response = requests.request("POST", url, headers=headers, json=payload, verify=False)

    return response.status_code


def get_tag_id(env, name):
    url = f"{env['base_url']}/dna/intent/api/v1/tag"

    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    params = {"name": name}
    response = requests.request("GET", url, headers=headers, params=params, verify=False)

    return response.json()["response"][0]["id"]


def tag_add_member(env, tag_id, members):
    url = f"{env['base_url']}/dna/intent/api/v1/tag/{tag_id}/member"

    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {"networkdevice": members}
    response = requests.request("POST", url, headers=headers, json=payload, verify=False)

    return response.status_code


def get_device_id(env, name):
    dev_list = []
    url = f"{env['base_url']}/dna/intent/api/v1/device-detail"
    headers = {
        "x-auth-token": env["token"],
        "Content-Type": "application/json",
        "Accept": 'application/json'
    }

    for device in name:
        params = {"searchBy": device[0], "identifier": "nwDeviceName"}
        dev = requests.get(url, headers=headers, params=params, verify=False)
        dev_list.append(dev.json()["response"]["nwDeviceId"])

    return dev_list
