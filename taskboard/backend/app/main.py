from routes.tasks import task_pages
import sqlite3
import database
from flask import Flask

app = Flask(__name__)
app.register_blueprint(task_pages)

if __name__ == "__main__":
    # Create database
    database = database.Database()
    conn = sqlite3.connect(database.get_database())

    # Populate database with default data
    database.populate_db_default()

    # Run app
    app.run(host="0.0.0.0", port=4000)

    # Close connection
    conn.close()
