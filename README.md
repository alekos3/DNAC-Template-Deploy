# DNAC-Deploy
Deploy templates 

This script allows you do deploy at scale by consuming the deploy API of DNAC. DNAC can deploy up to 100 devices per API call; On line 101 of the main.py you can set your group size. FYI The deploy API is rate limited to 100 calls per minute. So lets say we want to deploy 1000 devices if we set the group size to 100 then the script will make 10 API calls. DNAC does not wait for the deployement to be completed on each batch of devices so the script should run fairly quick.



1) Open the env.py file first and populate it with all the information for your DNAC (url, creds, version).
2) Run the main script from your IDE and a list of all available platforms to deploy on will be presented.
3) Copy and paste the desired platform to deploy on and hit Enter and confirm your choice.
4) Select a Project name that houses templates (copy/paste name of project)
5) Select a template to deploy. Templates are numbered on the left starting from 0-X (e.g enter 3 and press enter). Confirm choice y/n.
