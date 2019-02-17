import requests
import json
import MySQLdb

headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
}

with open('config.json') as data_file:
    config = json.load(data_file)

db = MySQLdb.connect(
    host=config["tanyajob_db"]["host"],
    user=config["tanyajob_db"]["user"],
    passwd=config["tanyajob_db"]["passwd"],
    db=config["tanyajob_db"]["db"])

master_list = [
    "degrees", "facilities", "fields", "industries", "job_levels", "locations",
    "majors", "skill_sets"
]

for mstr in master_list:
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT name FROM master_" + mstr)
    print "-----------------" + mstr + "-----------------"
    url = config["base_host"] + "/api/master_" + mstr + "/"
    for row in cur.fetchall():
        payload = {"name": row["name"]}
        data = json.dumps(payload)
        print data
        response = requests.request("POST", url, data=data, headers=headers)

        if response.status_code != 201:
            print response.text
            print data
        else:
            print row["name"]
