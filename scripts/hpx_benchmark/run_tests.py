#! /usr/bin/env python

import json

import os
import sys

scriptpath = os.path.dirname(os.path.realpath(__file__))


if __name__ == "__main__":
   
    
    if len(sys.argv) != 3:
        print("Usage:")
        print("\t" + sys.argv[0] + " <machine-config> <hpx-commit-id>")
        print("")
        exit(1)

    for i in range(1,len(sys.argv)):
        validate(sys.argv[i], test_validator)
