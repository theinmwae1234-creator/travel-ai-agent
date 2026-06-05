def create_plan(city, interests, budget):

    plan = []

    plan.append("Retrieve memory")

    plan.append("Retrieve travel knowledge")

    if city:
        plan.append("Check weather")

    if "food" in interests.lower():
        plan.append("Get food recommendations")

    plan.append("Get attractions")

    plan.append("Generate itinerary")

    return plan