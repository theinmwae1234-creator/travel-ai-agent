# Hipster Project - Task 2 - Intelligent Travel Planning AI Agent

## Overview

AI Agent that helps users plan a personalized 2-day trip to any city (e.g., Tokyo, Paris,
Singapore), using multiple tools, memory, and reasoning to simulate goal-driven, context-aware
behavior.

## Live Demo

Render Deployment:

https://travel-ai-agent-bxlz.onrender.com/docs

GitHub Repository:

https://github.com/theinmwae1234-creator/travel-ai-agent.git

## Features

- 2-day itinerary generation
- Weather Forecasting (Tool)
- Attraction recommendation (Tool)
- Food recommendation (Tool)
- Short-term memory 
- Long-term memory 
- Retrieval Augmented Generation
- Dynamic planning mechanism
- Cloud deployment (Render)

## Tools Used

1. Weather Forecasting - Using the longtitude and the latitude of the selected city the system send a HTTP GET request to Open Meteo to retrive the current temperature of the city. Then the temperature is catagorised into hot, cold and comfortable.
2. Attraction Recommendation - Using a local Python dictionary for each city (Singapore, Tokyo, Paris) the system map to anime, food,culture, shopping, nature and art. Using the interest keywords the matching attraction is return from the database.
3. Food Recommendation -  Using the  budget input from the user it catagorizze food recommenation base on the city.

## Short-Term Memory

Stores current conversation context including:

- City
- Interests
- Budget
- Travel Style

## Long-Term Memory

Use FAIS-inspired memory system

- Save previous user preferences
- Retrieve similar past travel requests
- Demonstrate memory across sessions


### Planning

The planner:

1. Analyzes the user request
2. Using relevant tools retrive using the input - city, interests and budget
3. Creates an execution plan (After  retriving from the database base on user's preference)
4. Retrieves memory and travel knowledge
5. Generates a personalized itinerary
6. Retrieval-Augmented Generation (RAG)

### REST API

Built using FastAPI and exposed through:

POST /plan-trip


## Project Structure

```text
travel-ai-agent/
│
├── app/
│   ├── planner.py                
│   └── rag.py                    
│
├── data/
│   └── travel_knowledge.txt      
│
├── docs/                         
│   └── Technical_Document.md
├── memory/
│   └── faiss_memory.py           
│
├── main.py                       
├── README.md                     
├── requirements.txt              
├── render.yaml                   
├── .gitignore
└── .env
```

## Request (Example)

{
  "city": "Tokyo",
  "interests": "anime, food",
  "budget": "medium"
}

## Response (Example)

{ 
   "city": "Tokyo",
   "current_weather": "17°C",
   "rag_suggested_places": [
       "Akihabara", 
       "Nakano Broadway", 
       "Shibuya" 
   ] 
}

## Installation

# Clone Repository

git clone https://github.com/theinmwae1234-creator/travel-ai-agent.git

cd travel-ai-agent

# Install Dependencies

pip install -r requirements.txt

# Virtual Environment

uvicorn main:app --reload

# Open API Documentation

http://127.0.0.1:8000/docs

## Deployment

The project is deployed on Render using:

- FastAPI
- Uvicorn
- GitHub Integration

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Open-Meteo API
- Requests
- GitHub
- Render

## Author

Thein Mwae Than Tha

Engineering Product Development (EPD)
Singapore University of Technology and Design (SUTD)