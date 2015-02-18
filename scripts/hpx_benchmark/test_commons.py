from __future__ import print_function 

import os
import sys
import subprocess
import json
import time

def error(msg):
    print(msg, file=sys.stderr)

def get_config(test_name):

    error("Test: " + test_name)

    if len(sys.argv) != 6:
        error("Error: Invalid command line arguments!")
        exit(1)

    config = { "name":                test_name,
               "hpx_dir":             sys.argv[1],
               "threads":             sys.argv[2],
               "localities":          sys.argv[3],
               "nodes":               sys.argv[4],
               "invocation_command":  sys.argv[5] } 

    return config

def get_hpx_executable(config, name):
    return config["hpx_dir"] + os.sep + "bin" + os.sep + name

def build_command(config, hpx_command):
    
    command = config["invocation_command"]

    # Replace wildcards
    command = command.replace("${HPX_PROGRAM}", hpx_command)
    command = command.replace("${THREADS}",     config["threads"])
    command = command.replace("${LOCALITIES}",  config["localities"])
    command = command.replace("${NODES}",       config["nodes"])

    return command

def run_command(command):
    
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
    
    out,err = p.communicate()
    if p.returncode != 0:
        error("Test failed: ")
        error(err)
        exit(1)

    return out

def build_test_result(config, parameters, result):

    result = { "test_name":                 config["name"],
               "num_threads_per_locality":  int(config["threads"]),
               "num_localities_per_node":   int(config["localities"]),
               "num_nodes":                 int(config["nodes"]),
               "timestamp":                 int(time.time()),
               "result":                    float(result)}

    if parameters:
        result["additional_parameters"] = parameters,

    return result

def send_result(results):
    if not isinstance(results, list):
        results = [results]

    print(json.dumps(results))


