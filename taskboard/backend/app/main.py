from routes.tasks import task_pages
from routes.projects import project_pages
import sqlite3
import database
from flask import Flask
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
CORS(app)
metrics = PrometheusMetrics(app)

app.register_blueprint(task_pages)
app.register_blueprint(project_pages)

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