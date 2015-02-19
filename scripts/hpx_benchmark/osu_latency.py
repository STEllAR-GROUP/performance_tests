#! /usr/bin/env python

from test_commons import *
from test_parsing import *

def run_test_with_windowsize(config, hpx_command, windowsize):
   
    hpx_command_with_winsize = hpx_command + " --window-size " + str(windowsize) 

    # Build the execution string
    invocation_command = build_command(config, hpx_command_with_winsize)

    # Run the test
    out = run_command(invocation_command)

    # Parse results
    lines = get_lines(out)
    lines = remove_meaningless_lines(lines)
    lines = remove_startswith_lines(lines, "Total time:") 
  
    lines_split = split_lines_by_whitespace(lines) 
     
    results = []
    for row in lines_split:
        if len(row) != 2:
            continue
        value = float(row[1])
        size = row[0]

        arguments = { "size": size,
                      "window": windowsize }

        results.append(build_test_result(config, arguments, value))
    
    # Throw if no results read 
    if len(results) < 1:
        error("Unable to read results!")
        exit(1)

    return results
 

if __name__ == "__main__":
    
    # Get config
    config = get_config("osu_latency")

    if config["localities"] * config["nodes"] != 2:
        send_result([])
        exit(0)

    # Get executable path
    hpx_command = get_hpx_executable(config, "osu_latency")

    # Statically set the max-size
    hpx_command = hpx_command + " --max-size 4096"
    hpx_command = hpx_command + " --loop 200"

    results = []
    # Dynamically set the window-size
    for win_size in [1,10,20,100]:
        current_results = run_test_with_windowsize(config, hpx_command, win_size)
        results.extend(current_results)


    # Send results via writing the json string to stdout
    send_result(results)

