from langchain_core.tools import tool

@tool
def get_weather(city: str):
    """Get weather for a city."""
    if "madrid" in city.lower(): return "Sunny, 25°C"
    if "london" in city.lower(): return "Rainy, 15°C"
    return "Cloudy, 20°C"

tools = [get_weather]
