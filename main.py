import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from db import get_venues, get_venue_by_id, get_venue_availability
from chains import enrich_chain, routing_chain, event_plan_chain, summary_chain, vendor_info_chain
from validators import validate_event_plan, validate_venue_info, validate_venue_availability
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint

MOCK_USER_PROFILE = {
    "name": "John Doe",
    "company": "ABC Corp",
    "event_type": "Corporate Conference",
    "budget": "Medium",
    "attendees": 150,
    "other_info": "Looking for a professional venue with catering"
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
    print(f"User query: {query}")

    try:
        # Normalize the query
        enriched_query = enrich_chain.invoke({"query": query})
        print(f"Enriched query: {enriched_query['enriched_query']}")

        # Route the query
        route = routing_chain.invoke({"question": enriched_query["enriched_query"]})

        venues = get_venues()
        venues_list = [venue for venue in venues]

        # Process based on the route
        print(f"Route: {route}")
        if "EventPlan" in route:
            event_plan_json = event_plan_chain.invoke({
                "user_profile": MOCK_USER_PROFILE,
                "query": enriched_query,
                "resources": venues_list
            })

            valid, message = validate_event_plan(event_plan_json)
            if not valid:
                return JSONResponse(content={"type": "error", "message": message})

            summary = summary_chain.invoke({
                "user_profile": MOCK_USER_PROFILE,
                "event_plan": event_plan_json
            })
            event_plan_json["summary"] = summary
            return JSONResponse(content=event_plan_json)
        elif "VendorInfo" in route:
            vendor_info_json = vendor_info_chain.invoke({
                "query": enriched_query,
                "resources": venues_list
            })
            valid, message = validate_venue_info(vendor_info_json)
            if not valid:
                return JSONResponse(content={"type": "error", "message": message})

            return JSONResponse(content=vendor_info_json)
        else:
            return JSONResponse(content={"type": "not_supported"})
    
    except Exception as e:
        return JSONResponse(content={"type": "error", "message": str(e)})

@app.get("/api/venues")
async def get_all_venues():
    venues = get_venues()
    return JSONResponse(content={"venues": venues})

@app.get("/api/venues/{venue_id}")
async def get_venue(venue_id: int):
    venue = get_venue_by_id(venue_id)
    if venue:
        return JSONResponse(content=venue)
    return JSONResponse(content={"error": "Venue not found"}, status_code=404)

@app.get("/api/venues/{venue_id}/availability")
async def get_venue_availability_endpoint(venue_id: int, date: str):
    availability = get_venue_availability(venue_id, date)
    if availability:
        return JSONResponse(content=availability)
    return JSONResponse(content={"error": "Venue not found"}, status_code=404)

app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
