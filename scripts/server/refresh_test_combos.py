#!/usr/bin/python

import subprocess, os
import db_interface, db_password

DOCROOT='/var/www/html/graphs'

def refresh():
    my_env = os.environ.copy()
    
    my_env['PYTHONPATH'] = DOCROOT + '/server'
    my_env['CONFIG_MYSQL_HOST'] = db_interface.mysql_host
    my_env['CONFIG_MYSQL_USER'] = db_interface.mysql_user
    my_env['CONFIG_MYSQL_PASSWORD'] = db_password.pw
    my_env['CONFIG_MYSQL_DBNAME'] = db_interface.mysql_db
    
    p = subprocess.Popen(['/usr/bin/python', DOCROOT + '/scripts/refresh_test_combos.py'], env=my_env)
    
    p.communicate()

if __name__ == "__main__":
    refresh()
