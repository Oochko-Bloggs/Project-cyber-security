import sqlite3


def create_connection():
    conn = sqlite3.connection("student.db")
    c = conn.cursor()
    return conn, c


def create_table():
    conn, c = create_connection()
    try:
        c.execute("""
            CREATE TABLE IF NOT EXISTS students  (
                first_name TEXT,
                last_name TEXT,
                student_id INTEGER
            );
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()


def lookup(query):
    conn, c = create_connection()
    try:
        c.execute(query)
        items = c.fetchall()
        for item in items:
            print(item)
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
    finally:
        conn.close()


def show_all(order_by='ASC'):
    conn, c = create_connection()
    try:
        c.execute(f"SELECT rowid, * FROM students ORDER BY student_id {order_by}")
        items = c.fetchall()
        for item in items:
            print(item)
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
    finally:
        conn.close()


def add_single(first_name, last_name, student_id):
    conn, c = create_connection()
    try:
        values = (first_name, last_name, student_id)
        c.execute(f"INSERT INTO students VALUES (?, ?, ?)", values)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting record: {e}")
    finally:
        conn.close()


def add_many(records):
    conn, c = create_connection()
    try:
        c.executemany(f"INSERT INTO students VALUES (?, ?, ?)", records)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting record: {e}")
    finally:
        conn.close()


def update(column_name, new_value, old_value):
    conn, c = create_connection()
    try:
        c.execute(f"UPDATE students SET {column_name} = ? WHERE {column_name}")

        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating record: {e}")
    finally:
        conn.close()


def delete(column_name, value):
    conn, c = create_connection()
    try:
        c.execute(f"DELETE FROM students WHERE {column_name} = ?", (value))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting record: {e}")
    finally:
        conn.close()


def delete_table(table_name=""):
    conn, c = create_connection()
    try:
        if table_name != "":
            c.execute("DROP TABLE IF EXISTS ?", (table_name,))
        else:
            c.execute("DROP TABLE IF EXISTS students")
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting table: {e}")
    finally:
        conn.close()


def rename_table(old_name, new_name):
    conn, c = create_connection()
    try:
        c.execute(f"ALTER TABLE {old_name} RENAME TO {new_name}")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error dleeting table: {e}")
    finally:
        conn.close()


def alter_add(column_name, data_type):
    conn, c = create_connection()
    try:
        c.execute(f"ALTER TABLE students ADD COLUMN  {column_name} {data_type}")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error adding new column : {e}")
    finally:
        conn.close()


def alter_delete(column_name):
    conn, c = create_connection()
    try:
        c.execute(f"ALTER TABLE students DROP COLUMN  {column_name} ")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting column: {e}")
    finally:
        conn.close()


def alter_rename_column(old_name, new_name):
    conn, c = create_connection()
    try:
        c.execute(f"ALTER TABLE  students RENAME COLUMN  {old_name} TO {new_name} ")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error renaming column: {e}")
    finally:
        conn.close()
