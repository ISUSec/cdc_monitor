import psycopg2
import datetime

DB_URL = "dbname='monitor'"

def getChecksPerTeam(team_num):
    conn = psycopg2.connect("dbname='monitor'")
    cur = conn.cursor()

    # cur.execute("select check_name, passed, max(time) from events where team_num = '%s' group by check_name, passed;", (team_num,))
    cur.execute("SELECT DISTINCT ON (check_name) check_name, passed, time FROM events where team_num = '%s' ORDER BY check_name, time DESC;", (team_num,))
    results = cur.fetchall()

    cur.close()
    conn.close()

    return results

def printChecksPerTeam(team_num):
	results = getChecksPerTeam(team_num)
	for item in results:
    		print("{0}:{1}{2} \t- Check {3} seconds ago.".format(item[0].strip(), " "*((len("UBUNTU WEB:") + 4)  - len(item[0].strip())),item[1], (datetime.datetime.now() - item[2]).seconds))
