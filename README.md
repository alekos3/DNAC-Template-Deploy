# DNAC-Template-Deploy
Deploy templates 

This script allows you to deploy at scale by consuming the deploy API of DNAC. DNAC can deploy up to 100 devices per API call; On line 39 of the main.py you can set your group size (1 to 100) by changing the integer value of the group_size variable. Lets say we want to deploy a template across 1000 devices; if we set the group size to 100 then the script will make a total of 10 API calls (10 groups of 100). FYI The deploy API is rate limited to 100 calls per minute.



1) Check Requirements.txt for library dependencies.
2) Run the main.py script from terminal or your favorite IDE. You will be prompted for the DNAC URL, username and password.
   Look at screenshot below for correct format on URL.


![dnaclogin](https://user-images.githubusercontent.com/79263622/163636037-d847fd9d-19b2-460c-bb51-6625c856dd9d.jpg)


4) Enter Platform to deploy on exactly as it appears in DNAC GUI and hit Enter and confirm your choice OR just press Enter to deploy to all inventory in Catalyst Center (DNAC).



6) Select a Project name that houses templates. Projects are numbered on the left starting from 0-X (e.g enter 3 and press enter). Confirm your choice y/n.


![project](https://user-images.githubusercontent.com/79263622/163638432-504d367a-be86-4386-b96e-2f0385574340.jpg)


8) Select a Template to deploy. Templates are numbered on the left starting from 0-X (e.g enter 3 and press enter). Confirm choice y/n.


![tempid](https://user-images.githubusercontent.com/79263622/163641564-47312877-2a93-4227-9fed-18623cecb618.jpg)

9) Run check_status.py for detailed results.


[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/alekos3/DNAC-Deploy)

