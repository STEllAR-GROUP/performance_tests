#! /usr/bin/env python

import json
import jsonschema

import os

def validate(test_file, v):
    print "Validating '" + test_file + "' ..."

    with open(test_file) as f:
        test_data = json.load(f)
    
     
    errors = sorted(v.iter_errors(slaves), key=lambda e: e.path)
    
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
    with open('test_data.schema.json') as f:
        test_schema = json.load(f)
    test_validator = jsonschema.Draft3Validator(test_schema)
        
    for data in os.listdir('test_data'):
        if data.endswith('.json'):
            validate(data, test_validator)
