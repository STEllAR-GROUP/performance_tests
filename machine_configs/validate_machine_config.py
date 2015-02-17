#! /usr/bin/env python

import json
import jsonschema

import os
import sys

def validate(test_file, v):
    print "Validating '" + test_file + "' ..."

    with open(test_file) as f:
        test_data = json.load(f)
    
     
    errors = sorted(v.iter_errors(test_data), key=lambda e: e.path)
    
    if len(errors) == 0:
        return
#        print "'" + test_file + "' is valid."
#        print
#        return   
 
    print "'" + test_file + "' is not valid!"
    print
    
    for error in errors:
        print(error)
        
    exit(1)

if __name__ == "__main__":
    scriptpath = os.path.dirname(os.path.realpath(__file__))

    with open(scriptpath + os.sep + 'machine_config.schema.json') as f:
        test_schema = json.load(f)
    test_validator = jsonschema.Draft3Validator(test_schema)
     
    if len(sys.argv) < 2:
        print("Usage:")
        print("\t" + sys.argv[0] + " <jsonfiles>")
        print("")
        exit(1)

    for i in range(1,len(sys.argv)):
        validate(sys.argv[i], test_validator)
