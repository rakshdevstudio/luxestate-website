#!/usr/bin/env python3
"""
Luxestate Property Seeder Script
Seeds the database with 50 luxury properties using high-quality images from Unsplash.
"""

import asyncio
import random
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

# High-quality property images from Unsplash & Pexels
# Using curated premium images with high resolution (1920px width, quality 90+)

VILLA_IMAGES = [
    "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=1920&q=95",
    "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1920&q=95",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1920&q=95",
    "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1920&q=95",
    "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=1920&q=95",
    "https://images.unsplash.com/photo-1600573472556-e636c2acda88?w=1920&q=95",
    "https://images.unsplash.com/photo-1613977257363-707ba9348227?w=1920&q=95",
    "https://images.unsplash.com/photo-1600607687644-c7171b42498f?w=1920&q=95",
    "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=1920&q=95",
    "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=1920&q=95",
    "https://images.pexels.com/photos/1396122/pexels-photo-1396122.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/1396132/pexels-photo-1396132.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/1396134/pexels-photo-1396134.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/323775/pexels-photo-323775.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/1571458/pexels-photo-1571458.jpeg?auto=compress&cs=tinysrgb&w=1920",
]

PENTHOUSE_IMAGES = [
    "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=1920&q=95",
    "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=1920&q=95",
    "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=1920&q=95",
    "https://images.unsplash.com/photo-1560185007-cde436f6a4d0?w=1920&q=95",
    "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=1920&q=95",
    "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=1920&q=95",
    "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=1920&q=95",
    "https://images.unsplash.com/photo-1560448075-bb485b067938?w=1920&q=95",
    "https://images.unsplash.com/photo-1560185127-6a8f6b13c537?w=1920&q=95",
    "https://images.unsplash.com/photo-1560184897-ae75f418493e?w=1920&q=95",
    "https://images.pexels.com/photos/245240/pexels-photo-245240.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/245247/pexels-photo-245247.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/271743/pexels-photo-271743.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/271816/pexels-photo-271816.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/271743/pexels-photo-271743.jpeg?auto=compress&cs=tinysrgb&w=1920",
]

MANSION_IMAGES = [
    "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=1920&q=95",
    "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=1920&q=95",
    "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=1920&q=95",
    "https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=1920&q=95",
    "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=1920&q=95",
    "https://images.unsplash.com/photo-1600585154363-67eb9e2e2099?w=1920&q=95",
    "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=1920&q=95",
    "https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?w=1920&q=95",
    "https://images.unsplash.com/photo-1600585152220-90363fe7e115?w=1920&q=95",
    "https://images.unsplash.com/photo-1600573472591-ee6b68d14c68?w=1920&q=95",
    "https://images.pexels.com/photos/1396132/pexels-photo-1396132.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos-1571453/pexels-photo-1571453.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/1396134/pexels-photo-1396134.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/280222/pexels-photo-280222.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/323775/pexels-photo-323775.jpeg?auto=compress&cs=tinysrgb&w=1920",
]

ESTATE_IMAGES = [
    "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1920&q=95",
    "https://images.unsplash.com/photo-1600607687644-c7171b42498f?w=1920&q=95",
    "https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?w=1920&q=95",
    "https://images.unsplash.com/photo-1600585152220-90363fe7e115?w=1920&q=95",
    "https://images.unsplash.com/photo-1600573472591-ee6b68d14c68?w=1920&q=95",
    "https://images.unsplash.com/photo-1600121848594-d8644e57abab?w=1920&q=95",
    "https://images.unsplash.com/photo-1600585154084-4e5fe7c39198?w=1920&q=95",
    "https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?w=1920&q=95",
    "https://images.pexels.com/photos/1396122/pexels-photo-1396122.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/1396132/pexels-photo-1396132.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/1571458/pexels-photo-1571458.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/323775/pexels-photo-323775.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos-1571453/pexels-photo-1571453.jpeg?auto=compress&cs=tinysrgb&w=1920",
]

