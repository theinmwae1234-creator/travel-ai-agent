def create_plan(city, interests, budget, weather):
    plan = []
    selected_tools = []
    planning_notes = []

    interests_lower = interests.lower()
    budget_lower = budget.lower()

    plan.append("Analyze user request")

    selected_tools.append("Memory tool")
    plan.append("Retrieve similar user preferences")

    selected_tools.append("RAG travel knowledge retriever")
    plan.append("Retrieve travel knowledge from knowledge base")

    if city:
        selected_tools.append("Weather tool")
        plan.append("Check current weather for the destination")

    if any(word in interests_lower for word in ["anime", "culture", "shopping", "nature", "art"]):
        selected_tools.append("Attraction database tool")
        plan.append("Find attractions matching user interests")

    if "food" in interests_lower or budget_lower in ["low", "medium", "high"]:
        selected_tools.append("Food recommendation tool")
        plan.append("Select food options based on budget and food interest")

    if weather not in ["Weather data unavailable for this city.", "Weather lookup failed."]:
        try:
            temperature = float(weather.replace("°C", ""))

            if temperature >= 30:
                planning_notes.append(
                    "Weather is hot, so the agent prioritizes indoor, shaded, or lower-effort activities."
                )
            elif temperature <= 10:
                planning_notes.append(
                    "Weather is cold, so the agent prioritizes indoor attractions and warm food stops."
                )
            else:
                planning_notes.append(
                    "Weather is comfortable, so both indoor and outdoor activities are suitable."
                )

        except ValueError:
            planning_notes.append("Weather data was retrieved but could not be interpreted.")

    if budget_lower == "low":
        planning_notes.append("Budget is low, so the agent prioritizes affordable food and low-cost attractions.")
    elif budget_lower == "medium":
        planning_notes.append("Budget is medium, so the agent balances affordability and experience quality.")
    elif budget_lower == "high":
        planning_notes.append("Budget is high, so the agent can include premium dining or experiences.")

    plan.append("Generate personalized 2-day itinerary")

    return {
        "execution_plan": plan,
        "selected_tools": selected_tools,
        "planning_notes": planning_notes
    }