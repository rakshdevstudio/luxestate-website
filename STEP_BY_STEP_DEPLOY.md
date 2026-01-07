# 🚀 Complete Deployment Guide - Step by Step

Follow these steps in order to deploy your Luxestate application.

---

## 📋 STEP 1: Set Up MongoDB Atlas (5 minutes)

### 1.1 Create MongoDB Atlas Account
1. Go to: **https://www.mongodb.com/cloud/atlas/register**
2. Click **"Try Free"** or **"Sign Up"**
3. Fill in:
   - Email address
   - Password
   - First/Last name
   - Company (optional - can skip)
4. Accept terms and click **"Get started free"**

### 1.2 Create a Free Cluster
1. On the **"Deploy a cloud database"** page:
   - Select **"M0" (Free tier)** - should be selected by default
   - Choose a **Cloud Provider**: AWS (default is fine)
   - Select a **Region**: Choose closest to you (e.g., `US East (N. Virginia)`)
2. Click **"Create"**
3. Wait 3-5 minutes for cluster to deploy

### 1.3 Create Database User
1. Once cluster is ready, you'll see **"Get started"** modal
2. Click **"Skip"** on the quickstart
3. On the left sidebar, click **"Database Access"**
4. Click **"Add New Database User"**
5. Choose **"Password"** authentication
6. Fill in:
   - **Username**: `luxestate_admin` (or any name you prefer)
   - **Password**: Click **"Autogenerate Secure Password"** (COPY THIS PASSWORD!)
   - Or create your own strong password (save it somewhere safe!)
7. Under **"User Privileges"**: Select **"Read and write to any database"**
8. Click **"Add User"**

### 1.4 Configure Network Access
1. In left sidebar, click **"Network Access"**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (this adds `0.0.0.0/0`)
   - ⚠️ For production, you'd restrict this, but for now this is fine
4. Click **"Confirm"**

### 1.5 Get Connection String
1. In left sidebar, click **"Database"**
2. Click **"Connect"** button on your cluster
3. Select **"Connect your application"**
4. Choose **"Python"** and version **"3.6 or later"**
5. Copy the connection string - it looks like:
   ```
   mongodb+srv://luxestate_admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. **IMPORTANT**: Replace `<password>` with your actual database user password
7. Save this complete connection string - you'll need it next!

**✅ Step 1 Complete!** You now have:
- MongoDB Atlas cluster
- Database user credentials
- Connection string

---

## 📋 STEP 2: Deploy Backend to Railway (10 minutes)

### 2.1 Create Railway Account
1. Go to: **https://railway.app/**
2. Click **"Start a New Project"** or **"Login"**
3. Choose **"Login with GitHub"** (easiest option)
4. Authorize Railway to access your GitHub account

### 2.2 Create New Project
1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. You'll see your repositories - click **"luxestate-website"**
4. Railway will start importing your repo

### 2.3 Configure Service
1. Railway will create a service automatically
2. Click on your service (it might be named "luxestate-website" or "backend")
3. Click **"Settings"** tab
4. Find **"Root Directory"** and click **"Edit"**
5. Set it to: `backend`
6. Click **"Update"**

### 2.4 Set Environment Variables
1. Still in **"Settings"** tab, scroll to **"Variables"**
2. Click **"New Variable"** and add each of these one by one:

   **Variable 1:**
   - Name: `MONGO_URL`
   - Value: `mongodb+srv://luxestate_admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority`
   - (Replace YOUR_PASSWORD with your actual MongoDB password)
   - Click **"Add"**

   **Variable 2:**
   - Name: `DB_NAME`
   - Value: `luxestate`
   - Click **"Add"**

   **Variable 3:**
   - Name: `JWT_SECRET`
   - Value: `luxestate-secret-key-change-in-production-12345`
   - (Or generate a random string)
   - Click **"Add"**

   **Variable 4:**
   - Name: `CORS_ORIGINS`
   - Value: `*`
   - Click **"Add"**

### 2.5 Deploy
1. Railway will automatically detect changes and start deploying
2. You can watch the deployment in the **"Deployments"** tab
3. Wait for status to show **"Active"** (green checkmark)
4. Click **"Settings"** → **"Generate Domain"** to get a public URL
5. Copy your backend URL (e.g., `https://luxestate-backend-production.up.railway.app`)

### 2.6 Test Your Backend
1. Open your backend URL in browser (e.g., `https://your-backend.railway.app/api/properties`)
2. You should see JSON data (might be empty array `[]` if database not seeded yet)
3. If you see data or empty array, backend is working! ✅

**✅ Step 2 Complete!** Your backend is now deployed.

---

## 📋 STEP 3: Seed Database (2 minutes)

You need to populate your database with the 50 properties.

