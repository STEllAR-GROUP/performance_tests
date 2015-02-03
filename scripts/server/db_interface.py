# this is the database password.
# create a file db_password.py in the same folder,
# containing only:
#
# pw='password'
#
# It will get ignored by git due to .gitignore.
import db_password

import MySQLdb
import time

mysql_host="localhost"
mysql_user="graphs"
mysql_db="graphs_v2"


db = MySQLdb.connect(host=mysql_host,
                     user=mysql_user,
                     passwd=db_password.pw,
                     db=mysql_db)

db.autocommit(False)
cur = db.cursor()

def current_time():
    return int(time.time())

def get_test_timestamps(machine_name, test_name, branch, hpx_commit):
    return 0

def get_machine_names():
    cur.execute("SELECT name FROM machines ORDER BY name")
    return cur.fetchall()

def get_test_names():
    cur.execute("SELECT name FROM tests ORDER BY name")
    return cur.fetchall()

def get_branches():
    cur.execute("SELECT name FROM branches ORDER BY name")
    return cur.fetchall()

def get_commits(branch):
    branch = db.escape_string(branch)
    cur.execute("SELECT id FROM branches WHERE name='" + branch + "'")
    branch_id = cur.fetchall()[0][0]
    cur.execute("SELECT ref_changeset FROM builds WHERE branch_id=" + str(branch_id) + " ORDER BY ref_changeset")
    return cur.fetchall()

existing_platforms = {}
def ensure_platform_exists(platform_name):
    platform_name = db.escape_string(platform_name)

    # prevent the repeated execution of the same query by caching
    if platform_name in existing_platforms:
        return existing_platforms[platform_name]

    # query the os_id
    cur.execute("SELECT id FROM os_list WHERE name='" + platform_name + "'")
    os_ids = cur.fetchall()
    if len(os_ids) < 1:
        cur.execute("INSERT INTO os_list (name) VALUES ('" + platform_name + "')")
        cur.execute("SELECT id FROM os_list WHERE name='" + platform_name + "'")
        os_ids = cur.fetchall()
    os_id = os_ids[0][0]

    # query the machine_id
    cur.execute("SELECT id, os_id FROM machines WHERE name='" + platform_name + "'")
    machine_ids = cur.fetchall()
    if len(machine_ids) < 1:
        cur.execute("INSERT INTO machines (os_id, name, is_active, date_added) "
                    "VALUES (" + str(os_id) + ", '" + platform_name + "', 1, " + str(current_time()) + ")")
        cur.execute("SELECT id, os_id FROM machines WHERE name='" + platform_name + "'")
        machine_ids = cur.fetchall()
    if machine_ids[0][1] != os_id:
        cur.execute("UPDATE machines SET os_id = " + os_id + " WHERE name='" + platform_name + "'")
    machine_id = machine_ids[0][0]
    
    existing_platforms[platform_name] = machine_id

    return machine_id

existing_branches = {}
def ensure_branch_exists(branch_name):
    branch_name = db.escape_string(branch_name)

    # prevent the repeated execution of the same query by caching
    if branch_name in existing_branches:
        return existing_branches[branch_name]

    # query the branch_id
    cur.execute("SELECT id FROM branches WHERE name='" + branch_name + "'")
    branch_ids = cur.fetchall()
    if len(branch_ids) < 1:
        cur.execute("INSERT INTO branches (name) VALUES ('" + branch_name + "')")
        cur.execute("SELECT id FROM branches WHERE name='" + branch_name + "'")
        branch_ids = cur.fetchall()
    branch_id = branch_ids[0][0]

    existing_branches[branch_name] = branch_id

    return branch_id
 
existing_builds = {}
def ensure_build_exists(branch_name, hpx_commit_id):
    branch_name = db.escape_string(branch_name)
    hpx_commit_id = db.escape_string(hpx_commit_id)

    # prevent the repeated execution of the same query by caching
    if (branch_name, hpx_commit_id) in existing_builds:
        return existing_builds[(branch_name, hpx_commit_id)]

    # create branch entry if necessary
    branch_id = ensure_branch_exists(branch_name)

    # query the build_id
    cur.execute("SELECT id FROM builds WHERE branch_id=" + str(branch_id)       \
                                 + " AND ref_changeset='" + hpx_commit_id + "'")
    build_ids = cur.fetchall()
    if len(build_ids) < 1:
        cur.execute("INSERT INTO builds (ref_changeset, branch_id, date_added)" \
                    "VALUES ('" + hpx_commit_id + "', " + str(branch_id) + ", " \
                    + str(current_time()) + ")")

   

def clear_database():
    cur.execute("DELETE FROM builds")
    cur.execute("DELETE FROM branches")
    cur.execute("DELETE FROM os_list")
    cur.execute("DELETE FROM test_runs")
    cur.execute("DELETE FROM machines")
    cur.execute("DELETE FROM annotations")
    cur.execute("DELETE FROM test_run_values")
    cur.execute("DELETE FROM tests")
    cur.execute("DELETE FROM pagesets")
    cur.execute("DELETE FROM pages")
    
def commit():
    db.commit()
