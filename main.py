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


@app.get("/")
def home():
    return {"message": "Travel AI Agent is running!"}


@app.post("/plan-trip")
def plan_trip(request: TripRequest):
    conversation_memory.append({
        "city": request.city,
        "interests": request.interests,
        "budget": request.budget
    })

    memory_text = (
        f"City: {request.city}, "
        f"Interests: {request.interests}, "
        f"Budget: {request.budget}"
    )

    similar_memories = retrieve_memory(memory_text)
    save_memory(memory_text)

    attractions = get_attractions(request.city, request.interests)
    food_recommendation = get_food_recommendation(request.city, request.budget)
    weather = get_weather(request.city)

    rag_query = f"{request.city} {request.interests} travel attractions food"
    retrieved_knowledge = retrieve_travel_knowledge(rag_query)

    execution_plan = create_plan(
        request.city,
        request.interests,
        request.budget
    )

    itinerary = {
        "city": request.city,
        "trip_length": "2 days",
        "current_weather": weather,
        "short_term_memory": conversation_memory,
        "long_term_memory_retrieved": similar_memories,
        "rag_retrieved_knowledge": retrieved_knowledge,
        "user_preferences": {
            "interests": request.interests,
            "budget": request.budget
        },
        "tools_used": [
            "Attraction database tool",
            "Food recommendation tool",
            "Weather tool (Open-Meteo)",
            "FAISS long-term memory tool",
            "RAG travel knowledge retriever",
            "Dynamic planning tool"
        ],
        "execution_plan": execution_plan,
        "agent_reasoning": [
            f"Planner created execution plan: {execution_plan}",
            "The agent executed memory retrieval, RAG retrieval, weather lookup, attraction lookup, and food recommendation based on the plan.",
            "The retrieved information was combined into a personalized 2-day itinerary."
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