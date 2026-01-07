from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok", "service": "luxestate-backend"}

api_router = APIRouter(prefix="/api")
security = HTTPBearer()

JWT_SECRET = os.environ.get('JWT_SECRET', 'luxestate-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'

# Models
class UserRole(str):
    ADMIN = 'admin'
    SELLER = 'seller'
    CLIENT = 'client'

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    name: str
    role: str = 'client'
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: Optional[str] = 'client'

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str
    user: User

class Property(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    price: float
    location: str
    bedrooms: int
    bathrooms: int
    area: float
    property_type: str
    images: List[str]
    status: str = 'pending'
    seller_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PropertyCreate(BaseModel):
    title: str
    description: str
    price: float
    location: str
    bedrooms: int
    bathrooms: int
    area: float
    property_type: str
    images: List[str]

class PropertyUpdate(BaseModel):
    status: str

class Lead(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    property_id: str
    name: str
    email: EmailStr
    phone: str
    message: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LeadCreate(BaseModel):
    property_id: str
    name: str
    email: EmailStr
    phone: str
    message: str

class Analytics(BaseModel):
    total_properties: int
    approved_properties: int
    pending_properties: int
    total_users: int
    total_leads: int

# Auth helpers
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id: str) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(days=7)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get('user_id')
        user_doc = await db.users.find_one({'id': user_id}, {'_id': 0})
        if not user_doc:
            raise HTTPException(status_code=401, detail='User not found')
        return User(**user_doc)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid token')

# Auth routes
@api_router.post('/auth/register', response_model=TokenResponse)
async def register(user_input: UserCreate):
    existing = await db.users.find_one({'email': user_input.email}, {'_id': 0})
    if existing:
        raise HTTPException(status_code=400, detail='Email already registered')
    
    user = User(
        email=user_input.email,
        name=user_input.name,
        role=user_input.role
    )
    user_dict = user.model_dump()
    user_dict['password'] = hash_password(user_input.password)
    user_dict['created_at'] = user_dict['created_at'].isoformat()
    
    await db.users.insert_one(user_dict)
    token = create_token(user.id)
    return TokenResponse(token=token, user=user)

@api_router.post('/auth/login', response_model=TokenResponse)
async def login(login_input: UserLogin):
    user_doc = await db.users.find_one({'email': login_input.email}, {'_id': 0})
    if not user_doc or not verify_password(login_input.password, user_doc['password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    if isinstance(user_doc['created_at'], str):
        user_doc['created_at'] = datetime.fromisoformat(user_doc['created_at'])
    
    user = User(**user_doc)
    token = create_token(user.id)
    return TokenResponse(token=token, user=user)

@api_router.get('/auth/me', response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# Property routes
@api_router.post('/properties', response_model=Property)
async def create_property(property_input: PropertyCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in ['seller', 'admin']:
        raise HTTPException(status_code=403, detail='Only sellers can create properties')
    
    prop = Property(**property_input.model_dump(), seller_id=current_user.id)
    prop_dict = prop.model_dump()
    prop_dict['created_at'] = prop_dict['created_at'].isoformat()
    prop_dict['updated_at'] = prop_dict['updated_at'].isoformat()
    
    await db.properties.insert_one(prop_dict)
    return prop

@api_router.get('/properties', response_model=List[Property])
async def get_properties(
    status: Optional[str] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    bedrooms: Optional[int] = None,
    location: Optional[str] = None
):
    query = {}
    if status:
        query['status'] = status
    if property_type:
        query['property_type'] = property_type
    if min_price is not None:
        query['price'] = query.get('price', {})
        query['price']['$gte'] = min_price
    if max_price is not None:
        query['price'] = query.get('price', {})
        query['price']['$lte'] = max_price
    if bedrooms is not None:
        query['bedrooms'] = bedrooms
    if location:
        query['location'] = {'$regex': location, '$options': 'i'}
    
    properties = await db.properties.find(query, {'_id': 0}).to_list(1000)
    for prop in properties:
        if isinstance(prop['created_at'], str):
            prop['created_at'] = datetime.fromisoformat(prop['created_at'])
        if isinstance(prop['updated_at'], str):
            prop['updated_at'] = datetime.fromisoformat(prop['updated_at'])
    
    return properties

@api_router.get('/properties/seller', response_model=List[Property])
async def get_seller_properties(current_user: User = Depends(get_current_user)):
    properties = await db.properties.find({'seller_id': current_user.id}, {'_id': 0}).to_list(1000)
    for prop in properties:
        if isinstance(prop['created_at'], str):
            prop['created_at'] = datetime.fromisoformat(prop['created_at'])
        if isinstance(prop['updated_at'], str):
            prop['updated_at'] = datetime.fromisoformat(prop['updated_at'])
    return properties

@api_router.get('/properties/{property_id}', response_model=Property)
async def get_property(property_id: str):
    prop = await db.properties.find_one({'id': property_id}, {'_id': 0})
    if not prop:
        raise HTTPException(status_code=404, detail='Property not found')
    
    if isinstance(prop['created_at'], str):
        prop['created_at'] = datetime.fromisoformat(prop['created_at'])
    if isinstance(prop['updated_at'], str):
        prop['updated_at'] = datetime.fromisoformat(prop['updated_at'])
    
    return Property(**prop)

@api_router.patch('/properties/{property_id}', response_model=Property)
async def update_property_status(property_id: str, update: PropertyUpdate, current_user: User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='Only admins can update property status')
    
    result = await db.properties.find_one_and_update(
        {'id': property_id},
        {'$set': {'status': update.status, 'updated_at': datetime.now(timezone.utc).isoformat()}},
        return_document=True,
        projection={'_id': 0}
    )
    
    if not result:
        raise HTTPException(status_code=404, detail='Property not found')
    
    if isinstance(result['created_at'], str):
        result['created_at'] = datetime.fromisoformat(result['created_at'])
    if isinstance(result['updated_at'], str):
        result['updated_at'] = datetime.fromisoformat(result['updated_at'])
    
    return Property(**result)

# Lead routes
@api_router.post('/leads', response_model=Lead)
async def create_lead(lead_input: LeadCreate):
    lead = Lead(**lead_input.model_dump())
    lead_dict = lead.model_dump()
    lead_dict['created_at'] = lead_dict['created_at'].isoformat()
    
    await db.leads.insert_one(lead_dict)
    return lead

@api_router.get('/leads', response_model=List[Lead])
async def get_leads(current_user: User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='Only admins can view leads')
    
    leads = await db.leads.find({}, {'_id': 0}).to_list(1000)
    for lead in leads:
        if isinstance(lead['created_at'], str):
            lead['created_at'] = datetime.fromisoformat(lead['created_at'])
    
    return leads

# User management
@api_router.get('/users', response_model=List[User])
async def get_users(current_user: User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='Only admins can view users')
    
    users = await db.users.find({}, {'_id': 0, 'password': 0}).to_list(1000)
    for user in users:
        if isinstance(user['created_at'], str):
            user['created_at'] = datetime.fromisoformat(user['created_at'])
    
    return users

# Analytics
@api_router.get('/analytics', response_model=Analytics)
async def get_analytics(current_user: User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='Only admins can view analytics')
    
    total_properties = await db.properties.count_documents({})
    approved_properties = await db.properties.count_documents({'status': 'approved'})
    pending_properties = await db.properties.count_documents({'status': 'pending'})
    total_users = await db.users.count_documents({})
    total_leads = await db.leads.count_documents({})
    
    return Analytics(
        total_properties=total_properties,
        approved_properties=approved_properties,
        pending_properties=pending_properties,
        total_users=total_users,
        total_leads=total_leads
    )

app.include_router(api_router)

# Explicit app-level alias to ensure /api/properties is reachable
@app.get("/api/properties", response_model=List[Property])
async def get_properties_alias(
    status: Optional[str] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    bedrooms: Optional[int] = None,
    location: Optional[str] = None
):
    query = {}
    if status:
        query['status'] = status
    if property_type:
        query['property_type'] = property_type
    if min_price is not None:
        query['price'] = query.get('price', {})
        query['price']['$gte'] = min_price
    if max_price is not None:
        query['price'] = query.get('price', {})
        query['price']['$lte'] = max_price
    if bedrooms is not None:
        query['bedrooms'] = bedrooms
    if location:
        query['location'] = {'$regex': location, '$options': 'i'}

    properties = await db.properties.find(query, {'_id': 0}).to_list(1000)
    for prop in properties:
        if isinstance(prop['created_at'], str):
            prop['created_at'] = datetime.fromisoformat(prop['created_at'])
        if isinstance(prop['updated_at'], str):
            prop['updated_at'] = datetime.fromisoformat(prop['updated_at'])

    return properties

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("server:app", host="0.0.0.0", port=port)