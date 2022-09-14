#!/usr/bin/env python3

import json
import os
import sys
import requests
import getpass

user_name = input("Username: ")

while True:
    user_pass = getpass.getpass(prompt="Password: ")
    break

sys.argv.pop(0)
projects = sys.argv
ref_id = "master"

extracted_directory = "extracted"

if not os.path.exists(extracted_directory):
    print("Creating new directory: " + extracted_directory)
    os.makedirs(extracted_directory)

for project_id in projects:
    temp = '''
        https://{user_name}:{user_pass}@opencae.jpl.nasa.gov/alfresco/service/projects/{project_id}/refs/{ref_id}/elements
    '''.strip()

    if project_id:
        url = temp.format(user_name=user_name, user_pass=user_pass, project_id=project_id, ref_id=ref_id)
        x = requests.get(url)

        response = json.dumps(json.loads(x.text), indent=4)
        filename = "{extracted}/{project_id}-{ref_id}.json".format(
            extracted=extracted_directory,
            project_id=project_id,
            ref_id=ref_id)
        with open(filename, "w") as outfile:
            outfile.write(response)
        print("File extracted to {filename}".format(filename=filename))
