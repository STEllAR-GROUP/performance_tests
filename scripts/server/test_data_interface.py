import json
import jsonschema

import os
from sets import Set

# Create schema validator
with open('../../test_data.schema.json') as f:
    schema = json.load(f)
schema_validator = jsonschema.Draft3Validator(schema)


def get_filenames():
    filenames = []
    for path, subdirs, files in os.walk('../../test_data'):
        for testfile in files:
            if testfile.endswith('.json'):
                filenames.append(path + os.sep + testfile)
    return filenames
    
    

def validate_test_file(file_json, filename):
    errors = sorted(schema_validator.iter_errors(file_json), key=lambda e: e.path)
    if len(errors) != 0:
        print("ERROR: '" + filename + "' seems to be invalid!")
        print()
        for error in errors:
            print(error)
        exit(1)

def open_testfile(filename):
    # Open testfile json
    with open(filename) as f:
        file_json = json.load(f)

    # Validate testfile
    validate_test_file(file_json, filename)

    return file_json

def get_platform_name(build_config):
    platform_name = build_config['machine_name'] + ' ('                     \
                  + str(build_config['num_threads_per_locality']) + '/'     \
                  + str(build_config['num_localities_per_node']) + '/'      \
                  + str(build_config['num_nodes']) + ') - '                 \
                  + build_config['compiler'] + ' - '                        \
                  + build_config['boost'] + ' - '                           \
                  + build_config['allocator']
    return platform_name
 
def get_build_configs(file_content):
    return file_content['machine_configurations']    

def get_branch_name(build_config):
    return build_config['branch']

def get_hpx_commit_id(build_config):
    return build_config['hpx_commit_id']
 
def get_tests(build_config):
    return build_config['tests']

def get_test_name(test_data):
    full_test_name = test_data['test_name']

    params = test_data['additional_parameters']
    for key in sorted(params.keys()):
        param = params[key]
        full_test_name = full_test_name + ' '   \
                       + str(key) + "=" + str(param)

    return full_test_name

def get_test_time(test_data):
    return test_data['timestamp']

def get_test_result(test_data):
    return test_data['result']
   
platform_names = Set()
branches = Set()
test_names = Set()

def read_test_file_roughly(filename):
    print("Reading '" + filename + "' ...")

    file_json = open_testfile(filename)

    # Read file to tables
    build_configs = file_json['machine_configurations']
    for build_config in build_configs:
        # generate platform name from config
        platform_name = get_platform_name(build_config)
        platform_names.add(platform_name)

        branch = build_config['branch']
        branches.add(branch)

        tests = build_config['tests']
        for test in tests:
            test_name = get_test_name(test)
            test_names.add(test_name)

def read_test_data_roughly():

    platform_names.clear()

    for filename in get_filenames():
        read_test_file_roughly(filename)



