
import sqlite3
from pathlib import Path

# Database file location
DB_PATH = Path(__file__).resolve().parent / "travel_planner.db"


def get_connection():

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# Test database connection
if __name__ == "__main__":

    try:
        connection = get_connection()

        print("SQLite Database Connected Successfully!")
        print("Database Location:", DB_PATH)

        connection.close()

    except Exception as e:
        print("Database Connection Failed:", e)
