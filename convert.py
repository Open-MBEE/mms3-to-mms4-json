#!/usr/bin/env python3

import json
import os
import sys

result = {"elements": []}
fullpath = sys.argv[1]

files = []

if os.path.isdir(fullpath):
    print("Processing directory " + fullpath)
    files = [os.path.join(fullpath, f) for f in os.listdir(fullpath) if os.path.isfile(os.path.join(fullpath, f))]
else:
    print("Processing file " + fullpath)
    files.append(fullpath)

print(files)

for filename in files:
    with open(filename, "r") as file:
        path, target = os.path.split(filename)
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

        new_full_path = os.path.join(new_path, target)

        print("Saving to: " + new_full_path)

        with open(new_full_path, "w") as outfile:
            json.dump(result, outfile)
