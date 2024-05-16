#!/usr/bin/env python3
import sqlite3
from sys import argv

# Database_File = "student.db"
if len(argv) == 2:
    Database_File = argv[1]
else:
    exit(1)

# Connect to the database
conn = sqlite3.connect(Database_File)
# Create a cursor object
c = conn.cursor()
# Query to create table
create_table_query = f"""CREATE TABLE IF NOT EXISTS students (
	id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	student_id INTEGER NOT NULL UNIQUE
)"""
# Execute the SQL query
c.execute(create_table_query)

# Commit the changes to the database and close the connection
conn.commit()
conn.close()
