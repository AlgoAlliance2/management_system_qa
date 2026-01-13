from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path
import bcrypt

# Load env
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR.parent / "management_system_back" / "app" / ".env"
load_dotenv(dotenv_path=ENV_PATH)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')

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
        plain_password = os.getenv("TEST_ADMIN_PASSWORD")
        if not plain_password:
             raise ValueError("TEST_ADMIN_PASSWORD not set in environment")
        
        users_collection.insert_one({
            "name": "Test Admin",
            "email": admin_email,
            "password": hash_password(plain_password),
            "role": "admin",
            "savedEvents": []
        })
        print(f"Created admin user: {admin_email}")
    else:
        plain_password = os.getenv("TEST_ADMIN_PASSWORD")
        if not plain_password:
             raise ValueError("TEST_ADMIN_PASSWORD not set in environment")
             
        users_collection.update_one(
            {"email": admin_email}, 
            {"$set": {"role": "admin", "password": hash_password(plain_password)}}
        )
        print(f"Updated Admin user password/role: {admin_email}")

    # 2. Ensure Secondary Student User
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
            "password": hash_password(plain_password),
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
            {"$set": {"password": hash_password(plain_password)}}
        )
        print(f"Updated Student 2 password: {student_email}")

    # 3. Ensure Organizer User
    org_email = os.getenv("TEST_ORG_EMAIL")
    if not org_email:
        raise ValueError("TEST_ORG_EMAIL not set in environment")

    organizer = users_collection.find_one({"email": org_email})
    
    if not organizer:
        plain_password = os.getenv("TEST_ORG_PASSWORD")
        if not plain_password:
             raise ValueError("TEST_ORG_PASSWORD not set in environment")
             
        users_collection.insert_one({
            "name": "Test Organizer",
            "email": org_email,
            "password": hash_password(plain_password),
            "role": "organizer",
            "savedEvents": []
        })
        print(f"Created organizer user: {org_email}")
    else:
        plain_password = os.getenv("TEST_ORG_PASSWORD")
        if not plain_password:
             raise ValueError("TEST_ORG_PASSWORD not set in environment")
             
        users_collection.update_one(
            {"email": org_email}, 
            {"$set": {"role": "organizer", "password": hash_password(plain_password)}}
        )
        print(f"Updated Organizer user password/role: {org_email}")

    # 4. Ensure TC-141 specific Student User (test_student@student.usv.ro)
    tc141_student_email = "test_student@student.usv.ro"
    tc141_student_pass = "StudentPass123!"
    
    tc141_student = users_collection.find_one({"email": tc141_student_email})
    
    if not tc141_student:
        users_collection.insert_one({
            "name": "E2E Test Student",
            "email": tc141_student_email,
            "password": hash_password(tc141_student_pass),
            "role": "student",
            "savedEvents": []
        })
        print(f"Created TC-141 student: {tc141_student_email}")
    else:
        users_collection.update_one(
            {"email": tc141_student_email},
            {"$set": {"password": hash_password(tc141_student_pass)}}
        )
        print(f"Updated TC-141 student password: {tc141_student_email}")

except Exception as e:
    print(f"Error: {e}")
