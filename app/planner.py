def create_plan(city, interests, budget, weather):
    plan = []
    selected_tools = []
    planning_notes = []

    plan.append("Analyze user request")

    selected_tools.append("Memory tool")
    plan.append("Retrieve similar user preferences")

    selected_tools.append("RAG travel knowledge retriever")
    plan.append("Retrieve travel knowledge from knowledge base")

    if city:
        selected_tools.append("Weather tool")
        plan.append("Check current weather for the destination")
    else:
        planning_notes.append("Weather tool skipped because no city was provided.")

    if interests:
        selected_tools.append("Attraction database tool")
        plan.append("Find attractions matching user interests")
    else:
        planning_notes.append("Attraction tool skipped because no interests were provided.")

    if budget:
        selected_tools.append("Food recommendation tool")
        plan.append("Select food options based on budget")
    else:
        planning_notes.append("Food tool skipped because no budget was provided.")

    if weather != "Weather data unavailable for this city." and weather != "Weather lookup failed.":
        try:
            temperature = float(weather.replace("°C", ""))

            if temperature >= 30:
                planning_notes.append(
                    "Weather is hot, so the itinerary should prioritize indoor, shaded, or lower-effort activities."
                )
            elif temperature <= 10:
                planning_notes.append(
                    "Weather is cold, so the itinerary should include warm indoor stops and cafés."
                )
            else:
                planning_notes.append(
                    "Weather is comfortable, so both indoor and outdoor activities are suitable."
                )

        except ValueError:
            planning_notes.append("Weather data was retrieved but could not be interpreted.")

    plan.append("Generate personalized 2-day itinerary")

    return {
        "execution_plan": plan,
        "selected_tools": selected_tools,
        "planning_notes": planning_notes
    }