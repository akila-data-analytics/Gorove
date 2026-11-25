
from database.db_connection import get_connection


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # 1. Users Table - Authentication
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'customer'
                CHECK (role IN ('customer', 'admin')),
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 2. Destinations Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS destinations (
            destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination_name TEXT NOT NULL,
            state TEXT NOT NULL,
            category TEXT,
            description TEXT,
            estimated_cost REAL,
            best_time_to_visit TEXT
        )
        """)

        # 3. Hotels Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS hotels (
            hotel_id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination_id INTEGER,
            hotel_name TEXT NOT NULL,
            price_per_night REAL,
            rating REAL,
            address TEXT,
            FOREIGN KEY (destination_id)
            REFERENCES destinations(destination_id)
        )
        """)

        # 4. Activities Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination_id INTEGER,
            activity_name TEXT NOT NULL,
            category TEXT,
            estimated_cost REAL,
            description TEXT,
            FOREIGN KEY (destination_id)
            REFERENCES destinations(destination_id)
        )
        """)

        # 5. Flights Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            airline TEXT,
            flight_number TEXT,
            departure_time TEXT,
            arrival_time TEXT,
            price REAL,
            travel_date TEXT
        )
        """)

        # 6. Trips Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
            traveler_name TEXT,
            destination_id INTEGER,
            start_date TEXT,
            end_date TEXT,
            budget REAL,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            FOREIGN KEY (destination_id)
            REFERENCES destinations(destination_id),
            FOREIGN KEY (user_id)
            REFERENCES users(user_id)
        )
        """)

        # Add user_id to existing Trips table if missing
        cursor.execute("PRAGMA table_info(trips)")
        trip_columns = [column[1] for column in cursor.fetchall()]

        if "user_id" not in trip_columns:
            cursor.execute("""
            ALTER TABLE trips
            ADD COLUMN user_id INTEGER REFERENCES users(user_id)
            """)

        # 7. Itineraries Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS itineraries (
            itinerary_id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER,
            day_number INTEGER,
            activity_title TEXT,
            description TEXT,
            estimated_cost REAL,
            FOREIGN KEY (trip_id)
            REFERENCES trips(trip_id)
        )
        """)

        connection.commit()

        print("All 7 Database Tables Created Successfully!")
        print("Users table added successfully!")
        print("Trips table updated with user_id column!")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    create_tables()
