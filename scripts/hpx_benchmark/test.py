#! /usr/bin/env python

from __future__ import print_function

from test_commons import *

if __name__ == "__main__":
    
    # Get config
    config = get_config()

    # Get executable path
    hpx_executable = get_hpx_executable(config, "osu_latency")

    # Build the execution string
    invocation_command = build_command(config, hpx_executable)

    # Run the test
    out = run_command(invocation_command)

    # Parse results
    #TODO 

    print(invocation_command, file=sys.stderr)

    print("[{\"bla\": \"bla2\"}]")
    for arg in sys.argv:
        print("\t" + arg, file=sys.stderr)

    print(out, file=sys.stderr)
#    exit(1)
