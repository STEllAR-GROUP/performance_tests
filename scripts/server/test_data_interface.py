import json
import jsonschema

import os
from sets import Set

platform_names = Set()
branches = Set()
test_names = Set()

def generate_platform_name(machine_name, compiler, boost, allocator):
    platform_name = machine_name + ' - '    \
                  + compiler + ' - '        \
                  + boost + ' - '           \
                  + allocator
    return platform_name
 
def generate_test_name(short_test_name, threads_per_locality, localities_per_node, nodes, params):
    full_test_name = short_test_name + ' '              \
                   + str(threads_per_locality) + '/'    \
                   + str(localities_per_node) + '/'     \
                   + str(nodes)

    for key in sorted(params.keys()):
        param = params[key]
        full_test_name = full_test_name + ' '   \
                       + key + "=" + param

    return full_test_name
    

def validate_test_file(file_json, filename, validator):
    errors = sorted(validator.iter_errors(file_json), key=lambda e: e.path)
    if len(errors) != 0:
        print("ERROR: '" + filename + "' seems to be invalid!")
        print()
        for error in errors:
            print(error)
        exit(1)

    

def read_test_file_roughly(filename, validator):
    print("Reading '" + filename + "' ...")

    # Open testfile json
    with open(filename) as f:
        file_json = json.load(f)

    # Validate testfile
    validate_test_file(file_json, filename, validator)

    # Read file to tables
    build_configs = file_json['build_configurations']
    for build_config in build_configs:
        # generate platform name from config
        platform_name = generate_platform_name(build_config['machine_name'],    \
                                               build_config['compiler'],        \
                                               build_config['boost'],           \
                                               build_config['allocator'])
        platform_names.add(platform_name)
        branch = build_config['branch']
        branches.add(branch)
        tests = build_config['tests']
        for test in tests:
            test_name = generate_test_name(test['test_name'],                   \
                                           test['num_threads_per_locality'],    \
                                           test['num_localities_per_node'],     \
                                           test['num_nodes'],                   \
                                           test['additional_parameters'])
            test_names.add(test_name)

def read_test_data_roughly():
    with open('../../test_data.schema.json') as f:
        schema = json.load(f)

    schema_validator = jsonschema.Draft3Validator(schema)

    platform_names.clear()

    for path, subdirs, files in os.walk('../../test_data'):
        for testfile in files:
            if testfile.endswith('.json'):
                read_test_file_roughly(path + os.sep + testfile, schema_validator)