APARTMENT_IMAGES = [
    "https://images.unsplash.com/photo-1502672023488-70e25813eb80?w=1920&q=95",
    "https://images.unsplash.com/photo-1560448075-bb485b067938?w=1920&q=95",
    "https://images.unsplash.com/photo-1560185127-6a8f6b13c537?w=1920&q=95",
    "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=1920&q=95",
    "https://images.unsplash.com/photo-1554995207-c18c203602cb?w=1920&q=95",
    "https://images.unsplash.com/photo-1502005229766-31cb065ac472?w=1920&q=95",
    "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=1920&q=95",
    "https://images.unsplash.com/photo-1560184897-ae75f418493e?w=1920&q=95",
    "https://images.pexels.com/photos/245240/pexels-photo-245240.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/271743/pexels-photo-271743.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/271816/pexels-photo-271816.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/245247/pexels-photo-245247.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/276583/pexels-photo-276583.jpeg?auto=compress&cs=tinysrgb&w=1920",
]

INTERIOR_IMAGES = [
    "https://images.unsplash.com/photo-1600210491892-03d54c0aaf87?w=1920&q=95",
    "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=1920&q=95",
    "https://images.unsplash.com/photo-1600566753104-685f4f24cb4d?w=1920&q=95",
    "https://images.unsplash.com/photo-1600585153490-76fb20a32601?w=1920&q=95",
    "https://images.unsplash.com/photo-1600573472599-7510137a8421?w=1920&q=95",
    "https://images.unsplash.com/photo-1600121771843-5b725c452291?w=1920&q=95",
    "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=1920&q=95",
    "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=1920&q=95",
    "https://images.pexels.com/photos-271743/pexels-photo-271743.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/271816/pexels-photo-271816.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/245240/pexels-photo-245240.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "https://images.pexels.com/photos/276583/pexels-photo-276583.jpeg?auto=compress&cs=tinysrgb&w=1920",
]

# Property templates with descriptions
VILLA_TEMPLATES = [
    {
        "title": "Mediterranean Villa Estate",
        "description": "Stunning Mediterranean-style villa featuring panoramic ocean views, imported Italian marble floors, and a resort-style infinity pool. This exceptional property offers the ultimate in luxury coastal living with meticulously landscaped gardens and private beach access.",
        "features": ["Ocean Views", "Infinity Pool", "Smart Home", "Wine Cellar", "Home Theater"]
    },
    {
        "title": "Contemporary Hillside Villa",
        "description": "Architectural masterpiece perched atop the hills with breathtaking city views. Floor-to-ceiling windows flood the space with natural light, while the open floor plan seamlessly blends indoor and outdoor living areas.",
        "features": ["City Views", "Glass Walls", "Rooftop Deck", "Gourmet Kitchen", "Spa"]
    },
    {
        "title": "Tuscan Villa Retreat",
        "description": "Authentic Tuscan villa with rustic charm and modern amenities. Features include hand-painted tiles, beamed ceilings, a professional chef's kitchen, and a sparkling pool surrounded by olive trees and lavender gardens.",
        "features": ["Pool", "Olive Grove", "Guest House", "Chef's Kitchen", "Stone Terraces"]
    },
    {
        "title": "Beachfront Paradise Villa",
        "description": "Direct beachfront villa with white sand steps from your door. This coastal gem features tropical landscaping, a private cabana, outdoor kitchen, and expansive decks perfect for sunset entertaining.",
        "features": ["Beach Access", "Private Beach", "Cabana", "Outdoor Kitchen", "Dock"]
    },
    {
        "title": "Modern Luxury Villa",
        "description": "Sleek contemporary design meets comfort in this stunning modern villa. With clean lines, an open concept living area, and premium finishes throughout, this home is perfect for those who appreciate sophisticated design.",
        "features": ["Modern Design", "Pool", "Gym", "Office", "Elevator"]
    },
]

