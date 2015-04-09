#! /usr/bin/env python

import sys

from optparse import OptionParser

import db_interface
import test_data_interface

import refresh_test_combos



### PARSE COMMAND LINES ###
parser = OptionParser(usage="%prog [options] <data_repository_path>")

parser.add_option("--clear-database", action="store_true", dest="reset", default=False,
                  help="""Resets the whole database and rewrites all entries.
                        WARNING: TAKES A LONG TIME! Also, it completely messes
                        with the ids needed for website references. So DON'T DO IT!""")
parser.add_option("--temp-file", "-t", action="store", dest="version_file", default="/tmp/synchronize_perfomatic.txt",
                  help="Defines a file where the script will store the previous commit id. This improves performance drastically.")

(options, args) = parser.parse_args()

if len(args) < 1:
    parser.error("data_repository_path not set!")
    exit(1)

if len(args) > 1:
    parser.error("too many command line arguments!")
    exit(1)



### TRY TO FIND LAST SYNCHRONIZED COMMIT ###
last_commit_id=None
print("Using version file: " + options.version_file)
try:
    with open (options.version_file, "r") as myfile:
        last_commit_id=myfile.read().replace('\n', '')
except:
    print("Warning: Unable to read the version file. Performing full sync ... (might take a long time)")


### RESET DATABASE IF REQUESTED ###
# Uncomment this line for complete database reset.
# This should only be necessary in the case of a deletion.
# Don't use this too much, as it messes with the ids horribly.
# (And with that destroys every static html link to a graph setup)
if options.reset:
    print("CLEARING DATABASE ...")
    db_interface.clear_database()

### SET DATA REPOSITORY PATH ###
test_data_interface.set_repo_path(args[0])

### GET CURRENT COMMIT ID ###
current_commit_id = test_data_interface.get_current_commit()



### FETCH FILE LIST ###
if last_commit_id:
    print("Searching for changed files since " + last_commit_id + " ...")
    filenames = test_data_interface.get_filenames_diff(current_commit_id,
                                                       last_commit_id)   
    if filenames == None:
        print("Error: Unable to fetch changed files. Performing full sync ...")
        filenames = test_data_interface.get_filenames()
else:
    filenames = test_data_interface.get_filenames()


### SYNCHRONIZE ###
for filename in filenames:
    print("Processing file '" + filename + "'...")
    file_content = test_data_interface.open_testfile(filename)
    
    # go through all build configs in current file
    build_configs = test_data_interface.get_build_configs(file_content)
    for build_config in build_configs:

        # get platform name
        platform_name = test_data_interface.get_platform_name(build_config)
        
        # create platform in database if necessary
        platform_id = db_interface.ensure_platform_exists(platform_name)
        
        # get branch name
        branch_name = test_data_interface.get_branch_name(build_config)

        # get hpx commit id
        hpx_commit_id = test_data_interface.get_hpx_commit_id(build_config)

        # create build entry in database if necessary
        build_id = db_interface.ensure_build_exists(branch_name, hpx_commit_id)

        # go through all submitted tests
        tests = test_data_interface.get_tests(build_config)
        for test_data in tests:
            
            # get test name
            test_name = test_data_interface.get_test_name(test_data)

            # create test in database if necessary
            test_id = db_interface.ensure_test_exists(test_name)

            # get test timestamp
            test_time = test_data_interface.get_test_time(test_data)

            # get test result
            test_result = test_data_interface.get_test_result(test_data)

            db_interface.insert_testrun(build_id, platform_id, test_id,         \
                                        test_time, test_result)


#platforms = db_interface.get_machine_names()
#for platform in platforms:
#    platform_name = platform[0]
#    
#    platform_id = db_interface.ensure_platform_exists(platform_name)
#    print(str(platform_id) + ": " + platform_name)


# At the end, commit changes to database
db_interface.commit()


# Refresh the test combinations
refresh_test_combos.refresh()



# Write new commit id to tmpfile
with open(options.version_file, "w") as myfile:
    myfile.write(current_commit_id)

print("Database is now synchronized with commit " + current_commit_id + ".")
