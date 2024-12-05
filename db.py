# db.py
exercises_db = [
    {
        "id": 1,
        "name": "Push-up",
        "description": "An upper body exercise that targets the chest, shoulders, and triceps.",
        "level": "Beginner",
        "muscle_groups": ["Chest", "Shoulders", "Triceps"],
        "requirements": "Home-friendly"
    },
    {
        "id": 2,
        "name": "Squat",
        "description": "A lower body exercise that targets the quadriceps, hamstrings, and glutes.",
        "level": "Beginner",
        "muscle_groups": ["Quadriceps", "Hamstrings", "Glutes"],
        "requirements": "Home-friendly"
    },
    {
        "id": 3,
        "name": "Plank",
        "description": "An exercise that targets the core muscles.",
        "level": "Beginner",
        "muscle_groups": ["Core"],
        "requirements": "Home-friendly"
    },
    {
        "id": 4,
        "name": "Bicep Curl",
        "description": "An exercise that targets the biceps.",
        "level": "Beginner",
        "muscle_groups": ["Biceps"],
        "requirements": "Gym required"
    },
    {
        "id": 5,
        "name": "Lunge",
        "description": "A lower body exercise that targets the quadriceps and glutes.",
        "level": "Intermediate",
        "muscle_groups": ["Quadriceps", "Glutes"],
        "requirements": "Home-friendly"
    },
    {
        "id": 6,
        "name": "Bench Press",
        "description": "An upper body exercise that targets the chest, shoulders, and triceps.",
        "level": "Intermediate",
        "muscle_groups": ["Chest", "Shoulders", "Triceps"],
        "requirements": "Gym required"
    },
    {
        "id": 7,
        "name": "Deadlift",
        "description": "A full body exercise that targets the back, glutes, and hamstrings.",
        "level": "Intermediate",
        "muscle_groups": ["Back", "Glutes", "Hamstrings"],
        "requirements": "Gym required"
    },
    {
        "id": 8,
        "name": "Pull-up",
        "description": "An upper body exercise that targets the back and biceps.",
        "level": "Intermediate",
        "muscle_groups": ["Back", "Biceps"],
        "requirements": "Gym required"
    },
    {
        "id": 9,
        "name": "Dumbbell Shoulder Press",
        "description": "An upper body exercise that targets the shoulders.",
        "level": "Intermediate",
        "muscle_groups": ["Shoulders"],
        "requirements": "Gym required"
    },
    {
        "id": 10,
        "name": "Leg Press",
        "description": "A lower body exercise that targets the quadriceps, hamstrings, and glutes.",
        "level": "Intermediate",
        "muscle_groups": ["Quadriceps", "Hamstrings", "Glutes"],
        "requirements": "Gym required"
    },
    {
        "id": 11,
        "name": "Burpees",
        "description": "A full body exercise that targets multiple muscle groups and improves cardiovascular fitness.",
        "level": "Advanced",
        "muscle_groups": ["Full Body"],
        "requirements": "Home-friendly"
    },
    {
        "id": 12,
        "name": "Snatch",
        "description": "A full body exercise that targets the shoulders, back, and legs.",
        "level": "Advanced",
        "muscle_groups": ["Shoulders", "Back", "Legs"],
        "requirements": "Gym required"
    },
    {
        "id": 13,
        "name": "Clean and Jerk",
        "description": "A full body exercise that targets the shoulders, back, and legs.",
        "level": "Advanced",
        "muscle_groups": ["Shoulders", "Back", "Legs"],
        "requirements": "Gym required"
    },
    {
        "id": 14,
        "name": "Front Squat",
        "description": "A lower body exercise that targets the quadriceps and core.",
        "level": "Advanced",
        "muscle_groups": ["Quadriceps", "Core"],
        "requirements": "Gym required"
    },
    {
        "id": 15,
        "name": "Russian Twist",
        "description": "An exercise that targets the core muscles.",
        "level": "Intermediate",
        "muscle_groups": ["Core"],
        "requirements": "Home-friendly"
    },
    {
        "id": 16,
        "name": "Mountain Climbers",
        "description": "A full body exercise that targets multiple muscle groups and improves cardiovascular fitness.",
        "level": "Beginner",
        "muscle_groups": ["Full Body"],
        "requirements": "Home-friendly"
    },
    {
        "id": 17,
        "name": "Lat Pulldown",
        "description": "An upper body exercise that targets the back and biceps.",
        "level": "Beginner",
        "muscle_groups": ["Back", "Biceps"],
        "requirements": "Gym required"
    },
    {
        "id": 18,
        "name": "Tricep Dips",
        "description": "An upper body exercise that targets the triceps.",
        "level": "Intermediate",
        "muscle_groups": ["Triceps"],
        "requirements": "Home-friendly"
    },
    {
        "id": 19,
        "name": "Leg Raises",
        "description": "An exercise that targets the lower abs.",
        "level": "Intermediate",
        "muscle_groups": ["Core"],
        "requirements": "Home-friendly"
    },
    {
        "id": 20,
        "name": "Calf Raises",
        "description": "A lower body exercise that targets the calves.",
        "level": "Beginner",
        "muscle_groups": ["Calves"],
        "requirements": "Home-friendly"
    }
]

def get_exercises():
    return exercises_db