PENTHOUSE_TEMPLATES = [
    {
        "title": "Skyline Penthouse Suite",
        "description": "Exquisite penthouse offering 360-degree views of the glittering city skyline. This sophisticated residence features private elevator access, a wraparound terrace, and interior finishes that rival the world's finest hotels.",
        "features": ["City Views", "Private Terrace", "Concierge", "Wine Room", "Smart Home"]
    },
    {
        "title": "Luxury High-Rise Penthouse",
        "description": "Spectacular penthouse living with floor-to-ceiling windows and unobstructed views. Features include a chef's kitchen with top-of-the-line appliances, spa-like bathrooms, and a private rooftop oasis.",
        "features": ["Panoramic Views", "Rooftop Pool", "Fitness Center", "Valet Parking", "Doorman"]
    },
    {
        "title": "Urban Sanctuary Penthouse",
        "description": "An urban sanctuary perched high above the city. This meticulously designed penthouse offers seamless indoor-outdoor flow, custom millwork, and every conceivable luxury amenity for the discerning buyer.",
        "features": ["Private Garden", "Home Office", "Wine Storage", "Heated Floors", "Security"]
    },
    {
        "title": "Waterfront Penthouse Residence",
        "description": "Experience waterfront living at its finest in this stunning penthouse. Watch yachts glide by from your expansive terrace while enjoying the sophisticated interior design and premium finishes.",
        "features": ["Waterfront", "Marina Access", "Wraparound Balcony", "Chef's Kitchen", "Spa Bath"]
    },
    {
        "title": "Modern Sky Penthouse",
        "description": "Cutting-edge design defines this remarkable penthouse. Featuring an open floor plan, custom Italian furniture, and state-of-the-art technology, this residence represents the pinnacle of modern luxury living.",
        "features": ["Sky Views", "Smart Home", "Art Gallery Space", "Wine Cellar", "Private Gym"]
    },
]

MANSION_TEMPLATES = [
    {
        "title": "Gated Estate Mansion",
        "description": "Impressive gated estate spanning multiple acres. This magnificent mansion features grand reception rooms, a gourmet kitchen, wine cellar, home theater, and resort-style outdoor amenities including a pool and tennis court.",
        "features": ["Tennis Court", "Pool House", "Theater", "Wine Cellar", "Guest Quarters"]
    },
    {
        "title": "Coastal Mansion Masterpiece",
        "description": "Iconic coastal mansion with sweeping ocean views from nearly every room. The impeccable design seamlessly combines elegance with comfort, featuring custom details and the finest materials throughout.",
        "features": ["Ocean Views", "Pool", "Beach House", "Chef's Kitchen", "Library"]
    },
    {
        "title": "Grand Estate Residence",
        "description": "A grand estate of unparalleled distinction. This remarkable property offers an abundance of space and amenities including a separate guest house, staff quarters, horse facilities, and manicured grounds.",
        "features": ["Horse Facilities", "Guest House", "Staff Quarters", "Formal Gardens", "Stables"]
    },
    {
        "title": "Historic Mansion Estate",
        "description": "Meticulously restored historic mansion blending original architectural details with modern luxury. Features include ornate moldings, hardwood floors, a gourmet kitchen, and beautifully appointed entertaining spaces.",
        "features": ["Historic Character", "Original Details", "Gardens", "Wine Cellar", "Carriage House"]
    },
    {
        "title": "Contemporary Mansion Estate",
        "description": "Stunning contemporary mansion on a private lot with mountain views. This architectural tour de force features walls of glass, dramatic ceilings, and a seamless integration with the stunning natural surroundings.",
        "features": ["Mountain Views", "Pool", "Guest House", "Home Theater", "Wine Room"]
    },
]