### Option A: Run Seed Script Locally (Easiest)
1. Open terminal on your Mac
2. Navigate to your project:
   ```bash
   cd /Users/raksh/luxestate-website/backend
   ```
3. Update your local `.env` file with MongoDB Atlas connection:
   ```bash
   # Edit backend/.env file
   MONGO_URL="mongodb+srv://luxestate_admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
   DB_NAME="luxestate"
   ```
   (Replace YOUR_PASSWORD with your actual password)

4. Run the seed script:
   ```bash
   python3 seed_properties.py
   ```
5. You should see:
   ```
   🌱 Starting property seeding...
   Creating seller users...
   Creating admin user...
   ✅ Successfully seeded 50 luxury properties!
   ```

6. Create admin user:
   ```bash
   python3 fix_admin_password.py
   ```

### Option B: Run via Railway CLI (Alternative)
1. Install Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```
2. Login:
   ```bash
   railway login
   ```
3. Navigate to backend:
   ```bash
   cd /Users/raksh/luxestate-website/backend
   ```
4. Link to Railway project:
   ```bash
   railway link
   ```
5. Run seed script:
   ```bash
   railway run python seed_properties.py
   railway run python fix_admin_password.py
   ```

**✅ Step 3 Complete!** Your database now has 50 properties and admin user.

---

## 📋 STEP 4: Deploy Frontend to Vercel (5 minutes)

### 4.1 Create Vercel Account
1. Go to: **https://vercel.com/**
2. Click **"Sign Up"** or **"Log In"**
3. Choose **"Continue with GitHub"**
4. Authorize Vercel to access your GitHub account

### 4.2 Import Project
1. In Vercel dashboard, click **"Add New Project"**
2. You'll see your GitHub repositories
3. Find and click **"luxestate-website"**
4. Click **"Import"**

### 4.3 Configure Project Settings
1. **Framework Preset**: Select **"Create React App"**
2. **Root Directory**: Click **"Edit"** and set to `frontend`
3. **Build Command**: Should auto-fill as `npm run build`
4. **Output Directory**: Should auto-fill as `build`
5. Click **"Override"** if you need to change these

### 4.4 Add Environment Variables
1. Scroll down to **"Environment Variables"**
2. Click **"Add"** next to each variable:

   **Variable 1:**
   - Key: `REACT_APP_BACKEND_URL`
   - Value: Your Railway backend URL (e.g., `https://luxestate-backend-production.up.railway.app`)
   - Environment: Select **Production, Preview, Development** (all three)
   - Click **"Add"**

### 4.5 Deploy
1. Scroll down and click **"Deploy"**
2. Wait for build to complete (2-3 minutes)
3. You'll see build logs in real-time
4. When complete, you'll see **"Success"** with your deployment URL

### 4.6 Get Your Live URL
1. After deployment, click on your project
2. You'll see your live URL (e.g., `https://luxestate-website.vercel.app`)
3. Click it to visit your live site! 🎉

**✅ Step 4 Complete!** Your frontend is now live!

---

## 🎉 Final Checklist

- [ ] MongoDB Atlas cluster created and running
- [ ] Database user created with password saved
- [ ] Network access configured (0.0.0.0/0)
- [ ] Connection string copied and password replaced
- [ ] Backend deployed to Railway
- [ ] Environment variables set in Railway
- [ ] Backend URL accessible and working
- [ ] Database seeded with 50 properties
- [ ] Admin user created (admin@luxestate.com / password123)
- [ ] Frontend deployed to Vercel
- [ ] Frontend environment variable set (REACT_APP_BACKEND_URL)
- [ ] Live site is working and showing properties

---

## 🔍 Testing Your Deployment

### Test Backend:
- Visit: `https://your-backend.railway.app/api/properties`
- Should return JSON with properties

### Test Frontend:
- Visit: `https://your-frontend.vercel.app`
- Should show homepage with properties
- Try logging in: `/login`
  - Email: `admin@luxestate.com`
  - Password: `password123`

---

## 🆘 Troubleshooting

### Backend Issues:
- **500 Error**: Check Railway logs in "Deployments" tab
- **Can't connect to MongoDB**: Verify MONGO_URL has correct password
- **CORS errors**: Make sure CORS_ORIGINS includes your frontend URL

### Frontend Issues:
- **Properties not loading**: Check REACT_APP_BACKEND_URL is correct
- **Build fails**: Check Vercel build logs
- **API calls fail**: Verify backend URL is accessible

### Database Issues:
- **Empty properties**: Run seed script again
- **Can't connect**: Check MongoDB network access settings

---

## 📞 Need Help?

If you get stuck at any step:
1. Check the error message carefully
2. Review the logs (Railway Deployments tab, Vercel Build logs)
3. Make sure all environment variables are set correctly
4. Verify MongoDB connection string has password replaced

**You're all set! 🚀**

