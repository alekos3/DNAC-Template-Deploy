# DNAC-Deploy
Deploy templates 

This script allows you to deploy at scale by consuming the deploy API of DNAC. DNAC can deploy up to 100 devices per API call; On line 101 of the main.py you can set your group size. Lets say we want to deploy a template accross 1000 devices if we set the group size to 100 then the script will make 10 API calls (10 groups of 100). DNAC does not wait for the deployement to be completed (asynchromous API) on each batch of devices so the script should run fairly quick. FYI The deploy API is rate limited to 100 calls per minute.



1) Check Requirements.txt for library dependencies.
2) Run the main.py script from terminal or your favorite ID. You will be prompted for the DNAC URL, username and password.
   Look at screenshot below for correct format on URL.


![dnaclogin](https://user-images.githubusercontent.com/79263622/163636037-d847fd9d-19b2-460c-bb51-6625c856dd9d.jpg)


4) Select Platform to deploy on and hit Enter and confirm your choice. Platforms are numbered on the left starting from 0-X (e.g enter 3 and press enter).
5) Select a Project name that houses templates. Projects are numbered on the left starting from 0-X (e.g enter 3 and press enter)
6) Select a Template to deploy. Templates are numbered on the left starting from 0-X (e.g enter 3 and press enter). Confirm choice y/n.
