#!/usr/bin/python


import db_interface
import test_data_interface

import refresh_test_combos

# Uncomment this line for complete database reset.
# This should only be necessary in the case of a deletion.
# Don't use this too much, as it messes with the ids horribly.
# (And with that destroys every static html link to a graph setup)
db_interface.clear_database()


for filename in test_data_interface.get_filenames():
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