ESTATE_TEMPLATES = [
    {
        "title": "Private Country Estate",
        "description": "Secluded country estate offering privacy and tranquility. The property features a main residence, separate guest house, equestrian facilities, and acres of professionally landscaped grounds with mature trees and rolling lawns.",
        "features": ["Equestrian Center", "Guest House", "Pool", "Tennis Court", "Orchard"]
    },
    {
        "title": "Vineyard Estate Property",
        "description": "Picturesque vineyard estate with producing vines and a charming tasting room. The property includes a beautifully renovated main home, guest cottage, and potential for winery operations.",
        "features": ["Vineyard", "Tasting Room", "Cottage", "Wine Production", "Event Space"]
    },
    {
        "title": "Ranch Estate Retreat",
        "description": "Magnificent ranch estate with panoramic mountain and valley views. This working ranch features luxury accommodations, horse facilities, hiking trails, and every amenity for the ultimate retreat experience.",
        "features": ["Mountain Views", "Horse Facilities", "Hiking Trails", "Guest Lodge", "Pool"]
    },
    {
        "title": "Waterfront Estate Compound",
        "description": "Extraordinary waterfront estate with over 200 feet of water frontage. The compound includes a main residence, guest house, private dock, and resort-style outdoor living spaces.",
        "features": ["Waterfront", "Private Dock", "Guest House", "Pool", "Boat House"]
    },
    {
        "title": "Heritage Estate Property",
        "description": "Prestigious heritage estate with a rich history. The property has been thoughtfully updated while preserving its historic character, featuring antique details alongside modern luxury amenities.",
        "features": ["Historic Estate", "Formal Gardens", "Guest House", "Pool", "Event Venue"]
    },
]

APARTMENT_TEMPLATES = [
    {
        "title": "Luxury Downtown Apartment",
        "description": "Sophisticated urban living in this meticulously designed downtown apartment. Features include designer finishes, an open kitchen with premium appliances, and stunning city views from every room.",
        "features": ["City Views", "Concierge", "Fitness Center", "Rooftop Pool", "Parking"]
    },
    {
        "title": "Waterfront Luxury Residence",
        "description": "Stunning waterfront residence with floor-to-ceiling windows showcasing breathtaking water views. The interior features premium finishes, a gourmet kitchen, and spacious living areas perfect for entertaining.",
        "features": ["Water Views", "Marina Access", "Balcony", "Gym", "Valet"]
    },
    {
        "title": "Modern Urban Loft",
        "description": "Stylish modern loft in the heart of the city with soaring ceilings and industrial-chic design elements. Features include an open floor plan, chef's kitchen, and access to premier building amenities.",
        "features": ["High Ceilings", "Open Concept", "Industrial Style", "Rooftop Deck", "Doorman"]
    },
    {
        "title": "Elegant High-Rise Residence",
        "description": "Elegant high-rise residence offering refined urban living. This meticulously appointed apartment features custom finishes, a spa-like master bath, and panoramic views from its privileged position.",
        "features": ["Panoramic Views", "Spa Bathroom", "Walk-in Closet", "Wine Storage", "Pet Friendly"]
    },
    {
        "title": "Designer Furnished Apartment",
        "description": "Professionally designed furnished apartment in a premier building. Every detail has been carefully curated to create a luxurious and comfortable living space with hotel-style amenities.",
        "features": ["Furnished", "Designer Decor", "Building Gym", "Pool", "24/7 Security"]
    },
]

