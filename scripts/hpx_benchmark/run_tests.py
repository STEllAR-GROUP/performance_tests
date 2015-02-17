#! /usr/bin/env python

import json
import jsonschema

import os
import sys
import subprocess

scriptpath = os.path.dirname(os.path.realpath(__file__))

active_tests = [ "./osu_latency.py" ]



def load_machine_config(configfile):
  
    with open(scriptpath + os.sep + ".." + os.sep + ".." + os.sep               \
              + "machine_configs" + os.sep + "machine_config.schema.json") as f:
        json_schema = json.load(f)
    json_validator = jsonschema.Draft3Validator(json_schema)
    

    with open(configfile) as f:
        machine_config = json.load(f)
    
    errors = sorted(json_validator.iter_errors(machine_config), key=lambda e: e.path)

    if len(errors) == 0:
        return machine_config

    print "'" + configfile + "' is not valid!"
    print

    for error in errors:
        print(error)

    exit(1)
    
def generate_result_template(machine_config):
    result = {"build_configurations":[]}
    return result

def finish_test(p, result_vector):
    out,err = p.communicate()
    if p.returncode != 0:
        print "Test failed: "
        print "==============="
        print err
        print "==============="
        return

    result = json.loads(out)
    result_vector.extend(result)



def run_test(result_vector, test, configuration, machine_config, folder):
    print test, configuration, folder

    threads     = str(configuration[0])
    localities  = str(configuration[1])
    nodes       = str(configuration[2])

    # Build command string
    p = subprocess.Popen([test, folder, threads, localities, nodes,
                         machine_config["invocation_command"]],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    finish_test(p, result_vector)
    #machine_config["invoke_parallel"]

def run_test_series(build, machine_config, hpx_commit_id):

    result = { "machine_name":  machine_config["machine_name"],
               "compiler":      build["compiler"],
               "boost":         build["boost"],
               "allocator":     build["allocator"], 
               "branch":        ("hpx_" + build["branch"]),
               "hpx_commit_id": hpx_commit_id,
               "tests":         [] }

    for test in active_tests:
        for configuration in machine_config["configurations"]:
            run_test(result["tests"], test, configuration, machine_config,
                     build["folder"]) 
        
    return result

if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        print("Usage:")
        print("\t" + sys.argv[0] + " <machine-config> <hpx-commit-id> <output>")
        print("")
        exit(1)

    machine_config = load_machine_config(sys.argv[1])
    hpx_commit_id = sys.argv[2]
    
    result = generate_result_template(machine_config)

    for build in machine_config["builds"]:
        testseries_result = run_test_series(build, machine_config, hpx_commit_id)
        result["build_configurations"].append(testseries_result)

    print json.dumps(result, sort_keys=True,indent=4, separators=(',', ': '))
     
