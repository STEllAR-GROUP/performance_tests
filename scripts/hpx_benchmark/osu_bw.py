#! /usr/bin/env python

from test_commons import *
from test_parsing import *

if __name__ == "__main__":
    
    # Get config
    config = get_config("osu_bw")

    # Get executable path
    hpx_executable = get_hpx_executable(config, "osu_bw")

    # Build the execution string
    invocation_command = build_command(config, hpx_executable)

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

        arguments = {"size": size}

        results.append(build_test_result(config, arguments, value))
    
    send_result(results)

