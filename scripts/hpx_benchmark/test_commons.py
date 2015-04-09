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

    if len(sys.argv) != 7:
        error("Error: Invalid command line arguments!")
        error("Expected: <hpx_dir> <threads> <localities> <nodes> <parcelport> <command>")
        exit(1)

    config = { "name":                test_name,
               "hpx_dir":             sys.argv[1],
               "threads":             int(sys.argv[2]),
               "localities":          int(sys.argv[3]),
               "nodes":               int(sys.argv[4]),
               "parcelport":          sys.argv[5],
               "invocation_command":  sys.argv[6] } 

    return config

def get_hpx_executable(config, name):
    return config["hpx_dir"] + os.sep + "bin" + os.sep + name

def build_command(config, hpx_command):
    
    command = config["invocation_command"]

    hpx_command = hpx_command + " --hpx:threads " + str(config["threads"])

    # add parcelport flags
    if config["parcelport"] == "mpi":
        hpx_command = hpx_command + " --hpx:ini hpx.parcel.tcp.enable=0"
        hpx_command = hpx_command + " --hpx:ini hpx.parcel.bootstrap=mpi"

    # Replace wildcards
    command = command.replace("${HPX_PROGRAM}", hpx_command)
    command = command.replace("${THREADS}",     str(config["threads"]))
    command = command.replace("${LOCALITIES}",  str(config["localities"]))
    command = command.replace("${NODES}",       str(config["nodes"]))

    return command

def run_command(command):
    
    error("Running: " + command)

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
               "timestamp":                 int(time.time()),
               "result":                    float(result)}

    if parameters:
        result["additional_parameters"] = parameters

    return result

def send_result(results):
    if not isinstance(results, list):
        results = [results]

    print(json.dumps(results))


