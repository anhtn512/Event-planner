import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from db import get_exercises
from chains import enrich_chain, routing_chain, workout_plan_chain, summary_chain, exercise_info_chain
from validators import validate_workout_plan, validate_exercise_info
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint

MOCK_USER_PROFILE = {
        "name": "John Doe",
        "age": 36,
        "height": "180 cm",
        "weight": "75 kg",
        "other_info": "new to exercise"
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust this in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/api/process_query")
async def process_query(request: Request):
    data = await request.json()
    query = data.get("query")
    print(F"User query: {query}")

    try:
        # Normalize the query
        enriched_query = enrich_chain.invoke({"query": query})
        print(f"Enriched query: {enriched_query["enriched_query"]}")

        # Route the query
        route = routing_chain.invoke({"question": enriched_query["enriched_query"]})

        exercises = get_exercises()
        exercises_list = [ex for ex in exercises]

        # Process based on the route
        if "WorkoutPlan" in route:
            workout_plan_json = workout_plan_chain.invoke({
                "user_profile": MOCK_USER_PROFILE,
                "query": enriched_query,
                "exercises": exercises_list
            })

            valid = validate_workout_plan(workout_plan_json)
            if not valid:
                return JSONResponse(content={"type": "error"})

            summary = summary_chain.invoke({
                "user_profile": MOCK_USER_PROFILE,
                "workout_plan": workout_plan_json
            })
            workout_plan_json["summary"] = summary
            return JSONResponse(content=workout_plan_json)
        elif "ExerciseInfo" in route:
            exercise_info_json = exercise_info_chain.invoke({
                "query": enriched_query,
                "exercises": exercises_list
            })
            valid = validate_exercise_info(exercise_info_json)
            if not valid:
                return JSONResponse(content={"type": "error"})

            return JSONResponse(content=exercise_info_json)
        else:
            return JSONResponse(content={"type": "not_supported"})
    
    except:
        return JSONResponse(content={"type": "error"})

@app.get("/api/exercises")
async def get_all_exercises():
    exercises = get_exercises()
    return JSONResponse(content={"exercises": exercises})

app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
