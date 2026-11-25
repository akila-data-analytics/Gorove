
import bcrypt
import re

from database.db_connection import get_connection


class AuthService:

    # -----------------------------------------
    # 1. Email Validation
    # -----------------------------------------
    @staticmethod
    def validate_email(email):

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        return re.match(pattern, email) is not None

    # -----------------------------------------
    # 2. Password Validation
    # -----------------------------------------
    @staticmethod
    def validate_password(password):

        return len(password) >= 8

    # -----------------------------------------
    # 3. Customer Registration
    # -----------------------------------------
    def register_user(self, full_name, email, password):

        full_name = full_name.strip()
        email = email.strip().lower()

        if not full_name:
            return False, "Please enter your full name."

        if not self.validate_email(email):
            return False, "Please enter a valid email address."

        if not self.validate_password(password):
            return False, "Password must contain at least 8 characters."

        # Secure password hashing
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
                    role
                )
                VALUES (?, ?, ?, 'customer')
            """, (
                full_name,
                email,
                password_hash
            ))

            connection.commit()

            return True, "Registration successful!"

        except Exception as error:

            connection.rollback()

            if "UNIQUE constraint failed" in str(error):
                return False, "This email is already registered."

            return False, "Registration failed. Please try again."

        finally:
            connection.close()

    # -----------------------------------------
    # 4. User Login
    # -----------------------------------------
    def login_user(self, email, password):

        email = email.strip().lower()

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT *
                FROM users
                WHERE email = ?
                AND is_active = 1
            """, (email,))

            user = cursor.fetchone()

            if not user:
                return False, "Invalid email or password.", None

            stored_hash = user["password_hash"]

            password_match = bcrypt.checkpw(
                password.encode("utf-8"),
                stored_hash.encode("utf-8")
            )

            if not password_match:
                return False, "Invalid email or password.", None

            user_data = {
                "user_id": user["user_id"],
                "full_name": user["full_name"],
                "email": user["email"],
                "role": user["role"]
            }

            return True, "Login successful!", user_data

        except Exception:
            return False, "Login failed. Please try again.", None

        finally:
            connection.close()

    # -----------------------------------------
    # 5. Get User Details
    # -----------------------------------------
    def get_user_by_id(self, user_id):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT user_id, full_name, email, role,
                       is_active, created_at
                FROM users
                WHERE user_id = ?
            """, (user_id,))

            user = cursor.fetchone()

            if user:
                return dict(user)

            return None

        finally:
            connection.close()
