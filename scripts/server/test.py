#!/usr/bin/python


import db_interface
import test_data_interface

test_data_interface.read_test_data_roughly()

branches = db_interface.get_branches();

for branch in branches:
    print "branch: " + branch[0]
    for commit in db_interface.get_commits(branch[0]):
        print "   commit: " + commit[0]

machines = db_interface.get_machine_names()

for machine in machines:
    print "machine: " + machine[0]


