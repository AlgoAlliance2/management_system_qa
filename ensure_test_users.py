from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load env
load_dotenv(dotenv_path="../management_system_back/app/.env")

# Connect (Construct URI manually if needed or from env)
# Assuming local dev defaults if env missing, but we saw previous script worked
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    # Remove hardcoded fallback to prevent leak
    print("ERROR: MONGO_URI not found in environment variables.")
    print("Please ensure you have a .env file in ../management_system_back/app/.env or set MONGO_URI in your environment.")
    exit(1)

try:
    client = MongoClient(MONGO_URI)
    db = client['test'] # Ensure this matches the app's DB
    users_collection = db['users']

    # 1. Ensure Admin User
    admin_email = os.getenv("TEST_ADMIN_EMAIL")
    if not admin_email:
        raise ValueError("TEST_ADMIN_EMAIL not set in environment")

    admin = users_collection.find_one({"email": admin_email})
    
    if not admin:
        # NOTE: Paswords must be hashed in production, but here we match the backend's current plain state.
        plain_password = os.getenv("TEST_ADMIN_PASSWORD")
        if not plain_password:
             raise ValueError("TEST_ADMIN_PASSWORD not set in environment")
        
        users_collection.insert_one({
            "name": "Test Admin",
            "email": admin_email,
            "password": plain_password,
            "role": "admin",
            "savedEvents": []
        })
        print(f"Created admin user: {admin_email}")
    else:
        # Force password update to ensure consistency
        plain_password = os.getenv("TEST_ADMIN_PASSWORD")
        if not plain_password:
             raise ValueError("TEST_ADMIN_PASSWORD not set in environment")
             
        users_collection.update_one(
            {"email": admin_email}, 
            {"$set": {"role": "admin", "password": plain_password}}
        )
        print(f"Updated Admin user password/role: {admin_email}")

    # 2. Ensure Secondary Student User (for RSVP tests)
    student_email = os.getenv("TEST_STUDENT_EMAIL")
    if not student_email:
        raise ValueError("TEST_STUDENT_EMAIL not set in environment")

    student = users_collection.find_one({"email": student_email})
    
    if not student:
        plain_password = os.getenv("TEST_STUDENT_PASSWORD")
        if not plain_password:
             raise ValueError("TEST_STUDENT_PASSWORD not set in environment")
             
        users_collection.insert_one({
            "name": "Test Student 2",
            "email": student_email,
            "password": plain_password,
            "role": "student",
            "savedEvents": []
        })
        print(f"Created secondary student: {student_email}")
    else:
        plain_password = os.getenv("TEST_STUDENT_PASSWORD")
        if not plain_password:
             raise ValueError("TEST_STUDENT_PASSWORD not set in environment")
             
        users_collection.update_one(
            {"email": student_email}, 
            {"$set": {"password": plain_password}}
        )
        print(f"Updated Student 2 password: {student_email}")

except Exception as e:
    print(f"Error: {e}")
