import json
import jsonschema

import subprocess

import os
from sets import Set

repo_path = ""

schema_validator = {}

def set_repo_path(path):
    global repo_path
    global schema_validator
    
    repo_path = path

    # Create schema validator
    with open(repo_path + os.sep + 'test_data.schema.json') as f:
        schema = json.load(f)
    schema_validator = jsonschema.Draft3Validator(schema)


set_repo_path(os.path.dirname(os.path.realpath(__file__)) + os.sep + ".."       \
                                                          + os.sep + "..")
def get_current_commit():
    p = subprocess.Popen(["git", "rev-parse", "--verify", "HEAD"],
                         cwd=repo_path,
                         stdout=subprocess.PIPE)
    out,err = p.communicate()
    if p.returncode:
        print("Error: Can't fetch current commit id of data repository!")
        exit(1)
    return out.strip()


def get_filenames():
    filenames = []
    for path, subdirs, files in os.walk(repo_path + os.sep + 'test_data'):
        for testfile in files:
            if testfile.endswith('.json'):
                filenames.append(path + os.sep + testfile)
    return filenames
    
def get_filenames_diff(commit_id, old_commit_id):
    filenames = []
    p = subprocess.Popen(["git", "diff", "--name-only", "--diff-filter=ACMRTUXB",
                          "--relative=test_data",
                          old_commit_id, commit_id],
                         cwd=repo_path,
                         stdout=subprocess.PIPE)
    out,err = p.communicate()
    if p.returncode:
        return None

    files=out.split('\n')
    
    filenames = []
    for f in files:
        f = f.strip()
        if f:
            filenames.append(os.path.abspath(
                os.path.join(repo_path + os.sep + "test_data", f)))

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



