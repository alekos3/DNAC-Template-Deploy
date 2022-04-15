#!/usr/bin/env python3
# Alexios Nersessian

from dnac import *
from env import *


######################################
# SCRIPT
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


######################################

# get Auth token and save in environment variable
env['token'] = getAuthToken(env)

if __name__ == "__main__":
    all_platforms = get_Dnac_Devices(env)
    platforms = []
    template_count = 0
    platform_Id = ''
    temp_select = -1
    count_plat = 0

    print("List of all Platform IDs available to deploy on")

    for i in range(len(all_platforms)):
        if all_platforms[i]['platformId'] not in platforms:
            platforms.append(all_platforms[i]['platformId'])
            print(count_plat, '-', all_platforms[i]['platformId'])
            count_plat += 1
        else:
            continue

    while True:
        try:
            platChoice = platforms[int(input("Please enter the platform you wish to deploy on:"))]
            confPlat = input(f"Confirm Platform y/n {platChoice} ")
            if confPlat == 'y':
                platform_Id = {'platformId': platChoice}
                break
            elif confPlat == 'n':
                continue
            else:
                print(f'{bcolors.FAIL}Bad choice!!!{bcolors.ENDC}')
        except:
            print(f"{bcolors.FAIL}\nNot a valid Choice!\n {bcolors.ENDC}")

    print()
    print()

    # Select project
    project = get_Project_names(env)
    select_project = ''
    count_proj = 0
    projectList = []

    for proj in project:
        print(f'{count_proj} - {proj}')
        projectList.append(proj)
        count_proj += 1

    while True:
        try:
            index = int(input(f'{bcolors.OKGREEN}Please select a project 0 - {count_proj - 1}:\n{bcolors.ENDC}'))
            select_project = projectList[index]
            yeorne = input(f"{bcolors.WARNING}Are you sure? y/n {select_project} {bcolors.ENDC}")
            break
        except:
            print(f"{bcolors.FAIL}\nNot a valid Project name!\n {bcolors.ENDC}")

    print()
    print()

    # Select Template
    if select_project != 'q':
        template = get_Template_ID(env, select_project)  # Get template ID

        for i in range(0, len(template), 2):
            print(template_count, '-', template[i], "|  Template ID:", template[i + 1])
            template_count += 1

    print()

    while select_project != 'q':
        print()

        try:
            temp_select = input(
                f"{bcolors.OKGREEN}Please Select a template to deploy 0-{template_count - 1}{bcolors.ENDC}: ")
            if int(temp_select) <= template_count and int(temp_select) >= 0:
                convertSelection = int(temp_select) + int(
                    temp_select) + 1  # Convert to proper index in list to pull correct ID
                yeorne = input(
                    f"Are you sure you want to deploy {bcolors.WARNING}{template[convertSelection - 1]}{bcolors.ENDC}? y or n\nq to quit")
                if yeorne == "y":
                    devices = get_Devices_By_Platform(env, platform_Id)
                    group_size = 50  # group size must be below 100, 40-50 is recommended per API call.
                    groups = [devices[x:x + group_size] for x in
                              range(0, len(devices), group_size)]  # break down list to groups of X devices

                    for i in range(len(groups)):
                        print(groups[i])
                        ###deploy_Template(env, template[convertSelection], groups[i])  # Template ID is the second parameter
                    # print(template[convertSelection])
                    break
                elif yeorne == 'q':
                    break
                else:
                    continue
            else:
                print(f'{bcolors.FAIL}Bad choice!!!{bcolors.ENDC}')
                continue
        except:
            print(f'{bcolors.FAIL}Bad choice!!!{bcolors.ENDC}')
            continue
