#!/usr/bin/env python3
"""
Quick script to create an admin user for Luxestate.
"""

import asyncio
import uuid
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

async def create_admin_user():
    """Create an admin user for the application."""
    admin_id = str(uuid.uuid4())
    admin = {
        "id": admin_id,
        "email": "admin@luxestate.com",
        "name": "Admin User",
        "role": "admin",
        "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi",  # "password123"
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.users.update_one(
        {"email": "admin@luxestate.com"},
        {"$set": admin},
        upsert=True
    )
    print("✅ Admin user created successfully!")
    print(f"📧 Email: admin@luxestate.com")
    print(f"🔑 Password: password123")
    return admin_id

async def main():
    """Main function to create admin user."""
    try:
        await create_admin_user()
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())

