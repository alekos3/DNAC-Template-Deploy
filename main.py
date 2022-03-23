#!/usr/bin/env python3
#Alexios Nersessian

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

#get Auth token and save in environment variable
env['token'] = getAuthToken(env)
x=0
platform_Id =''

if __name__ == "__main__":

    #List all platforms
    all_platforms = get_Dnac_Devices(env)
    platforms = []
    count = 0
    print("List of all Platform IDs available to deploy on")
    #print(all_platforms[0]['platformId'])

    for i in range(len(all_platforms)):
        if all_platforms[i]['platformId'] not in platforms:
            platforms.append(all_platforms[i]['platformId'])
            print(platforms[i-count])
        else:
            count += 1
    while True:
        platChoice = input("Please enter the platform you wish to deploy on:")
        if platChoice not in platforms:
            print(f"{bcolors.FAIL}Bad choice!!!{bcolors.ENDC}\n")
            continue
        else:
            confPlat = input(f"Confirm Platform y/n {platChoice} ")
            if confPlat == 'y':
                platform_Id = {'platformId': platChoice}
                break
            elif confPlat =='n':
                continue
            else:
                print(f'{bcolors.FAIL}Bad choice!!!{bcolors.ENDC}')
    #for x in range(len(all_platforms)):
    #    print(all_platforms[x])

    print()
    print()

    # Select project
    project = get_Project_names(env)
    select_project = ''
    row_length = 3
    for row in [project[i:i + row_length] for i in range(0, len(project), row_length)]:
        print(row)
    print()
    while select_project != 'q' and select_project not in project:
        select_project = input('Please select a project name:')
        if select_project not in project and select_project != 'q':
            print("Not a valid Project name! q to quit")
        elif select_project == 'q':
            break

    print()
    print()

    #Select Template
    if select_project != 'q':
        template = get_Template_ID(env, select_project) #Get template ID

        for i in range(0,len(template),2):
            print(x, template[i], "Template ID:", template[i+1])
            x+=1

    print()


    while select_project != 'q':

        print(f"{bcolors.OKGREEN}Please Select a template to deploy 0-{x - 1}{bcolors.ENDC}")

        selection = int(input())
        convertSelection = selection + selection + 1  # Convert to proper index in list to pull correct ID
        yeorne = input(f"Are you sure you want to deploy {bcolors.WARNING}{template[convertSelection-1]}{bcolors.ENDC}? y or n\nq to quit")


        if yeorne == "y":
            devices = get_Devices_By_Platform(env, platform_Id)
            group_size = 2 #group size must be below 100, 40-50 is recommended per API call.
            groups = [devices[x:x + group_size] for x in
                      range(0, len(devices), group_size)]  # break down list to groups of X devices
            for i in range(len(groups)):
                print(groups[i])
                deploy_Template(env, template[convertSelection], groups[i])  # Template ID is the second parameter
            #print(template[convertSelection])
            break
        elif yeorne == 'q':
            break
        else:
            continue

