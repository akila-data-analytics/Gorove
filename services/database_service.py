
from database.db_connection import get_connection


class TravelDatabaseService:

    # ==========================================
    # GET ALL DESTINATIONS
    # ==========================================

    def get_destinations(self):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT destination_id, destination_name, state,
                       category, description, estimated_cost,
                       best_time_to_visit
                FROM destinations
                ORDER BY destination_name
            """)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            connection.close()

    # ==========================================
    # GET HOTELS
    # ==========================================

    def get_hotels(self, destination_name):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT h.hotel_name, h.price_per_night, h.rating,
                       h.address, d.destination_name
                FROM hotels h
                JOIN destinations d
                    ON h.destination_id = d.destination_id
                WHERE LOWER(d.destination_name) = LOWER(?)
                ORDER BY h.price_per_night
            """, (destination_name,))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            connection.close()

    # ==========================================
    # GET ACTIVITIES
    # ==========================================

    def get_activities(self, destination_name):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT a.activity_name, a.category,
                       a.estimated_cost, a.description,
                       d.destination_name
                FROM activities a
                JOIN destinations d
                    ON a.destination_id = d.destination_id
                WHERE LOWER(d.destination_name) = LOWER(?)
                ORDER BY a.estimated_cost
            """, (destination_name,))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            connection.close()

    # ==========================================
    # ADD ACTIVITY
    # ==========================================

    def add_activity(
        self,
        destination_name,
        activity_name,
        category,
        estimated_cost,
        description
    ):
        connection = get_connection()
        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT destination_id
                FROM destinations
                WHERE LOWER(destination_name) = LOWER(?)
            """, (destination_name,))

            destination = cursor.fetchone()

            if not destination:
                return f"Destination not found: {destination_name}"

            destination_id = destination["destination_id"]

            cursor.execute("""
                SELECT activity_id
                FROM activities
                WHERE destination_id = ?
                AND LOWER(activity_name) = LOWER(?)
            """, (destination_id, activity_name))

            if cursor.fetchone():
                return f"Activity already exists: {activity_name}"

            cursor.execute("""
                INSERT INTO activities (
                    destination_id, activity_name, category,
                    estimated_cost, description
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                destination_id,
                activity_name,
                category,
                estimated_cost,
                description
            ))

            connection.commit()
            return f"Activity added successfully: {activity_name}"

        except Exception as error:
            connection.rollback()
            return f"Error adding activity: {error}"
        finally:
            connection.close()

    # ==========================================
    # SEARCH FLIGHTS
    # ==========================================

    def search_flights(self, origin, destination):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT airline, flight_number, origin,
                       destination, departure_time,
                       arrival_time, price, travel_date
                FROM flights
                WHERE LOWER(origin) = LOWER(?)
                AND LOWER(destination) = LOWER(?)
                ORDER BY price
            """, (origin, destination))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            connection.close()

    # ==========================================
    # SAVE CUSTOMER TRIP
    # ==========================================

    def save_trip(
        self,
        user_id,
        traveler_name,
        destination,
        start_date,
        end_date,
        budget
    ):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            # Confirm that the customer account exists and is active
            cursor.execute("""
                SELECT user_id
                FROM users
                WHERE user_id = ? AND is_active = 1
            """, (user_id,))

            if not cursor.fetchone():
                return False, "User account not found or inactive."

            # Find destination in the existing destinations table
            cursor.execute("""
                SELECT destination_id
                FROM destinations
                WHERE LOWER(destination_name) = LOWER(?)
            """, (destination.strip(),))

            destination_record = cursor.fetchone()

            if not destination_record:
                return False, (
                    "This destination is not available in our database. "
                    "Please select a listed destination."
                )

            cursor.execute("""
                INSERT INTO trips (
                    traveler_name,
                    destination_id,
                    start_date,
                    end_date,
                    budget,
                    status,
                    user_id
                )
                VALUES (?, ?, ?, ?, ?, 'Planned', ?)
            """, (
                traveler_name,
                destination_record["destination_id"],
                str(start_date),
                str(end_date),
                float(budget),
                user_id
            ))

            connection.commit()
            return True, "Your trip has been saved successfully!"

        except Exception:
            connection.rollback()
            return False, "Unable to save your trip. Please try again."

        finally:
            connection.close()

    # ==========================================
    # GET TRIPS FOR A CUSTOMER
    # ==========================================

    def get_user_trips(self, user_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    t.trip_id,
                    t.traveler_name,
                    d.destination_name,
                    t.start_date,
                    t.end_date,
                    t.budget,
                    t.status,
                    t.created_at
                FROM trips t
                LEFT JOIN destinations d
                    ON t.destination_id = d.destination_id
                WHERE t.user_id = ?
                ORDER BY t.created_at DESC
            """, (user_id,))

            return [dict(row) for row in cursor.fetchall()]

        finally:
            connection.close()

    # ==========================================
    # ADMIN: GET ALL TRIPS
    # ==========================================

    def get_all_trips(self):
        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    t.trip_id,
                    t.traveler_name,
                    d.destination_name,
                    t.start_date,
                    t.end_date,
                    t.budget,
                    t.status,
                    t.created_at,
                    u.user_id,
                    u.full_name,
                    u.email
                FROM trips t
                LEFT JOIN destinations d
                    ON t.destination_id = d.destination_id
                LEFT JOIN users u
                    ON t.user_id = u.user_id
                ORDER BY t.created_at DESC
            """)

            return [dict(row) for row in cursor.fetchall()]

        finally:
            connection.close()

    # ==========================================
    # ADMIN: GET ALL USERS
    # ==========================================

    def get_all_users(self):
        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    user_id,
                    full_name,
                    email,
                    role,
                    is_active,
                    created_at
                FROM users
                ORDER BY created_at DESC
            """)

            return [dict(row) for row in cursor.fetchall()]

        finally:
            connection.close()

    # ==========================================
    # ADMIN: ACTIVATE / DEACTIVATE USER
    # ==========================================

    def update_user_status(self, user_id, is_active):
        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE users
                SET is_active = ?
                WHERE user_id = ?
                AND role = 'customer'
            """, (1 if is_active else 0, user_id))

            connection.commit()

            if cursor.rowcount == 0:
                return False, "Customer account not found."

            return True, "Customer account status updated."

        except Exception:
            connection.rollback()
            return False, "Unable to update customer status."

        finally:
            connection.close()

    # ==========================================
    # ADMIN: UPDATE TRIP STATUS
    # ==========================================

    def update_trip_status(self, trip_id, status):
        allowed_statuses = ["Planned", "Confirmed", "Completed", "Cancelled"]

        if status not in allowed_statuses:
            return False, "Invalid trip status."

        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE trips
                SET status = ?
                WHERE trip_id = ?
            """, (status, trip_id))

            connection.commit()

            if cursor.rowcount == 0:
                return False, "Trip not found."

            return True, "Trip status updated successfully."

        except Exception:
            connection.rollback()
            return False, "Unable to update trip status."

        finally:
            connection.close()

    # ==========================================
    # ADMIN: DASHBOARD SUMMARY
    # ==========================================

    def get_admin_summary(self):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(*) AS total_users
                FROM users
                WHERE role = 'customer'
            """)
            total_users = cursor.fetchone()["total_users"]

            cursor.execute("""
                SELECT COUNT(*) AS active_users
                FROM users
                WHERE role = 'customer' AND is_active = 1
            """)
            active_users = cursor.fetchone()["active_users"]

            cursor.execute("""
                SELECT COUNT(*) AS total_trips
                FROM trips
            """)
            total_trips = cursor.fetchone()["total_trips"]

            cursor.execute("""
                SELECT COUNT(*) AS planned_trips
                FROM trips
                WHERE status = 'Planned'
            """)
            planned_trips = cursor.fetchone()["planned_trips"]

            return {
                "total_users": total_users,
                "active_users": active_users,
                "total_trips": total_trips,
                "planned_trips": planned_trips
            }

        finally:
            connection.close()


# ==========================================
# DATABASE SERVICE TESTING
# ==========================================

if __name__ == "__main__":

    db = TravelDatabaseService()

    print("\n========== DESTINATIONS ==========")
    for destination in db.get_destinations()[:5]:
        print(destination)

    print("\n========== HOTELS IN OOTY ==========")
    for hotel in db.get_hotels("Ooty"):
        print(hotel)

    print("\n========== ACTIVITIES IN OOTY ==========")
    for activity in db.get_activities("Ooty"):
        print(activity)

    print("\n========== SAMPLE FLIGHTS ==========")
    for flight in db.search_flights("Chennai", "Delhi"):
        print(flight)

    print("\n========== ADMIN SUMMARY ==========")
    print(db.get_admin_summary())
