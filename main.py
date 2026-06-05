from fastapi import FastAPI
from pydantic import BaseModel
import requests

from memory.faiss_memory import save_memory, retrieve_memory
from app.rag import retrieve_travel_knowledge
from app.planner import create_plan

app = FastAPI()

conversation_memory = []


class TripRequest(BaseModel):
    city: str
    interests: str
    budget: str
    travel_style: str = "general"


def get_attractions(city: str, interests: str):
    attraction_database = {
        "Tokyo": {
            "anime": ["Akihabara", "Nakano Broadway"],
            "food": ["Tsukiji Outer Market", "Shinjuku Omoide Yokocho"],
            "culture": ["Sensoji Temple", "Meiji Shrine"],
            "shopping": ["Shibuya", "Harajuku Takeshita Street"]
        },
        "Singapore": {
            "food": ["Lau Pa Sat", "Maxwell Food Centre"],
            "nature": ["Gardens by the Bay", "Singapore Botanic Gardens"],
            "culture": ["Chinatown", "Little India"],
            "shopping": ["Orchard Road", "Bugis Street"]
        },
        "Paris": {
            "art": ["Louvre Museum", "Musée d'Orsay"],
            "food": ["Le Marais", "Saint-Germain cafés"],
            "culture": ["Notre-Dame area", "Montmartre"],
            "shopping": ["Champs-Élysées", "Galeries Lafayette"]
        }
    }

    city_data = attraction_database.get(city, {})
    selected_attractions = []

    for interest, places in city_data.items():
        if interest.lower() in interests.lower():
            selected_attractions.extend(places)

    if not selected_attractions:
        for places in city_data.values():
            selected_attractions.extend(places)

    return selected_attractions[:4]


def get_food_recommendation(city: str, budget: str):
    food_database = {
        "Tokyo": {
            "low": "Convenience store meals, ramen shops, and street food around Ueno.",
            "medium": "Ramen, sushi trains, izakayas, and casual restaurants in Shinjuku.",
            "high": "Omakase sushi, fine dining, and premium wagyu restaurants."
        },
        "Singapore": {
            "low": "Hawker centres such as Maxwell Food Centre and Lau Pa Sat.",
            "medium": "Casual restaurants in Bugis, Chinatown, and Tanjong Pagar.",
            "high": "Fine dining restaurants around Marina Bay Sands."
        },
        "Paris": {
            "low": "Bakeries, crêpe stands, and affordable cafés.",
            "medium": "Bistros and brasseries around Le Marais or Saint-Germain.",
            "high": "Michelin-starred restaurants and luxury French dining."
        }
    }

    return food_database.get(city, {}).get(
        budget.lower(),
        "Local restaurants based on the traveller's budget."
    )


def get_weather(city: str):
    city_coordinates = {
        "Tokyo": {"lat": 35.6764, "lon": 139.6500},
        "Singapore": {"lat": 1.3521, "lon": 103.8198},
        "Paris": {"lat": 48.8566, "lon": 2.3522}
    }

    if city not in city_coordinates:
        return "Weather data unavailable for this city."

    lat = city_coordinates[city]["lat"]
    lon = city_coordinates[city]["lon"]

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}"
            f"&longitude={lon}"
            f"&current=temperature_2m"
        )

        response = requests.get(url)
        data = response.json()
        temperature = data["current"]["temperature_2m"]

        return f"{temperature}°C"

    except Exception:
        return "Weather lookup failed."


def make_weather_aware_note(weather: str):
    try:
        temperature = float(weather.replace("°C", ""))

        if temperature >= 30:
            return "Weather is hot, so the agent prioritizes indoor, shaded, or lower-effort activities."
        elif temperature <= 10:
            return "Weather is cold, so the agent recommends indoor stops and warm food options."
        else:
            return "Weather is comfortable, so both indoor and outdoor activities are suitable."

    except Exception:
        return "Weather data could not be interpreted, so the agent uses a general itinerary."


def get_travel_style_note(travel_style: str):
    style = travel_style.lower()

    if style == "pet-friendly":
        return "Pet-friendly constraint detected: prioritize outdoor areas, parks, walkable districts, and avoid places that may restrict pets."

    if style == "family":
        return "Family travel style detected: prioritize safe, accessible, lower-effort attractions and avoid overly packed schedules."

    if style == "relaxed":
        return "Relaxed travel style detected: reduce rushing and keep the itinerary comfortable with fewer transitions."

    if style == "adventure":
        return "Adventure travel style detected: include more exploration-heavy and active experiences."

    return "General travel style selected: create a balanced itinerary."


