import json

def validate_workout_plan(workout_plan):
    try:
   
        # Check if type is workout_plan
        if workout_plan.get("type") != "workout_plan":
            return False, "Invalid type"

        # Validate each day's plan
        valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day_plan in workout_plan.get("plan", []):
            # Check if day is valid
            if day_plan.get("day") not in valid_days:
                return False, f"Invalid day: {day_plan.get('day')}"
            
            # Validate exercises
            for exercise in day_plan.get("exercises", []):
                if not isinstance(exercise.get("exercise_id"), int) or exercise["exercise_id"] <= 0:
                    return False, f"Invalid exercise_id: {exercise.get('exercise_id')}"
                
                if not isinstance(exercise.get("sets"), int) or exercise["sets"] <= 0:
                    return False, f"Invalid sets: {exercise.get('sets')}"
                
                if not isinstance(exercise.get("repetitions"), int) or exercise["repetitions"] <= 0:
                    return False, f"Invalid repetitions: {exercise.get('repetitions')}"
        
        return True
    
    except json.JSONDecodeError:
        return False

def validate_exercise_info(exercise_info):
    try:
        # Check if type is exercises
        if exercise_info.get("type") != "exercises":
            return False, "Invalid type"
        
        # Validate exercise_ids
        exercise_ids = exercise_info.get("exercise_ids")
        if not isinstance(exercise_ids, list):
            return False, "exercise_ids should be a list"
        
        for exercise_id in exercise_ids:
            if not isinstance(exercise_id, int) or exercise_id <= 0:
                return False, f"Invalid exercise_id: {exercise_id}"
        
        return True, "Valid exercise info"
    
    except json.JSONDecodeError:
        return False
