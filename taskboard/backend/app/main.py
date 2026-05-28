import sqlite3
import database

if __name__ == "__main__":
    # Create database
    database = database.Database()
    conn = sqlite3.connect(database.get_database())

    # Populate database with default data
    database.populate_db_default()

    # Query and print
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM task")  # Can change this query according to needs
    print(cursor.fetchall())

    # Close connection
    conn.close()
