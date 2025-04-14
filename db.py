# db.py
venue_db = [
    {
        "id": 1,
        "name": "Grand Ballroom",
        "type": "Indoor",
        "capacity": 500,
        "location": "Downtown",
        "amenities": ["Stage", "Sound System", "Lighting", "Catering Kitchen"],
        "price_range": "High",
        "available_times": ["09:00-23:00"],
        "setup_time": "2 hours",
        "teardown_time": "1 hour"
    },
    {
        "id": 2,
        "name": "Garden Pavilion",
        "type": "Outdoor",
        "capacity": 300,
        "location": "City Park",
        "amenities": ["Tent", "Dance Floor", "Outdoor Lighting", "Restrooms"],
        "price_range": "Medium",
        "available_times": ["10:00-22:00"],
        "setup_time": "3 hours",
        "teardown_time": "2 hours"
    },
    {
        "id": 3,
        "name": "Conference Center",
        "type": "Indoor",
        "capacity": 200,
        "location": "Business District",
        "amenities": ["Projector", "Whiteboards", "Breakout Rooms", "Catering"],
        "price_range": "Medium",
        "available_times": ["08:00-20:00"],
        "setup_time": "1 hour",
        "teardown_time": "1 hour"
    },
    {
        "id": 4,
        "name": "Beach Resort",
        "type": "Outdoor",
        "capacity": 150,
        "location": "Coastal Area",
        "amenities": ["Beach Access", "Pool", "Restaurant", "Accommodation"],
        "price_range": "High",
        "available_times": ["07:00-23:00"],
        "setup_time": "2 hours",
        "teardown_time": "2 hours"
    },
    {
        "id": 5,
        "name": "Community Hall",
        "type": "Indoor",
        "capacity": 100,
        "location": "Suburban Area",
        "amenities": ["Kitchen", "Tables", "Chairs", "Basic Sound System"],
        "price_range": "Low",
        "available_times": ["09:00-21:00"],
        "setup_time": "1 hour",
        "teardown_time": "1 hour"
    }
]

def get_venues():
    """Get all venues from the database"""
    return venue_db

def get_venue_by_id(venue_id):
    """Get a specific venue by its ID"""
    return next((venue for venue in venue_db if venue["id"] == venue_id), None)

def get_venue_availability(venue_id, date):
    """Get availability for a specific venue on a given date"""
    venue = get_venue_by_id(venue_id)
    if venue:
        return {
            "venue_id": venue_id,
            "date": date,
            "available_times": venue.get("available_times", []),
            "setup_time": venue.get("setup_time", "1 hour"),
            "teardown_time": venue.get("teardown_time", "1 hour")
        }
    return None
