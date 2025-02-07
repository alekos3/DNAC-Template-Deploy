#!/usr/bin/env python3
__author__ = "Alexios Nersessian"
__copyright__ = "Copyright 2025, Cisco"
__email__ = "anersess@cisco.com"
__version__ = "v2.0"

import csv
import getpass
import os
import time
import urllib3
from dnac import *

urllib3.disable_warnings()


def write_results(results_csv, failed_devs, success_devs):
    try:
        with open(results_csv, "w", newline="") as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Hostname", "Result", "Details"])

            # writing the data rows
            csvwriter.writerows(failed_devs)
            csvwriter.writerows(success_devs)

    except FileNotFoundError:
        os.mkdir("./results")
        with open(results_csv, "w", newline="") as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Hostname", "Result", "Details"])

            # writing the data rows
            csvwriter.writerows(failed_devs)
            csvwriter.writerows(success_devs)


def main():
    env = {}
    # get Auth token and save in environment variable
    env["base_url"] = input("Enter Catalyst Center URL:  ").strip("/")
    env["username"] = input("Enter your username:  ")
    env["password"] = getpass.getpass()
    env["token"] = get_auth_token(env)
    id_list = []
    yeorne = ""
    success_devs = []
    jobs = []
    failed_devs = []
    directory = "./deployids"
    count_deploy = 0

    print()

    # get template to deploy from file
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            print(f"{count_deploy} - {filename}")
            jobs.append(filename)
            count_deploy += 1
    print()
    while True:
        select = input(f"Select a job ID to check the status: Enter a choice from 0 to {count_deploy-1}: ")
        print()
        try:
            job_id = jobs[int(select)].partition("s_")[2]
            break

        except:
            print("Not a valid choice!")

    with open(f"{directory}/{jobs[int(select)]}", "r", newline="") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")

        for row in csv_reader:
            if row[0] != "deploying":
                id_list.append(row)

    for x in range(len(id_list)):
        status = check_deployment_status(env, id_list[x][0])
        for i in range(len(status)):

            while True:
                if "IN_PROGRESS" in status[i]["status"]:
                    time.sleep(1)  # Wait 1 Sec and recheck device status
                    status = check_deployment_status(env, id_list[x][0])
                else:
                    break

            if "SUCCESS" in status[i]["status"]:
                success_devs.append(
                    [get_device_info_by_id(env, status[i]["deviceId"])["response"]["hostname"], status[i]["status"],
                     status[i]["detailedStatusMessage"].split("Message:")[-1].replace("<br></pre>", "")])

            else:
                failed_devs.append(
                    [get_device_info_by_id(env, status[i]["deviceId"])["response"]["hostname"], status[i]["status"],
                     status[i]["detailedStatusMessage"].split("Message:")[-1].replace("<br></pre>", "")])

    results_csv = f"./results/results_{job_id}"

    if failed_devs or success_devs:
        write_results(results_csv, failed_devs, success_devs)

    if failed_devs:  # If there are any failed devices go ahead and ask user if they want to tag them
        while True:
            yeorne = input("Failed deployments have been detected! Tag failed devices? y/n:  ")

            if yeorne.lower() == "y":
                tag_name = input("Please give your tag a name:  ")  # Create custom tag for any potential failed devices
                create_tag(env, tag_name)
                tagid = get_tag_id(env, tag_name)
                devid = get_device_id(env, failed_devs)
                tag_add_member(env, tagid, devid)
                break
            elif yeorne.lower() == "n":
                break
            else:
                print("Invalid Choice!")

    print()
    print()

    if failed_devs or success_devs:
        print(f"Deployment status has been gathered for all devices.\nCheck {results_csv} file for results.")

    print(f"Total Successful devices: {len(success_devs)}")
    print(f"Total Failed devices: {len(failed_devs)}")
    print()

    if yeorne.lower() == "y":
        print(f"Failed Devices have been tagged with {tag_name} tag.")


if __name__ == "__main__":
    main()
