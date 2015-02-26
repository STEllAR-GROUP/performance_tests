#!/usr/bin/env python

from __future__ import print_function

import sys
import subprocess

def error(msg):
    print(msg, file=sys.stderr)

if len(sys.argv) < 5:
    error("Error: invalid command line syntax!")
    exit(1)


threads = sys.argv[1]
localities = sys.argv[2]
nodes = sys.argv[3]

mpi_processes = str(int(nodes) * int(localities))

call_string = ['srun', '-p', 'marv_noht', '-t', '00:15:00', '-n'+mpi_processes,
                       '-N'+nodes]

call_string.extend(sys.argv[4:])

p = subprocess.Popen(call_string)
p.communicate()

exit(p.returncode)
