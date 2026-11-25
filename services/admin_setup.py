
import bcrypt
from getpass import getpass

from database.db_connection import get_connection
from services.auth_service import AuthService


def create_admin():

    print("\n========== GoRove Admin Setup ==========\n")

    # Check whether an admin account already exists
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) AS admin_count
            FROM users
            WHERE role = 'admin'
        """)

        admin_count = cursor.fetchone()["admin_count"]

        if admin_count > 0:
            print("An admin account already exists.")
            print("Admin setup cannot be repeated.")
            return

    finally:
        connection.close()

    full_name = input("Enter Admin Full Name: ").strip()
    email = input("Enter Admin Email: ").strip().lower()

    if not full_name:
        print("Full name is required.")
        return

    if not AuthService.validate_email(email):
        print("Please enter a valid email address.")
        return

    password = getpass("Create Admin Password: ")
    confirm_password = getpass("Confirm Admin Password: ")

    if len(password) < 8:
        print("Password must contain at least 8 characters.")
        return

    if password != confirm_password:
        print("Passwords do not match.")
        return

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users (
                full_name,
                email,
                password_hash,
                role,
                is_active
            )
            VALUES (?, ?, ?, 'admin', 1)
        """, (full_name, email, password_hash))

        connection.commit()

        print("\nAdmin account created successfully!")
        print("You can now log in to GoRove using your Admin credentials.")

    except Exception:
        connection.rollback()
        print("\nAdmin account creation failed.")
        print("Please check whether this email is already registered.")

    finally:
        connection.close()


if __name__ == "__main__":
    create_admin()