# Locations with neighborhoods
LOCATIONS = [
    {"city": "Beverly Hills, CA", "neighborhoods": ["Beverly Hills", "The Flats", "Beverly Park", "Mulholland Drive"]},
    {"city": "Miami, FL", "neighborhoods": ["Miami Beach", "Coconut Grove", "Coral Gables", "Key Biscayne"]},
    {"city": "New York, NY", "neighborhoods": ["Tribeca", "SoHo", "Upper East Side", "Chelsea"]},
    {"city": "Malibu, CA", "neighborhoods": ["Malibu Colony", "Carbon Beach", "Broad Beach", "Point Dume"]},
    {"city": "San Francisco, CA", "neighborhoods": ["Pacific Heights", "Marina District", "Russian Hill", "Sea Cliff"]},
    {"city": "Los Angeles, CA", "neighborhoods": ["Bel Air", "Holmby Hills", "Brentwood", "Westwood"]},
    {"city": "Aspen, CO", "neighborhoods": ["Aspen Mountain", "Red Mountain", "Smuggler", "West End"]},
    {"city": "Hamptons, NY", "neighborhoods": ["East Hampton", "Southampton", "Montauk", "Sagaponack"]},
    {"city": "Palm Beach, FL", "neighborhoods": ["Palm Beach", "Manalapan", "Ocean Ridge", "Hypoluxo"]},
    {"city": "Montecito, CA", "neighborhoods": ["Lower Village", "Upper Village", "Cold Spring", "San Ysidro"]},
]

# Price ranges by property type
PRICE_RANGES = {
    "villa": {"min": 2500000, "max": 12000000},
    "penthouse": {"min": 3000000, "max": 15000000},
    "mansion": {"min": 5000000, "max": 20000000},
    "estate": {"min": 4000000, "max": 18000000},
    "apartment": {"min": 500000, "max": 3500000},
}

# Bedroom/bathroom configurations
BEDROOM_CONFIGURATIONS = {
    "villa": {"bedrooms": (4, 7), "bathrooms": (4, 7), "area": (3500, 8500)},
    "penthouse": {"bedrooms": (2, 5), "bathrooms": (2, 5), "area": (1500, 5000)},
    "mansion": {"bedrooms": (6, 10), "bathrooms": (6, 9), "area": (6000, 15000)},
    "estate": {"bedrooms": (5, 9), "bathrooms": (5, 8), "area": (5000, 12000)},
    "apartment": {"bedrooms": (1, 3), "bathrooms": (1, 3), "area": (800, 2500)},
}

# Image galleries for each property type
IMAGE_GALLERIES = {
    "villa": VILLA_IMAGES,
    "penthouse": PENTHOUSE_IMAGES,
    "mansion": MANSION_IMAGES,
    "estate": ESTATE_IMAGES,
    "apartment": APARTMENT_IMAGES,
}

def generate_property_images(property_type, count=8):
    """Generate a list of high-quality property images."""
    base_images = IMAGE_GALLERIES.get(property_type, APARTMENT_IMAGES)
    # Add some interior images for variety
    all_images = base_images + INTERIOR_IMAGES
    # Shuffle and select unique images
    random.shuffle(all_images)
    selected = []
    seen = set()
    for img in all_images:
        if img not in seen:
            selected.append(img)
            seen.add(img)
        if len(selected) >= count:
            break
    
    # Ensure we have at least count images
    while len(selected) < count:
        selected.append(random.choice(all_images))
    
    return selected[:count]

def create_property(property_type, template, location, seller_id):
    """Create a single property from template."""
    config = BEDROOM_CONFIGURATIONS[property_type]
    prices = PRICE_RANGES[property_type]
    
    bedrooms = random.randint(*config["bedrooms"])
    bathrooms = random.randint(*config["bathrooms"])
    area = random.randint(*config["area"])
    price = round(random.uniform(prices["min"], prices["max"]), -5)
    
    neighborhood = random.choice(location["neighborhoods"])
    full_location = f"{neighborhood}, {location['city']}"
    
    # Generate 8 high-quality images per property
    images = generate_property_images(property_type, 8)
    
    features = template["features"]
    
    description = template["description"] + f"\n\nAdditional Features:\n" + "\n".join([f"• {feature}" for feature in features])
    
    return {
        "id": str(uuid.uuid4()),
        "title": template["title"],
        "description": description,
        "price": price,
        "location": full_location,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "area": area,
        "property_type": property_type,
        "images": images,
        "status": "approved",
        "seller_id": seller_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

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
        {"id": admin_id, "email": "admin@luxestate.com"},
        {"$set": admin},
        upsert=True
    )
    return admin_id

