

from langchain.tools import tool


# ---------------------------------------------------------
# TOOL 1 — Budget Calculator
# ---------------------------------------------------------

@tool
def calculate_budget(total_budget: float, days: int) -> str:
    """
    Calculate an approximate daily travel budget and
    divide the total budget into major categories.
    """

    if days <= 0:
        return "Number of days must be greater than 0."

    daily_budget = total_budget / days

    accommodation = total_budget * 0.35
    food = total_budget * 0.20
    transport = total_budget * 0.20
    activities = total_budget * 0.15
    emergency = total_budget * 0.10

    return f"""
Budget Summary:
Total Budget: ₹{total_budget:,.0f}
Number of Days: {days}
Approximate Daily Budget: ₹{daily_budget:,.0f}

Suggested Allocation:
- Accommodation: ₹{accommodation:,.0f}
- Food: ₹{food:,.0f}
- Transportation: ₹{transport:,.0f}
- Activities/Sightseeing: ₹{activities:,.0f}
- Emergency/Miscellaneous: ₹{emergency:,.0f}
"""


# ---------------------------------------------------------
# TOOL 2 — Itinerary Planner
# ---------------------------------------------------------

@tool
def create_itinerary(destination: str, days: int) -> str:
    """
    Create a basic day-by-day itinerary structure.
    """

    if days <= 0:
        return "Number of days must be greater than 0."

    itinerary = []

    for day in range(1, days + 1):
        itinerary.append(
            f"Day {day}: Plan sightseeing and activities in {destination} "
            f"based on the retrieved travel-guide information."
        )

    return "\n".join(itinerary)


# ---------------------------------------------------------
# TOOL 3 — Travel Checklist
# ---------------------------------------------------------

@tool
def travel_checklist(destination: str, days: int) -> str:
    """
    Generate a practical travel preparation checklist.
    """

    return f"""
Travel Checklist for {destination} ({days} days):

- Valid ID and important documents
- Booking confirmations
- Comfortable clothes
- Comfortable walking shoes
- Phone and charger
- Power bank
- Basic medicines
- Toiletries
- Water bottle
- Weather-appropriate clothing
- Emergency contact information
- Some cash and payment method
- Check local weather before travelling
"""


# ---------------------------------------------------------
# TOOL 4 — Destination Check
# ---------------------------------------------------------

@tool
def check_destination(destination: str) -> str:
    """
    Check whether the requested destination has a travel guide
    available in the project knowledge base.
    """

    supported_destinations = [
        "goa",
        "darjeeling",
        "jaipur",
        "delhi",
        "kerala"
    ]

    destination_lower = destination.strip().lower()

    if destination_lower in supported_destinations:
        return (
            f"A travel guide for {destination.title()} is available "
            "in the knowledge base."
        )

    return (
        f"No dedicated travel guide for {destination.title()} was found "
        "in the current knowledge base. Use available information carefully."
    )


# ---------------------------------------------------------
# TOOL 5 — Transport Recommendation
# ---------------------------------------------------------

@tool
def transport_recommendation(destination: str) -> str:
    """
    Provide a basic transportation planning framework.
    """

    return f"""
Transportation planning for {destination}:

- Check the travel guide for available transport options.
- Compare public transport, taxis and rental options.
- Consider distance between attractions.
- Consider travel time when creating the itinerary.
- Check current transport schedules before travelling.
"""


# ---------------------------------------------------------
# TOOL 6 — Packing Recommendation
# ---------------------------------------------------------

@tool
def packing_recommendation(destination: str, days: int) -> str:
    """
    Generate a basic packing recommendation based on trip duration.
    """

    if days <= 0:
        return "Number of days must be greater than 0."

    clothing = max(2, days)

    return f"""
Packing recommendation for {destination}:

- Approximately {clothing} sets of comfortable clothing
- Comfortable footwear
- Weather-appropriate clothing
- Toiletries
- Phone charger
- Power bank
- Basic medicines
- Identification documents
- Water bottle
- Small day bag
- Sunglasses/sunscreen where appropriate
"""