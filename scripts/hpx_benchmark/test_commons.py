from __future__ import print_function 

import os
import sys
import subprocess

def get_config():
    if len(sys.argv) != 6:
        print("Error: Invalid command line arguments!", file=sys.stderr)
        exit(1)

    config = { "hpx_dir":             sys.argv[1],
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
        print("Test failed: ", file=sys.stderr)
        print(err, file=sys.stderr)
        exit(1)

    return out