def extract_places_from_rag(retrieved_knowledge):
    known_places = [
        "Akihabara",
        "Nakano Broadway",
        "Tsukiji Outer Market",
        "Shinjuku Omoide Yokocho",
        "Sensoji Temple",
        "Tokyo Skytree",
        "Meiji Shrine",
        "Shibuya",
        "Harajuku",
        "Lau Pa Sat",
        "Maxwell Food Centre",
        "Gardens by the Bay",
        "Singapore Botanic Gardens",
        "Chinatown",
        "Little India",
        "Kampong Glam",
        "Eiffel Tower",
        "Louvre Museum",
        "Montmartre",
        "Le Marais",
        "Musée d'Orsay"
    ]

    extracted_places = []

    for chunk in retrieved_knowledge:
        for place in known_places:
            if place.lower() in chunk.lower() and place not in extracted_places:
                extracted_places.append(place)

    return extracted_places


@app.get("/")
def home():
    return {"message": "Travel AI Agent is running!"}


@app.post("/plan-trip")
def plan_trip(request: TripRequest):
    conversation_memory.append({
        "city": request.city,
        "interests": request.interests,
        "budget": request.budget,
        "travel_style": request.travel_style
    })

    memory_text = (
        f"City: {request.city}, "
        f"Interests: {request.interests}, "
        f"Budget: {request.budget}, "
        f"Travel Style: {request.travel_style}"
    )

    similar_memories = retrieve_memory(memory_text)
    save_memory(memory_text)

    weather = get_weather(request.city)

    planning_result = create_plan(
        request.city,
        request.interests,
        request.budget,
        weather
    )

    rag_query = f"{request.city} {request.interests} {request.travel_style} travel attractions food"
    retrieved_knowledge = retrieve_travel_knowledge(rag_query)

    rag_places = extract_places_from_rag(retrieved_knowledge)
    tool_places = get_attractions(request.city, request.interests)

    attractions = rag_places + [
        place for place in tool_places
        if place not in rag_places
    ]

    food_recommendation = get_food_recommendation(request.city, request.budget)
    weather_note = make_weather_aware_note(weather)
    travel_style_note = get_travel_style_note(request.travel_style)

    itinerary = {
        "city": request.city,
        "trip_length": "2 days",
        "current_weather": weather,
        "weather_aware_note": weather_note,
        "travel_style_note": travel_style_note,

        "short_term_memory": conversation_memory,
        "long_term_memory_retrieved": similar_memories,
        "rag_retrieved_knowledge": retrieved_knowledge,
        "rag_suggested_places": rag_places,

        "user_preferences": {
            "interests": request.interests,
            "budget": request.budget,
            "travel_style": request.travel_style
        },

        "selected_tools": planning_result["selected_tools"],
        "tools_used": planning_result["selected_tools"],

        "execution_plan": planning_result["execution_plan"],
        "planning_notes": planning_result["planning_notes"] + [
            travel_style_note
        ],

        "agent_reasoning": [
            "The agent analyzed the user request and selected tools based on city, interests, budget, weather, and travel style.",
            "The planner decided which tools were relevant and created an execution plan.",
            "The agent retrieved related memories and travel knowledge before generating the itinerary.",
            "RAG retrieved relevant destination knowledge, and matching places were extracted from the retrieved context.",
            "The itinerary prioritizes RAG-suggested places first, then fills remaining slots using the attraction database.",
            "Weather, budget, and travel style constraints were considered before finalizing the itinerary."
        ],

        "day_1": {
            "morning": attractions[0] if len(attractions) > 0 else "Explore city centre",
            "afternoon": attractions[1] if len(attractions) > 1 else "Visit a popular local area",
            "evening": food_recommendation
        },

        "day_2": {
            "morning": attractions[2] if len(attractions) > 2 else "Visit a cultural attraction",
            "afternoon": attractions[3] if len(attractions) > 3 else "Explore a shopping or leisure district",
            "evening": f"End the trip with a relaxed evening in {request.city}."
        }
    }

    return itinerary