# MongoDB Setup Guide

## Option 1: Local MongoDB (Recommended for Development)

### macOS (using Homebrew):
```bash
# Install MongoDB
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB service
brew services start mongodb-community

# Verify it's running
mongosh --eval "db.version()"
```

### Alternative: Run MongoDB with Docker:
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Verify it's running
docker ps
```

## Option 2: MongoDB Atlas (Cloud - Free Tier Available)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for a free account
3. Create a new cluster (choose the FREE tier)
4. Click "Connect" → "Connect your application"
5. Copy the connection string (it will look like: `mongodb+srv://username:password@cluster.mongodb.net/`)
6. Update your `.env` file:
   ```
   MONGO_URL="mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
   DB_NAME="luxestate"
   ```

**Important:** Replace `username` and `password` with your Atlas credentials, and add your IP address to the whitelist in Atlas dashboard.

## Verify Connection

After setting up MongoDB (local or Atlas), test the connection:

```bash
cd backend
python3 -c "from motor.motor_asyncio import AsyncIOMotorClient; import asyncio; client = AsyncIOMotorClient('YOUR_MONGO_URL'); print('Connected!' if asyncio.run(client.admin.command('ping')) else 'Failed')"
```

## Update Your .env File

Make sure your `backend/.env` file has:
```env
MONGO_URL="mongodb://localhost:27017"  # or your Atlas connection string
DB_NAME="luxestate"  # or "test_database" if you prefer
JWT_SECRET="your-secret-key-here"
CORS_ORIGINS="*"
```

Then run the seeder:
```bash
python3 seed_properties.py
```

