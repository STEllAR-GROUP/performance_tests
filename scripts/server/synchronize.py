#!/usr/bin/python


import db_interface
import test_data_interface


# Delete everything.
# There will soon be a better way, but until then, this should work.
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

        #TODO
        # see if test exists
        # create test
        # see if test_run exist
        # create test_run


platforms = db_interface.get_machine_names()
for platform in platforms:
    platform_name = platform[0]
    
    platform_id = db_interface.ensure_platform_exists(platform_name)
    print(str(platform_id) + ": " + platform_name)








# At the end, commit changes to database
#db_interface.commit()
