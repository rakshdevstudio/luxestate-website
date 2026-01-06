# Luxestate Property Seeder

This directory contains the seed script that populates your Luxestate application with 50 luxury properties.

## What's Included

### 50 Luxury Properties Across 5 Categories:
- **Villas** (15 properties) - Mediterranean, Contemporary, Tuscan, Beachfront, Modern
- **Penthouses** (10 properties) - Skyline, High-rise, Urban, Waterfront, Modern
- **Mansions** (10 properties) - Gated, Coastal, Grand, Historic, Contemporary
- **Estates** (8 properties) - Country, Vineyard, Ranch, Waterfront, Heritage
- **Apartments** (7 properties) - Downtown, Waterfront, Modern Loft, High-rise, Designer

### Property Details:
- High-quality images from Unsplash & Pexels (8 images per property at 1920px resolution)
- Realistic prices ($500,000 - $20,000,000)
- Varied bedroom counts (1-10 beds)
- Varied bathroom counts (1-9 baths)
- Square footage from 800 to 15,000 sq ft
- Status: 'approved' (visible in listings immediately)

### Locations:
- Beverly Hills, CA
- Miami, FL
- New York, NY
- Malibu, CA
- San Francisco, CA
- Los Angeles, CA
- Aspen, CO
- Hamptons, NY
- Palm Beach, FL
- Montecito, CA

## Running the Seeder

### Prerequisites:
1. MongoDB running and accessible
2. Environment variables set in `backend/.env`:
   ```
   MONGO_URL=mongodb://localhost:27017
   DB_NAME=luxestate
   JWT_SECRET=your-secret-key
   ```

### Run the seeder:
```bash
cd backend
python seed_properties.py
```

### Expected Output:
```
🌱 Starting property seeding...
Creating seller users...
Creating 15 villa properties...
Creating 10 penthouse properties...
Creating 10 mansion properties...
Creating 8 estate properties...
Creating 7 apartment properties...
Inserting 50 properties into database...
✅ Successfully seeded 50 luxury properties!
📍 Properties include villas, penthouses, mansions, estates, and apartments
🏙️ Located in top markets: Beverly Hills, Miami, NYC, Malibu, and more

📊 Database Statistics:
   Total Properties: 50
   Approved: 50
   Pending: 0

📈 Properties by Type:
   Villa: 15
   Penthouse: 10
   Mansion: 10
   Estate: 8
   Apartment: 7
```

## What Gets Created

### Seller Users:
5 seller accounts are created for property attribution:
- seller1@luxestate.com
- seller2@luxestate.com
- seller3@luxestate.com
- seller4@luxestate.com
- seller5@luxestate.com

**Password for all: `password123`**

### Images:
Each property gets 8 high-quality images (1920px resolution) from Unsplash & Pexels:
- Main exterior shots (multiple angles)
- Interior living spaces
- Kitchen
- Bedroom(s)
- Bathroom(s)
- Pool/outdoor spaces
- Additional feature shots
- Detailed interior views

## API Endpoints

After seeding, your API will return these properties at:
- `GET /api/properties` - List all approved properties
- `GET /api/properties?status=approved` - Filter by status
- `GET /api/properties?property_type=villa` - Filter by type
- `GET /api/properties?min_price=1000000&max_price=5000000` - Price range
- `GET /api/properties?bedrooms=4` - Bedroom filter
- `GET /api/properties/{id}` - Single property details

## Re-seeding

To clear existing properties and re-seed:

```bash
# From MongoDB shell
use luxestate
db.properties.drop()
db.users.drop()  # This will also remove seller accounts

# Then run the seeder again
python seed_properties.py
```

