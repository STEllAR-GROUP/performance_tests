#! /usr/bin/env python

import json
import jsonschema

import os
import sys
import subprocess

scriptpath = os.path.dirname(os.path.realpath(__file__))

active_tests = [ "osu_latency.py",
                 "osu_bw.py" ]



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



pending_tests = []
def finish_pending_tests():

    for i in range(len(pending_tests)):
        print("Waiting for test #" + str(i) + " to finish ...")
        finish_test(test[i][0], test[i][1])

test_id = 0
def run_test(result_vector, test, configuration, machine_config, folder):
    global test_id

    threads     = str(configuration[0])
    localities  = str(configuration[1])
    nodes       = str(configuration[2])

    print("#" + str(test_id) + ": " + test + " ("                               \
              + threads + "/" + localities + "/" + nodes + ")")

    # Build command string
    p = subprocess.Popen([scriptpath + os.sep + test, folder, threads, localities, nodes,
                         machine_config["invocation_command"]],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if machine_config["invoke_parallel"]:
        pending_tests.append([p, result_vector])
    else:
        finish_test(p, result_vector)
    
    test_id = test_id + 1

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

    finish_pending_tests()

    #print json.dumps(result, sort_keys=True,indent=4, separators=(',', ': '))
     
    with open(sys.argv[3], 'wb') as outfile:
#        outfile.write(json.dumps(result, sort_keys=True,indent=4, separators=(',', ': ')))
        outfile.write(json.dumps(result))

