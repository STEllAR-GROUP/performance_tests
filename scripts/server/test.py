#!/usr/bin/python


import db_interface

branches = db_interface.get_branches();
print "branches: " + str(branches);


