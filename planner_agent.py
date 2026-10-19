from ai_agent import query_llm
from tools.weather_tool import get_weather
from tools.sightseeing_tool import get_sightseeing
from tools.hotel_tool import find_hotels
from tools.budget_tool import estimate_budget
from tools.travel_tool import get_travel_info


def interpret_user_query(user_input: str) -> str:
    # 🚀 Direct travel detection (no LLM dependency)
    if "flight" in user_input.lower():
        return get_travel_info(user_input)

    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI travel assistant.\n"
                "Available tools: weather, sightseeing, hotels, budget, travel.\n"
                "The parameter is the city name (or the full query for budget/travel).\n"
                "If a tool is needed, respond ONLY in this format:\n"
                "[TOOL: tool_name | parameter]\n"
                "Example: [TOOL: weather | Chennai]"
            )
        },
        {"role": "user", "content": user_input}
    ]

    try:
        base_reply = query_llm(messages)
    except Exception:
        return "⚠️ AI service is busy. Please try again shortly."

    if "[TOOL:" in base_reply:
        try:
            tool_block = base_reply.split("[TOOL:")[1].split("]")[0]
            tool_name, param = map(str.strip, tool_block.split("|", 1))
            return call_tool(tool_name.lower(), param, user_input)
        except:
            return base_reply.strip()

    return base_reply.strip()



def call_tool(name: str, param: str, full_query: str) -> str:
    if name == "weather":
        return get_weather(param)

    elif name == "sightseeing":
        return get_sightseeing(param)

    elif name == "hotels":
        return find_hotels(param)

    elif name == "budget":
        return estimate_budget(param)

    elif name == "travel":
        return get_travel_info(full_query)

    return "❌ Sorry, I couldn’t find the right tool for that request."
