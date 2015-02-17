#! /usr/bin/env python

from test_commons import *


if __name__ == "__main__":
    
    # Get config
    config = get_config("osu_latency")

    # Get executable path
    hpx_executable = get_hpx_executable(config, "osu_latency")

    # Build the execution string
    invocation_command = build_command(config, hpx_executable)

    # Run the test
    out = run_command(invocation_command)

    # Parse results
    #TODO 
    results = []
    results.append(build_test_result(config, {}, 1.0))
    send_result(results)


    error(invocation_command)

    for arg in sys.argv:
        error("\t" + arg)

    error(out)
    
#    exit(1)
