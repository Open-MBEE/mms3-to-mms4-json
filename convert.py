#!/usr/bin/env python3

import json
import os
import sys

result = {"elements": []}
fullpath = sys.argv[1]
path, filename = os.path.split(fullpath)

print("Processing " + filename)

with open(filename, "r") as file:
    data = json.load(file)

count = 0
added = 0
for d in data["elements"]:
    count += 1
    if d["id"].startswith("PROJECT") and not d["id"].endswith("_pm"):
        continue
    if "_contents" in d:
        new_element = {"_contents": d["_contents"], "id": d["id"]}
        result["elements"].append(new_element)
        added += 1
    elif d["id"].endswith("_pei") or d["id"].startswith("_hidden") or d["ownerId"].startswith("_hidden") or d["ownerId"].endswith("_pei") or d["ownerId"].startswith("view_instances_bin"):
        new_element = {}
        for key, value in d.items():
            if not key.startswith("_") or key == "_contents" or key == "_appliedStereotypeIds":
                new_element[key] = value
        result["elements"].append(new_element)
        added += 1

print("Finished processing " + str(count) + " elements")
print("Outputted " + str(added) + " elements")

new_path = os.path.join(path, "processed")
if not os.path.exists(new_path):
    print("Creating new directory: " + new_path)
    os.makedirs(new_path)

new_full_path = os.path.join(new_path, filename)

print("Saving to: " + new_full_path)

with open(new_full_path, "w") as outfile:
    json.dump(result, outfile)
