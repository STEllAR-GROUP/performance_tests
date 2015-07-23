#! /usr/bin/env python

from test_commons import *

def run_test_with_vecsize(config, hpx_command, vectorsize):
    hpx_command = hpx_command + " --vector_size " + str(vectorsize)

    # Build the execution string
    invocation_command = build_command(config, hpx_command)

    # Run the test
    out = run_command(invocation_command)

    # Parse results
    seq_time, par_time, task_time = map(float, out[1:].split(','))

    # Take the max of par_time and task time. Because of the extra
    # overhead, this will usually just be task_time
    scale = seq_time / max(par_time, task_time)

    arguments = { "vector_size": vectorsize }

    result = build_test_result(config, arguments, scale)
    return [result]


if __name__ == "__main__":

    # Get config
    config = get_config("foreach_scaling")

# Is this condition needed for a foreach test?
#    if config["localities"] * config["nodes"] != 2:
#        send_result([])
#        exit(0)

    # Get executable path
    hpx_command = get_hpx_executable(config, "foreach_scaling")

    # Statically set the max-size
    hpx_command = hpx_command + " --csv_output 1 "
    hpx_command = hpx_command + " --work_delay 100 "

    results = []
    # Dynamically set the vector size and the work_delay
    for vec_size in [100, 1000, 10000]:
        current_results = run_test_with_vecsize(config, hpx_command, vec_size)
        results.extend(current_results)

    # Send results via writing the json string to stdout
    send_result(results)
