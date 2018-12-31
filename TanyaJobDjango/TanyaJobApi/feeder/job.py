import requests
import json
import MySQLdb


with open('config.json') as data_file:
    config = json.load(data_file)


url = config["base_host"] + "/api/job/"

headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "612ff27d-b3e1-42c3-8e89-063b016882e4"
}

db = MySQLdb.connect(host=config["tanyajob_db"]["host"], user=config["tanyajob_db"]["user"], passwd=config["tanyajob_db"]["passwd"], db=config["tanyajob_db"]["db"]) 

cur = db.cursor(MySQLdb.cursors.DictCursor)

# Use all the SQL you like
cur.execute("""
SELECT 
    work_experiences.job_position as title,
    master_degrees.name as degree,
    master_majors.name as major,
    master_industries.name as industry,
    YEAR(CURDATE()) - YEAR(users.date_of_birth) AS min_age,
    YEAR(CURDATE()) - YEAR(users.date_of_birth) AS max_age,
    master_fields.name as field,
    master_locations.name as location,
    master_job_levels.name as job_level,
    work_experiences.salary_lower  as min_salary,
    work_experiences.salary_upper  as max_salary,
    if (current = 1 OR work_experiences.started_work_at > work_experiences.ended_work_at, 
        DATEDIFF(CURDATE(),work_experiences.started_work_at), 
        DATEDIFF(work_experiences.ended_work_at,work_experiences.started_work_at)) / 30
    as work_exp
    FROM users
    JOIN work_experiences ON users.id = work_experiences.user_id
    JOIN master_degrees ON users.last_degree_id = master_degrees.id
    JOIN master_majors ON users.major_id = master_majors.id 
    JOIN master_industries ON master_industries.id = work_experiences.industry_id
    JOIN master_fields ON master_fields.id = work_experiences.field_id
    JOIN master_locations ON master_locations.id = work_experiences.location_id
    JOIN master_job_levels ON master_job_levels.id = work_experiences.job_level_id;
""")

for row in cur.fetchall():
    payload = {
        "title": row["title"],
        "degree": row["degree"],
        "major": row["major"],
        "industry": row["industry"],
        "min_age": row["min_age"],
        "max_age": row["max_age"],
        "field": row["field"],
        "location": row["location"],
        "job_level": row["job_level"],
        "work_exp": float(row["work_exp"]),
        "min_salary": row["min_salary"],
        "max_salary": row["max_salary"]
    }

    data = json.dumps(payload)

    response = requests.request("POST", url, data=data, headers=headers)

    if response.status_code != 201:
        print response.text
        print data
    else:
        print row["title"]
