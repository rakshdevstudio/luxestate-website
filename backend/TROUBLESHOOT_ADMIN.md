# 🔧 Troubleshooting Admin Login

## ✅ Admin User Created!

The admin user has been successfully created in your MongoDB Atlas database:
- **Email**: `admin@luxestate.com`
- **Password**: `password123`
- **Role**: `admin`

## 🧪 Test Login

### Option 1: Test on Deployed Backend

1. Get your backend URL from Railway (e.g., `https://your-app.railway.app`)

2. Test login with curl:
   ```bash
   curl -X POST https://your-backend-url/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@luxestate.com", "password": "password123"}'
   ```

3. Or test in browser console:
   ```javascript
   fetch('https://your-backend-url/api/auth/login', {
     method: 'POST',
     headers: {'Content-Type': 'application/json'},
     body: JSON.stringify({
       email: 'admin@luxestate.com',
       password: 'password123'
     })
   }).then(r => r.json()).then(console.log)
   ```

### Option 2: Test on Frontend

1. Go to your deployed frontend login page
2. Enter:
   - Email: `admin@luxestate.com`
   - Password: `password123`
3. Click login

## 🔍 Common Issues

### Issue: "Invalid credentials"

**Possible causes:**
1. Backend is connecting to wrong database
   - **Fix**: Check `DB_NAME` environment variable in Railway matches your database name
   
2. Admin user doesn't exist in database
   - **Fix**: Run `python3 create_admin_remote.py` again
   
3. CORS issues
   - **Fix**: Make sure `CORS_ORIGINS` in Railway includes your frontend URL or is set to `*`

### Issue: "Network error" or "Failed to fetch"

**Possible causes:**
1. Backend URL is wrong in frontend
   - **Fix**: Check `REACT_APP_BACKEND_URL` in Vercel matches your Railway backend URL
   
2. Backend is down
   - **Fix**: Check Railway dashboard to see if deployment is active

3. Backend URL has trailing slash
   - **Fix**: Make sure URL doesn't end with `/` (should be `https://backend.railway.app`, not `https://backend.railway.app/`)

### Issue: Login works but redirects incorrectly

**Fix**: Check your frontend login logic in `LoginPage.js` - it should redirect to `/admin` for admin users.

## 🛠️ Recreate Admin User

If you need to recreate the admin user:

```bash
cd backend
python3 create_admin_remote.py
```

Or use the fix script:

```bash
cd backend
python3 fix_admin_password.py
```

## ✅ Verify Admin User Exists

Check if admin exists in database:

```python
# Run this locally with your .env pointing to Atlas
python3 -c "
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path('backend') / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

async def check():
    admin = await db.users.find_one({'email': 'admin@luxestate.com'})
    if admin:
        print('✅ Admin user found!')
        print(f'   Email: {admin[\"email\"]}')
        print(f'   Role: {admin[\"role\"]}')
    else:
        print('❌ Admin user NOT found')
    client.close()

asyncio.run(check())
"
```

## 📞 Still Having Issues?

1. Check Railway logs: Go to Railway dashboard → Your service → Deployments → View logs
2. Check browser console: Open DevTools (F12) → Console tab
3. Verify environment variables are set correctly in both Railway and Vercel


