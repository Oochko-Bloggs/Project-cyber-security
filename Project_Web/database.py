import sqlite3
from hashlib import sha256

# Connect to the database
conn = sqlite3.connect('userdata.db')
c = conn.cursor()

# Hash the password with SHA256
hashed_password = sha256('password'.encode('utf-8')).hexdigest()

# Insert the user into the database
c.execute("INSERT INTO userdata (username, password, email) VALUES (?, ?, ?)",
          ('admin', hashed_password, 'admin@admin.com'))

# Commit the changes and close the connection
conn.commit()
conn.close()
