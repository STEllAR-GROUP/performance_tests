from __future__ import print_function 

from test_commons import error

def get_lines(str_in):

    return str_in.split('\n')

def join_lines(lines):

    str_out = ""
    for line in lines:
        if len(str_out) != 0:
            str_out = str_out + '\n'
        str_out = str_out + line

    return str_out

def trim_lines(lines_in):

    lines_out = []
    for line in lines_in:
        lines_out.append(line.strip())

    return lines_out

def remove_meaningless_lines(lines_in):

    lines_out = []

    for line in lines_in:

        line_trimmed = line.strip()
        if len(line_trimmed) == 0:
            continue
        if line_trimmed.startswith('#'):
            continue

        lines_out.append(line)

    return lines_out
    
     
def remove_startswith_lines(lines_in, string):

    lines_out = []
    
    for line in lines_in:

        if line.startswith(string):
            continue

        lines_out.append(line)

    return lines_out

def split_lines_by_whitespace(lines_in):

    output = []

    for line in lines_in:
        
        output.append(line.split())

    return output

def split_lines(lines_in, delim):

    output = []

    for line in lines_in:

        output.append(line.split(delim))

    return output




