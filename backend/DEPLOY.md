# Backend Deployment Guide

## Prerequisites

1. **MongoDB Atlas Account** (Free tier available)
   - Sign up at https://www.mongodb.com/cloud/atlas/register
   - Create a free cluster
   - Get your connection string

2. **Deployment Platform** (Choose one):
   - **Railway** (Recommended - Easy setup): https://railway.app
   - **Render** (Free tier available): https://render.com
   - **Fly.io**: https://fly.io

---

## Step 1: Set Up MongoDB Atlas

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up and create a free cluster (M0 Sandbox)
3. Create a database user:
   - Go to Database Access → Add New Database User
   - Username: `luxestate_admin`
   - Password: Generate a secure password (save it!)
   - User Privileges: Read and write to any database

4. Allow network access:
   - Go to Network Access → Add IP Address
   - Click "Allow Access from Anywhere" (0.0.0.0/0) for development
   - Or add your deployment platform's IP ranges

5. Get connection string:
   - Go to Database → Connect → Connect your application
   - Copy the connection string
   - It will look like: `mongodb+srv://username:password@cluster.mongodb.net/`
   - Replace `<password>` with your actual password

---

## Step 2: Deploy to Railway (Recommended)

### Option A: Deploy via GitHub

1. **Push code to GitHub** (already done ✅)

2. **Sign up/Login to Railway**: https://railway.app

3. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `luxestate-website` repository
   - Select `backend` as the root directory

4. **Add Environment Variables**:
   - Click on your service → Variables tab
   - Add these variables:
     ```
     MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
     DB_NAME=luxestate
     JWT_SECRET=your-secret-key-change-this-to-random-string
     CORS_ORIGINS=*
     PORT=8000
     ```

5. **Deploy**:
   - Railway will auto-detect Python and install dependencies
   - It will run `uvicorn server:app` automatically
   - Wait for deployment to complete

6. **Get your backend URL**:
   - Railway will provide a URL like: `https://your-app.railway.app`
   - Copy this URL - you'll need it for frontend!

### Option B: Deploy via Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
cd backend
railway init

# Add environment variables
railway variables set MONGO_URL="mongodb+srv://..."
railway variables set DB_NAME="luxestate"
railway variables set JWT_SECRET="your-secret-key"
railway variables set CORS_ORIGINS="*"

# Deploy
railway up
```

---

## Step 3: Deploy to Render (Alternative)

1. **Sign up/Login**: https://render.com

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `luxestate-website`
   - Set Root Directory to: `backend`

3. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3

4. **Add Environment Variables**:
   ```
   MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   DB_NAME=luxestate
   JWT_SECRET=your-secret-key-change-this
   CORS_ORIGINS=*
   ```

5. **Deploy**: Click "Create Web Service"

---

## Step 4: Seed the Database

After deployment, you need to seed your database with properties:

1. **Option A: SSH into your deployment and run seed script**
2. **Option B: Run locally pointing to MongoDB Atlas**:
   ```bash
   cd backend
   # Update .env with MongoDB Atlas connection string
   python3 seed_properties.py
   python3 fix_admin_password.py
   ```

---

## Step 5: Test Your Backend

1. Visit your backend URL: `https://your-backend.railway.app/api/properties`
2. You should see JSON response with properties
3. Test login: `POST /api/auth/login` with admin credentials

---

## Step 6: Update Frontend

After backend is deployed:

1. Update frontend `.env` or Vercel environment variable:
   ```
   REACT_APP_BACKEND_URL=https://your-backend.railway.app
   ```

2. Redeploy frontend on Vercel

---

## Troubleshooting

- **MongoDB Connection Issues**: 
  - Make sure your IP is whitelisted in Atlas
  - Check connection string has correct password
  - Verify network access settings

- **CORS Issues**:
  - Update CORS_ORIGINS with your frontend URL
  - Or use `*` for development

- **Port Issues**:
  - Make sure PORT environment variable is set
  - Railway/Render set this automatically

---

## Quick Deploy Checklist

- [ ] MongoDB Atlas cluster created
- [ ] Database user created
- [ ] Network access configured
- [ ] Connection string copied
- [ ] Backend deployed to Railway/Render
- [ ] Environment variables set
- [ ] Database seeded with properties
- [ ] Backend URL tested
- [ ] Frontend updated with backend URL


