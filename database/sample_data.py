
from database.db_connection import get_connection


def insert_sample_data():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    # 1. DESTINATIONS DATA
    if cursor.execute("SELECT COUNT(*) FROM destinations").fetchone()[0] == 0:

        destinations = [
            ("Ooty", "Tamil Nadu", "Hill Station", "Queen of Hills", 8000, "October to June"),
            ("Kodaikanal", "Tamil Nadu", "Hill Station", "Princess of Hill Stations", 7500, "April to June"),
            ("Munnar", "Kerala", "Hill Station", "Tea gardens and mountains", 9000, "September to March"),
            ("Coorg", "Karnataka", "Hill Station", "Coffee plantations", 10000, "October to March"),
            ("Goa", "Goa", "Beach", "Beaches and nightlife", 12000, "November to February"),
            ("Jaipur", "Rajasthan", "Historical", "Pink City and forts", 11000, "October to March"),
            ("Manali", "Himachal Pradesh", "Hill Station", "Snow mountains", 15000, "October to February"),
            ("Pondicherry", "Puducherry", "Beach", "French architecture and beaches", 7000, "October to March"),
            ("Wayanad", "Kerala", "Nature", "Forests and waterfalls", 8500, "October to May"),
            ("Alleppey", "Kerala", "Backwaters", "Houseboats and backwaters", 9500, "November to February")
        ]

        cursor.executemany("""
            INSERT INTO destinations
            (destination_name, state, category, description,
             estimated_cost, best_time_to_visit)
            VALUES (?, ?, ?, ?, ?, ?)
        """, destinations)

    # Get destination IDs
    destination_rows = cursor.execute("""
        SELECT destination_id, destination_name
        FROM destinations
    """).fetchall()

    destination_ids = {
        row["destination_name"]: row["destination_id"]
        for row in destination_rows
    }

    # 2. HOTELS DATA
    if cursor.execute("SELECT COUNT(*) FROM hotels").fetchone()[0] == 0:

        hotels = [
            ("Ooty", "Hotel Lake View", 1800, 4.2, "Ooty Lake Road"),
            ("Ooty", "Mountain Retreat", 2500, 4.5, "Fern Hill"),
            ("Kodaikanal", "Hill Country Resort", 2200, 4.3, "Observatory Road"),
            ("Kodaikanal", "Pine Tree Stay", 1500, 4.0, "Pine Forest"),
            ("Munnar", "Tea Valley Resort", 2800, 4.6, "Tea Estate Road"),
            ("Munnar", "Green Woods Hotel", 2000, 4.2, "Munnar Town"),
            ("Coorg", "Coffee Plantation Stay", 3000, 4.5, "Madikeri"),
            ("Coorg", "Nature Nest Resort", 2400, 4.3, "Kushalnagar"),
            ("Goa", "Beach Paradise Hotel", 3500, 4.4, "Calangute Beach"),
            ("Goa", "Sea View Residency", 2800, 4.1, "Baga"),
            ("Jaipur", "Royal Heritage Inn", 2600, 4.5, "Pink City"),
            ("Jaipur", "City Palace Hotel", 3200, 4.6, "MI Road"),
            ("Manali", "Snow Peak Resort", 4000, 4.7, "Old Manali"),
            ("Pondicherry", "French Corner Stay", 1900, 4.2, "White Town"),
            ("Wayanad", "Forest View Resort", 2700, 4.4, "Kalpetta")
        ]

        cursor.executemany("""
            INSERT INTO hotels
            (destination_id, hotel_name, price_per_night, rating, address)
            VALUES (?, ?, ?, ?, ?)
        """, [
            (destination_ids[d], name, price, rating, address)
            for d, name, price, rating, address in hotels
        ])

    # 3. ACTIVITIES DATA
    if cursor.execute("SELECT COUNT(*) FROM activities").fetchone()[0] == 0:

        activities = [
            ("Ooty", "Ooty Lake Boating", "Adventure", 200, "Enjoy boating at Ooty Lake"),
            ("Ooty", "Botanical Garden", "Nature", 50, "Explore beautiful gardens"),
            ("Kodaikanal", "Coaker's Walk", "Sightseeing", 30, "Enjoy scenic valley views"),
            ("Kodaikanal", "Pillar Rocks", "Nature", 50, "Visit famous rock formations"),
            ("Munnar", "Tea Museum", "Cultural", 150, "Learn about tea production"),
            ("Munnar", "Eravikulam National Park", "Nature", 200, "Explore wildlife and landscapes"),
            ("Coorg", "Abbey Falls", "Nature", 100, "Visit scenic waterfalls"),
            ("Coorg", "Coffee Plantation Tour", "Adventure", 300, "Explore coffee plantations"),
            ("Goa", "Beach Activities", "Adventure", 500, "Enjoy beach activities"),
            ("Goa", "Water Sports", "Adventure", 1200, "Experience water sports"),
            ("Jaipur", "Amber Fort", "Historical", 200, "Explore historic fort"),
            ("Jaipur", "City Palace", "Historical", 300, "Visit royal palace"),
            ("Manali", "Solang Valley", "Adventure", 500, "Enjoy mountain activities"),
            ("Manali", "Rohtang Pass", "Nature", 800, "Explore mountain scenery"),
            ("Pondicherry", "Paradise Beach", "Beach", 150, "Relax at the beach"),
            ("Pondicherry", "French Quarter Walk", "Sightseeing", 0, "Explore French architecture"),
            ("Wayanad", "Edakkal Caves", "Historical", 100, "Explore ancient caves"),
            ("Wayanad", "Banasura Dam", "Nature", 50, "Enjoy scenic reservoir views"),
            ("Alleppey", "Houseboat Cruise", "Adventure", 1500, "Experience backwater cruise"),
            ("Alleppey", "Alappuzha Beach", "Beach", 0, "Enjoy sunset at the beach")
        ]

        cursor.executemany("""
            INSERT INTO activities
            (destination_id, activity_name, category, estimated_cost, description)
            VALUES (?, ?, ?, ?, ?)
        """, [
            (destination_ids[d], name, category, cost, description)
            for d, name, category, cost, description in activities
        ])

    # 4. SAMPLE FLIGHT DATA
    if cursor.execute("SELECT COUNT(*) FROM flights").fetchone()[0] == 0:

        flights = [
            ("Chennai", "Coimbatore", "IndiGo", "6E101", "08:00", "09:00", 2500, "2026-12-10"),
            ("Chennai", "Bengaluru", "Air India", "AI201", "10:00", "11:00", 3000, "2026-12-10"),
            ("Chennai", "Goa", "IndiGo", "6E301", "07:30", "09:00", 4500, "2026-12-11"),
            ("Chennai", "Jaipur", "Air India", "AI401", "06:00", "09:00", 6000, "2026-12-12"),
            ("Bengaluru", "Kochi", "IndiGo", "6E501", "09:00", "10:15", 2800, "2026-12-10"),
            ("Bengaluru", "Goa", "Air India", "AI601", "11:00", "12:15", 3200, "2026-12-11"),
            ("Coimbatore", "Chennai", "IndiGo", "6E701", "14:00", "15:00", 2600, "2026-12-12"),
            ("Coimbatore", "Bengaluru", "Air India", "AI801", "16:00", "17:00", 2900, "2026-12-13"),
            ("Delhi", "Manali", "Demo Air", "DA901", "08:00", "09:30", 5000, "2026-12-14"),
            ("Delhi", "Jaipur", "IndiGo", "6E1001", "12:00", "13:00", 3500, "2026-12-15"),
            ("Kochi", "Coimbatore", "Air India", "AI1101", "09:30", "10:30", 2700, "2026-12-16"),
            ("Kochi", "Goa", "IndiGo", "6E1201", "13:00", "14:30", 3800, "2026-12-17"),
            ("Chennai", "Kochi", "Air India", "AI1301", "07:00", "08:15", 3200, "2026-12-18"),
            ("Bengaluru", "Jaipur", "IndiGo", "6E1401", "15:00", "17:30", 5500, "2026-12-19"),
            ("Delhi", "Goa", "Air India", "AI1501", "06:30", "09:00", 6500, "2026-12-20")
        ]

        cursor.executemany("""
            INSERT INTO flights
            (origin, destination, airline, flight_number,
             departure_time, arrival_time, price, travel_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, flights)

    connection.commit()

    # Verify inserted records
    print("\nTRAVEL DATABASE RECORD SUMMARY")
    print("--------------------------------")

    for table in ["destinations", "hotels", "activities", "flights"]:
        count = cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f"{table}: {count} records")

    connection.close()

    print("\nSample Travel Data Inserted Successfully!")


if __name__ == "__main__":
    insert_sample_data()
