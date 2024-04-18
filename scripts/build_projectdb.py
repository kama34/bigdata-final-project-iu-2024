import psycopg2 as psql
from pprint import pprint
import os
# from csv_preprocess_utils import preprocess_movie_csv

PROJECT_PATH = '/project/bigdata-final-project-iu-2024'
DATA_PATH = os.path.join(PROJECT_PATH, 'data')


# Read password from secrets file
file = os.path.join("/home/team8/project/secrets", ".psql.pass")
with open(file, "r") as file:
    password = file.read().rstrip()


# build connection string
conn_string = "host=hadoop-04.uni.innopolis.ru port=5432 user=team8 \
    dbname=team8_projectdb password={}".format(password)


# Connect to the remote dbms
with psql.connect(conn_string) as conn:
    # Create a cursor for executing psql commands
    cur = conn.cursor()
    # Read the commands from the file and execute them.
    with open(os.path.join("sql", "create_tables.sql")) as file:
        content = file.read()
        cur.execute(content)
    conn.commit()
    # Read the commands from the file and execute them.
    with open(os.path.join("sql", "import_data.sql")) as file:
        # We assume that the COPY commands in the file
        # are ordered (1.depts, 2.emps)
        commands = file.readlines()
        # import data
        with open(os.path.join(DATA_PATH, "new_movies.csv"), "r") as movies:
            cur.copy_expert(commands[1], movies)
        with open(os.path.join(DATA_PATH, "links.csv"), "r") as links:
            cur.copy_expert(commands[2], links)
        with open(os.path.join(DATA_PATH, "ratings.csv"), "r") as ratings:
            cur.copy_expert(commands[3], ratings)
        with open(os.path.join(DATA_PATH, "tags.csv"), "r") as tags:
            cur.copy_expert(commands[4], tags)
        with open(os.path.join(DATA_PATH, "ganres.csv"), "r") as tags:
            cur.copy_expert(commands[5], tags)
    # If the sql statements are CRUD then you need to commit the change
    conn.commit()

    pprint(conn)
    cur = conn.cursor()
    # Read the sql commands from the file
    with open(os.path.join("sql", "test_database.sql")) as file:
        commands = file.readlines()
        for command in commands:
            cur.execute(command)
            # Read all records and print them
            pprint(cur.fetchall())