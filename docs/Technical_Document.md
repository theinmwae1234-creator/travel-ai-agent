# Technical Document – Intelligent Travel Planning AI Agent

## 1. Introduction

The Intelligent Travel Planning AI Agent is a FastAPI-based system that generates personalized 2-day travel itineraries based on user preferences. The project demonstrates the use of multiple tools, memory systems, retrieval-augmented generation (RAG), planning logic, and cloud deployment.

The objective is to simulate an intelligent agent capable of reasoning about user requests and coordinating multiple components to produce a customized travel plan.

---

## 2. System Architecture

The system follows a modular architecture consisting of a planner, tool layer, memory layer, retrieval layer, and itinerary generator.

```text
User Request
      │
      ▼
   FastAPI API
      │
      ▼
     Planner
      │
 ┌────┼────┐
 ▼    ▼    ▼
Tools Memory  RAG
      │
      ▼
Itinerary Generator
      │
      ▼
 JSON Response
```

The planner acts as the central controller and determines which tools should be used based on the user request.

---

## 3. Tool Selection

The agent uses multiple tools to gather information and construct travel recommendations.

### Weather Tool

Purpose:

* Retrieves current weather conditions using the Open-Meteo API.
* Allows the agent to generate weather-aware recommendations.

Example:

* Hot weather → prioritize shaded or indoor activities.
* Cold weather → prioritize indoor attractions and warm food options.

### Attraction Tool

Purpose:

* Retrieves attractions from a local attraction database.
* Matches attractions to user interests.

Examples:

* Anime → Akihabara, Nakano Broadway
* Food → Tsukiji Outer Market

### Food Recommendation Tool

Purpose:

* Generates food recommendations according to budget.

Examples:

* Low budget → Hawker centres and street food
* High budget → Fine dining and premium experiences

---

## 4. Memory Design

### Short-Term Memory

Short-term memory stores requests made during the current session.

Stored information includes:

* City
* Interests
* Budget
* Travel Style

Purpose:

* Maintains conversational context.
* Demonstrates session-level memory.

### Long-Term Memory

Long-term memory stores previous user preferences.

Functions:

* Save user preferences
* Retrieve related historical requests
* Personalize future recommendations

Example:

A previous Tokyo anime trip can influence future anime-related recommendations.

---

## 5. Retrieval-Augmented Generation (RAG)

The project uses a lightweight RAG implementation.

Knowledge Source:

```text
data/travel_knowledge.txt
```

Process:

1. Build a travel query from user preferences.
2. Retrieve relevant travel knowledge.
3. Extract destination-specific places.
4. Use retrieved information to influence itinerary generation.

Example:

Query:

```text
Tokyo anime food
```

Retrieved Knowledge:

```text
Akihabara
Nakano Broadway
Tsukiji Outer Market
```

The itinerary prioritizes locations extracted from the retrieved knowledge.

---

## 6. Planning and Reasoning

The planner performs the following sequence:

1. Analyze user request.
2. Retrieve memory.
3. Retrieve travel knowledge.
4. Check weather conditions.
5. Select relevant tools.
6. Generate itinerary.
7. Produce reasoning trace.

The execution plan and reasoning trace are returned as part of the API response to improve transparency.

---

## 7. Deployment

The application is deployed using Render.

Technology Stack:

* Python
* FastAPI
* Uvicorn
* GitHub
* Render
* Open-Meteo API

Deployment Workflow:

```text
GitHub Repository
        │
        ▼
      Render
        │
        ▼
   FastAPI Service
        │
        ▼
 Live API Endpoint
```

---

## 8. Limitations

Current limitations include:

* Small travel knowledge base
* Rule-based planning logic
* No hotel recommendation API
* No flight recommendation API
* Limited city coverage

---

## 9. Future Improvements

Potential future enhancements include:

* Real FAISS vector database integration
* Multi-hop retrieval pipeline
* Hotel and flight recommendation APIs
* LLM-powered itinerary generation
* Multilingual travel planning
* User authentication and profiles

---

## 10. Conclusion

The Intelligent Travel Planning AI Agent successfully demonstrates tool usage, memory integration, retrieval-augmented generation, planning and reasoning, and cloud deployment. The project provides a practical example of how AI agents can coordinate multiple components to generate personalized recommendations and assist users in travel planning.
