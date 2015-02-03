# this is the database password.
# create a file db_password.py in the same folder,
# containing only:
#
# pw='password'
#
# It will get ignored by git due to .gitignore.
import db_password

import MySQLdb

mysql_host="localhost"
mysql_user="graphs"
mysql_db="graphs_v2"


db = MySQLdb.connect(host=mysql_host,
                     user=mysql_user,
                     passwd=db_password.pw,
                     db=mysql_db)

cur = db.cursor()
cur.execute("SET autocommit=0")

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
    cur.execute("SELECT id FROM branches WHERE name='" + branch + "'");
    branch_id = cur.fetchall()[0][0]
    cur.execute("SELECT ref_changeset FROM builds WHERE branch_id=" + str(branch_id) + " ORDER BY ref_changeset")
    return cur.fetchall()


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
    
