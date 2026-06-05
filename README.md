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

- Personalized 2-day itinerary generation
- FastAPI REST API
- Swagger API documentation
- Weather API integration using Open-Meteo
- Attraction recommendation tool
- Food recommendation tool
- Short-term memory for current session context
- Long-term memory for storing user preferences
- RAG-style travel knowledge retrieval
- Dynamic planning mechanism
- Render cloud deployment

## Tools Used

1. Weather Tool (Open-Meteo API)

2. Attraction Database Tool

3. Food Recommendation Tool.

4. Memory Tool  

5. RAG Travel Knowledge Retriever  

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
- Demonstrate persistent memory across sessions


### Planning

The planner:

1. Analyzes the user request
2. Selects relevant tools
3. Creates an execution plan
4. Retrieves memory and travel knowledge
5. Generates a personalized itinerary
6. Retrieval-Augmented Generation (RAG)

The RAG component:

- Searches a travel knowledge base
- Retrieves relevant travel information
- Extracts destination-specific locations
- Influences itinerary generation

### Constraint Support

Supports travel constraints such as:

- Budget (Low / Medium / High)
- Travel Style
   - General
   - Relaxed
   - Family
   - Adventure
   - Pet-Friendly

### REST API

Built using FastAPI and exposed through:

POST /plan-trip


## Project Structure

```text
travel-ai-agent/
│
├── app/
│   ├── planner.py                # Planning and tool-selection logic
│   └── rag.py                    # RAG retrieval and place extraction
│
├── data/
│   └── travel_knowledge.txt      # Travel knowledge base used for RAG
│
├── docs/                         # Documentation files
│
├── memory/
│   └── faiss_memory.py           # Long-term memory storage and retrieval
│
├── main.py                       # FastAPI application and API endpoints
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
├── render.yaml                   # Render deployment configuration
├── .gitignore
└── .env
```
## System Architecture

```text
User
 │
 ▼
FastAPI REST API
POST /plan-trip
 │
 ▼
Request Parser
(city, interests, budget, travel_style)
 │
 ▼
Planner
- Creates execution plan
- Selects relevant tools
- Adds planning notes
 │
 ├──────────────► Weather Tool
 │                - Gets current weather from Open-Meteo
 │
 ├──────────────► Attraction Tool
 │                - Finds attractions from local database
 │
 ├──────────────► Food Tool
 │                - Selects food recommendations by budget
 │
 ├──────────────► Short-Term Memory
 │                - Stores current session requests
 │
 ├──────────────► Long-Term Memory
 │                - Saves and retrieves past user preferences
 │
 └──────────────► RAG Retriever
                  - Searches travel_knowledge.txt
                  - Retrieves relevant knowledge
                  - Extracts suggested places
 │
 ▼
Itinerary Generator
- Combines weather, memory, RAG, tools, and constraints
 │
 ▼
JSON Response
- 2-day itinerary
- selected_tools
- execution_plan
- planning_notes
- rag_suggested_places
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

# Run Application

uvicorn main:app --reload

# Open API Documentation

http://127.0.0.1:8000/docs

## Deployment

The project is deployed on Render using:

- FastAPI
- Uvicorn
- GitHub Integration
- Auto Deployment

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