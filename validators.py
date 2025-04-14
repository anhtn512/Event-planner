import json

def validate_event_plan(event_plan):
    try:
        # Check if type is event_plan
        if event_plan.get("type") != "event_plan":
            return False, "Invalid type"

        # Validate each day's plan
        for day_plan in event_plan.get("plan", []):
            # Check if day is valid
            if not isinstance(day_plan.get("day"), str) or not day_plan.get("day").startswith("Day "):
                return False, f"Invalid day format: {day_plan.get('day')}"
            
            # Validate activities
            for activity in day_plan.get("activities", []):
                if not isinstance(activity.get("venue_id"), int) or activity["venue_id"] <= 0:
                    return False, f"Invalid venue_id: {activity.get('venue_id')}"
                
                if not isinstance(activity.get("time"), str) or not activity["time"].count(":") == 1:
                    return False, f"Invalid time format: {activity.get('time')}"
                
                if not isinstance(activity.get("description"), str) or not activity["description"]:
                    return False, f"Invalid description: {activity.get('description')}"
        
        return True, "Valid event plan"
    
    except json.JSONDecodeError:
        return False, "Invalid JSON format"

def validate_venue_info(venue_info):
    try:
        # Check if type is venues
        if venue_info.get("type") != "venues":
            return False, "Invalid type"
        
        # Validate venue_ids
        venue_ids = venue_info.get("venue_ids")
        if not isinstance(venue_ids, list):
            return False, "venue_ids should be a list"
        
        for venue_id in venue_ids:
            if not isinstance(venue_id, int) or venue_id <= 0:
                return False, f"Invalid venue_id: {venue_id}"
        
        return True, "Valid venue info"
    
    except json.JSONDecodeError:
        return False, "Invalid JSON format"

def validate_venue_availability(availability):
    try:
        # Check required fields
        required_fields = ["venue_id", "date", "available_times", "setup_time", "teardown_time"]
        for field in required_fields:
            if field not in availability:
                return False, f"Missing required field: {field}"
        
        # Validate venue_id
        if not isinstance(availability["venue_id"], int) or availability["venue_id"] <= 0:
            return False, f"Invalid venue_id: {availability['venue_id']}"
        
        # Validate date format (YYYY-MM-DD)
        if not isinstance(availability["date"], str) or len(availability["date"].split("-")) != 3:
            return False, f"Invalid date format: {availability['date']}"
        
        # Validate available_times
        if not isinstance(availability["available_times"], list):
            return False, "available_times should be a list"
        
        for time_slot in availability["available_times"]:
            if not isinstance(time_slot, str) or not time_slot.count("-") == 1:
                return False, f"Invalid time slot format: {time_slot}"
        
        # Validate setup and teardown times
        if not isinstance(availability["setup_time"], str) or not availability["setup_time"].endswith(" hours"):
            return False, f"Invalid setup_time format: {availability['setup_time']}"
        
        if not isinstance(availability["teardown_time"], str) or not availability["teardown_time"].endswith(" hours"):
            return False, f"Invalid teardown_time format: {availability['teardown_time']}"
        
        return True, "Valid venue availability"
    
    except json.JSONDecodeError:
        return False, "Invalid JSON format"
