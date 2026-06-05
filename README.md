# Intelligent Travel Planning AI Agent

## Overview

This project is an AI-style travel planning agent that helps users generate a personalized 2-day trip itinerary for a selected city.

The agent uses multiple tools, short-term memory, long-term memory, retrieval-augmented generation, and planning logic to create context-aware travel recommendations.

## Live Demo

Render Deployment:

https://travel-ai-agent-bxlz.onrender.com/docs

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

1. Attraction Database Tool  
   Selects attractions based on city and user interests.

2. Food Recommendation Tool  
   Suggests food options based on city and budget.

3. Weather Tool  
   Retrieves current weather using Open-Meteo API.

4. Memory Tool  
   Stores and retrieves user preferences.

5. RAG Travel Knowledge Retriever  
   Retrieves relevant travel information from a local knowledge base.

## API Endpoint

### POST /plan-trip

Example request:

```json
{
  "city": "Tokyo",
  "interests": "anime, food",
  "budget": "medium"
}