#!/usr/bin/env python3
"""
Fix admin user password by properly hashing it with bcrypt.
"""

import asyncio
import uuid
import bcrypt
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
MONGO_URL = os.environ['MONGO_URL']
DB_NAME = os.environ['DB_NAME']

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

async def fix_admin_password():
    """Update admin user with properly hashed password."""
    password = "password123"
    hashed_password = hash_password(password)
    
    # Check if admin exists
    existing_admin = await db.users.find_one({'email': 'admin@luxestate.com'})
    
    if existing_admin:
        # Update existing admin
        await db.users.update_one(
            {"email": "admin@luxestate.com"},
            {"$set": {"password": hashed_password}}
        )
        print("✅ Admin password updated successfully!")
    else:
        # Create new admin
        admin_id = str(uuid.uuid4())
        admin = {
            "id": admin_id,
            "email": "admin@luxestate.com",
            "name": "Admin User",
            "role": "admin",
            "password": hashed_password,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.update_one(
            {"email": "admin@luxestate.com"},
            {"$set": admin},
            upsert=True
        )
        print("✅ Admin user created with proper password hash!")
    
    # Verify it works
    admin = await db.users.find_one({'email': 'admin@luxestate.com'}, {'_id': 0})
    test_verify = bcrypt.checkpw(password.encode('utf-8'), admin['password'].encode('utf-8'))
    
    print(f"📧 Email: admin@luxestate.com")
    print(f"🔑 Password: password123")
    print(f"✅ Password verification test: {'PASSED' if test_verify else 'FAILED'}")

async def main():
    """Main function."""
    try:
        await fix_admin_password()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())

