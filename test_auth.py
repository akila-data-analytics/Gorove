
from services.auth_service import AuthService

auth = AuthService()

email = input("Enter Admin Email: ")
password = input("Enter Admin Password: ")

success, message, user = auth.login_user(email, password)

print("\nLogin Result:", message)

if success:
    print("Name:", user["full_name"])
    print("Email:", user["email"])
    print("Role:", user["role"])