async def create_seller_users(count=5):
    """Create sample seller users for the properties."""
    sellers = []
    seller_names = [
        "Luxury Estates Group",
        "Premium Properties Inc.",
        "Elite Real Estate Advisors",
        "Coastal Living Realty",
        "Urban Luxury Brokers"
    ]
    
    for i in range(count):
        seller_id = str(uuid.uuid4())
        seller = {
            "id": seller_id,
            "email": f"seller{i+1}@luxestate.com",
            "name": seller_names[i],
            "role": "seller",
            "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dW8KIuJ3eHFfTi",  # "password123"
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.update_one(
            {"id": seller_id},
            {"$set": seller},
            upsert=True
        )
        sellers.append(seller_id)
    
    return sellers

async def seed_properties():
    """Seed the database with 50 properties."""
    print("🌱 Starting property seeding...")
    
    # Create admin user
    print("Creating admin user...")
    admin_id = await create_admin_user()
    print(f"✅ Admin user created: admin@luxestate.com")
    
    # Create seller users
    print("Creating seller users...")
    sellers = await create_seller_users(5)
    
    # Property type distribution
    property_distribution = {
        "villa": 15,
        "penthouse": 10,
        "mansion": 10,
        "estate": 8,
        "apartment": 7,
    }
    
    templates = {
        "villa": VILLA_TEMPLATES,
        "penthouse": PENTHOUSE_TEMPLATES,
        "mansion": MANSION_TEMPLATES,
        "estate": ESTATE_TEMPLATES,
        "apartment": APARTMENT_TEMPLATES,
    }
    
    properties_to_insert = []
    property_id = 1
    
    for property_type, count in property_distribution.items():
        print(f"Creating {count} {property_type} properties...")
        type_templates = templates[property_type]
        
        for i in range(count):
            template = random.choice(type_templates)
            location = random.choice(LOCATIONS)
            seller_id = random.choice(sellers)
            
            # Add unique identifier to title
            title_suffix = f" - Property #{property_id}"
            template_copy = template.copy()
            template_copy["title"] = template["title"] + title_suffix
            
            property_data = create_property(
                property_type,
                template_copy,
                location,
                seller_id
            )
            properties_to_insert.append(property_data)
            property_id += 1
    
    # Insert all properties
    print(f"Inserting {len(properties_to_insert)} properties into database...")
    for prop in properties_to_insert:
        await db.properties.update_one(
            {"id": prop["id"]},
            {"$set": prop},
            upsert=True
        )
    
    print(f"✅ Successfully seeded {len(properties_to_insert)} luxury properties!")
    print(f"📍 Properties include villas, penthouses, mansions, estates, and apartments")
    print(f"🏙️ Located in top markets: Beverly Hills, Miami, NYC, Malibu, and more")
    
    return properties_to_insert

async def verify_seeding():
    """Verify the seeding was successful."""
    total = await db.properties.count_documents({})
    approved = await db.properties.count_documents({"status": "approved"})
    pending = await db.properties.count_documents({"status": "pending"})
    
    print(f"\n📊 Database Statistics:")
    print(f"   Total Properties: {total}")
    print(f"   Approved: {approved}")
    print(f"   Pending: {pending}")
    
    # Count by property type
    print(f"\n📈 Properties by Type:")
    for ptype in ["villa", "penthouse", "mansion", "estate", "apartment"]:
        count = await db.properties.count_documents({"property_type": ptype})
        print(f"   {ptype.capitalize()}: {count}")
    
    return {"total": total, "approved": approved, "pending": pending}

async def main():
    """Main function to run the seeder."""
    try:
        await seed_properties()
        await verify_seeding()
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())

