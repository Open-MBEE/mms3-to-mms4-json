# MMS3 to MMS4 JSON Transformation Script
This is a simple Python3 script to transform JSON extracted from MMS3 to be imported to MMS4. 

## What it does
All attributes generated by MMS3 are removed. This is essentially all attributes which start with an underscore ("_") aside from "_contents" and "_appliedStereotypeIds".

## To run
```shell
./convert.py PATH/FILENAME
```
OR
```
python convert.py PATH/FILENAME
```
This will create a new file in a new directory called "processed" in the given path of the file.