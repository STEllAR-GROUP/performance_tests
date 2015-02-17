#! /usr/bin/env python

from __future__ import print_function

import json
import jsonschema

import os
import sys
import subprocess


scriptpath = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    
    print("[{\"bla\": \"bla2\"}]")
    for arg in sys.argv:
        print("\t" + arg, file=sys.stderr)
