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
for d in data["elements"]:
    new_element = {}
    count += 1
    for key, value in d.items():
        if not key.startswith("_") or "_contents" in key or "_appliedStereotypeIds" in key:
            new_element[key] = value

    result["elements"].append(new_element)

print("Finished processing " + str(count) + " elements")

new_path = os.path.join(path, "processed")
if not os.path.exists(new_path):
    print("Creating new directory: " + new_path)
    os.makedirs(new_path)

new_full_path = os.path.join(new_path, filename)

print("Saving to: " + new_full_path)

with open(new_full_path, "w") as outfile:
    json.dump(result, outfile)
