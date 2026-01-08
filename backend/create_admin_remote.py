#!/usr/bin/env python3
"""
Create admin user on remote MongoDB Atlas database.
Run this script locally, pointing to your Atlas connection string.
"""

import asyncio
import uuid
import bcrypt
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import os
import sys

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

async def create_admin_user():
    """Create or update admin user on remote database."""
    # Get connection details
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'luxestate')
    
    if not mongo_url:
        print("❌ Error: MONGO_URL not found in environment variables")
        print("\nPlease set MONGO_URL in your .env file or as environment variable:")
        print("MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/")
        sys.exit(1)
    
    print(f"🔗 Connecting to MongoDB...")
    print(f"📊 Database: {db_name}")
    
    try:
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!\n")
        
        password = "password123"
        hashed_password = hash_password(password)
        
        # Check if admin exists
        existing_admin = await db.users.find_one({'email': 'admin@luxestate.com'})
        
        admin_data = {
            "id": existing_admin.get("id", str(uuid.uuid4())) if existing_admin else str(uuid.uuid4()),
            "email": "admin@luxestate.com",
            "name": "Admin User",
            "role": "admin",
            "password": hashed_password,
            "created_at": existing_admin.get("created_at", datetime.now(timezone.utc).isoformat()) if existing_admin else datetime.now(timezone.utc).isoformat()
        }
        
        if existing_admin:
            # Update existing admin
            await db.users.update_one(
                {"email": "admin@luxestate.com"},
                {"$set": admin_data}
            )
            print("✅ Admin user updated successfully!")
        else:
            # Create new admin
            await db.users.insert_one(admin_data)
            print("✅ Admin user created successfully!")
        
        # Verify it works
        admin = await db.users.find_one({'email': 'admin@luxestate.com'})
        test_verify = verify_password(password, admin['password'])
        
        print(f"\n📧 Email: admin@luxestate.com")
        print(f"🔑 Password: password123")
        print(f"👤 Role: admin")
        print(f"✅ Password verification test: {'PASSED' if test_verify else 'FAILED'}")
        
        if test_verify:
            print("\n🎉 Admin user is ready! You can now login.")
        else:
            print("\n⚠️  Warning: Password verification failed. Please check the setup.")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your MONGO_URL in .env file")
        print("2. Make sure password in connection string is correct")
        print("3. Verify network access is enabled in MongoDB Atlas")
        sys.exit(1)

async def main():
    """Main function."""
    print("=" * 60)
    print("  LUXESTATE - Admin User Creator (Remote Database)")
    print("=" * 60)
    print()
    
    await create_admin_user()
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())


