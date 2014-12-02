import psycopg2
import common

conn = psycopg2.connect(common.DB_URL)
cur = conn.cursor()

cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('events',))
if (not cur.fetchone()[0]):
    print("Events table missing!")
    cur.execute("CREATE TABLE events (id serial PRIMARY KEY, team_num integer, check_name char(20), passed boolean, time timestamp);")

cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('injects',))
if (not cur.fetchone()[0]):
    print("Injects table missing!")
    cur.execute("CREATE TABLE injects (id serial PRIMARY KEY, team_num integer, inject_num integer, description text, time timestamp);")


cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('breach',))
if (not cur.fetchone()[0]):
    print("Breach table missing!")
    cur.execute("CREATE TABLE breach (id serial PRIMARY KEY, team_num integer, box_num integer, description text, time timestamp);")


conn.commit()
cur.close()
conn.close()  
