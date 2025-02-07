#!/usr/bin/env python3
__author__ = "Alexios Nersessian"
__copyright__ = "Copyright 2025, Cisco"
__email__ = "anersess@cisco.com"
__version__ = "v2.0"

import csv
import getpass
import os
import re
import time
import urllib3

urllib3.disable_warnings()
from dnac import *


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def log_deploy_ids(deploy_ids):
    if deploy_ids:  # Check for empty list
        try:
            with open("jobid.id", "r") as read:
                jobid = int(read.readline())

        except FileNotFoundError:  # Creates jobid file and initializes it and creates deployids directory
            os.mkdir("./deployids")
            with open("jobid.id", "w") as f:
                f.write("1000")
            with open("jobid.id", "r") as read:
                jobid = int(read.readline())

        with open("jobid.id", "w") as f:
            jobid = jobid + 1
            strid = str(jobid)
            f.write(strid)
        print()
        print("Deploy ID file: ", f"deploy_ids_job{strid}.csv")

        ids = f"./deployids/deploy_ids_job{strid}.csv"  # CSV to store deploy IDs
        # Write Deployment ID(s) to file
        with open(ids, "a", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(deploy_ids)


def prepare_device_list_payload(device_list):
    api_structured_dev_list = []

    for item in device_list:
        api_structured_dev_list.append({"hostName": item["hostname"],
                                        "type": "MANAGED_DEVICE_UUID",
                                        "id": item["id"]})  # structure the list to the format of targetInfo

    return api_structured_dev_list


def extract_deploy_id_info(deploy_info):
    # Extract non-applicable targets
    non_applicable_match = re.search(r"nonApplicableTargets: \{(.+?)\}", deploy_info)
    non_applicable_targets = []
    if non_applicable_match:
        non_applicable_list = non_applicable_match.group(1).split(", ")
        for item in non_applicable_list:
            device_id, _ = item.split("=")
            non_applicable_targets.append(device_id)

    return non_applicable_targets, deploy_info.split()[-1]


def create_device_mapping(raw_devices):
    uuid_to_hostname = {}

    for device in raw_devices:
        uuid_to_hostname[device["instanceUuid"]] = device["hostname"]

    return uuid_to_hostname


def project_menu(projects):
    count_proj = 0
    project_list = []

    # Print available projects
    for proj in projects:
        print(f"{count_proj} - {proj}")
        project_list.append(proj)
        count_proj += 1

    while True:
        try:
            index = int(input(f"{bcolors.OKGREEN}Please select a project 0 - {count_proj - 1}:  {bcolors.ENDC}"))
            project = project_list[index]
            yeorne = input(f"{bcolors.WARNING}Are you sure? y/n {project}:   {bcolors.ENDC}")

            if yeorne.lower() == "y":
                return project
            elif yeorne.lower() == "q":
                return "q"
            else:
                continue
        except:
            print(f"{bcolors.FAIL}\nNot a valid selection!\n {bcolors.ENDC}")

    return project


def template_menu(templates):
    for i in range(len(templates)):
        print(i, "-", templates[i][0], "|  Template ID:", templates[i][1])

    print()

    while True:
        print()
        try:
            temp_select = int(input(
                f"{bcolors.OKGREEN}Please Select a template to deploy 0-{len(templates) - 1}{bcolors.ENDC}: "))
            if len(templates) >= temp_select >= 0:
                template_id = templates[temp_select][1]
                template_name = templates[temp_select][0]
                yeorne = input(
                    f"Are you sure you want to deploy {bcolors.WARNING}{template_name}{bcolors.ENDC}? y or n\nq to quit:  ")
                if yeorne == "y":
                    return template_id
                elif yeorne == "q":
                    return "q"
                else:
                    continue
            else:
                print(f"{bcolors.FAIL}Invalid choice!!!{bcolors.ENDC}")
                continue
        except:
            print(f"{bcolors.FAIL}Invalid choice!!!{bcolors.ENDC}")
            continue


def main():
    # get Auth token and save in environment variable
    env = {}
    # get Auth token and save in environment variable
    env["base_url"] = input("Enter Catalyst Center URL:  ").strip("/")
    env["username"] = input("Username: ")
    env["password"] = getpass.getpass()
    env["token"] = get_auth_token(env)

    platform_choice = input("Enter a platform to deploy template to, or press enter for all inventory:  ")

    raw_device_list = get_device_list(env, platform_choice)
    uuid_to_name = create_device_mapping(raw_device_list)
    device_list = prepare_device_list_payload(raw_device_list)
    group_size = 40  # group size must be below 100.

    print()
    print()

    # Project selection menu
    projects = get_project_names(env)
    project = project_menu(projects)
    if project == "q":
        print("Goodbye!")
        return

    print()
    print()

    # Select Template
    deploy_id_list = []
    templates = get_template_id(env, project)  # Get template ID
    template_id = template_menu(templates)

    if template_id == "q":
        print("Goodbye!")
        return

    # break down list to groups of X devices
    groups = [device_list[x:x + group_size] for x in range(0, len(device_list), group_size)]

    # Deploy template
    for i in range(len(groups)):
        deploy_info = deploy_template(env, template_id, groups[i])
        non_applicable_targets, deploy_id = extract_deploy_id_info(deploy_info)
        deploy_id_list.append([deploy_id])
        time.sleep(1)

    log_deploy_ids(deploy_id_list)

    if non_applicable_targets:
        print("\n" + "=" * 80)
        print(
            f"Failed to Start Deployment Process for {len(non_applicable_targets)} devices, as they are non applicable.")
        print("=" * 80)
        for dev_id in non_applicable_targets:
            print(uuid_to_name.get(dev_id))

    print()
    print("Deploy Job information has been saved. Please run check_status.py for detailed results.")
    print("Done!")


if __name__ == "__main__":
    main()
