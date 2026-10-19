# AI Travel Agent

An AI travel assistant you can chat with in the terminal or call as a REST API. It uses a local LLM (Ollama `gemma3:4b`) to understand your question and routes it to the right tool: weather, sightseeing, hotels, flights or budget.

## Features

| Feature | Source | Status |
|---|---|---|
| General travel Q&A | Ollama `gemma3:4b` (local) | ✅ Working |
| Weather | OpenWeatherMap | ✅ Working |
| Sightseeing | OpenTripMap | ⚠️ Needs `OPENTRIPMAP_API_KEY` |
| Flights, budget, hotels | Amadeus | ❌ Not working: Amadeus shut down its Self-Service API in 2026 |

## Project structure

```
ai_travel_agent/
├── chatbot.py          # Terminal chatbot
├── main.py             # FastAPI server
├── planner_agent.py    # Decides which tool to call
├── ai_agent.py         # LLM client (Ollama or OpenRouter)
└── tools/
    ├── weather_tool.py
    ├── sightseeing_tool.py
    ├── hotel_tool.py
    ├── travel_tool.py
    ├── budget_tool.py
    └── amadeus_client.py
```

## Setup

**Requirements:** Python 3.10+ and [Ollama](https://ollama.com).

1. Clone the repo:
   ```bash
   git clone https://github.com/Navyasharthal/ai_travel_agent.git
   cd ai_travel_agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Pull the model:
   ```bash
   ollama pull gemma3:4b
   ```

4. Create your `.env` file from the template and fill in your keys:
   ```bash
   cp .env.example .env
   ```

   | Variable | Needed for |
   |---|---|
   | `OPENWEATHERMAP_API_KEY` | Weather ([get a key](https://openweathermap.org/api)) |
   | `OPENTRIPMAP_API_KEY` | Sightseeing ([get a key](https://opentripmap.io/product)) |
   | `LLM_PROVIDER` | `ollama` (default) or `openrouter` |
   | `LLM_MODEL` | Model name, default `gemma3:4b` |
   | `OPENROUTER_API_KEY` | Only if `LLM_PROVIDER=openrouter` |

## Usage

### Terminal chatbot

```bash
python chatbot.py
```

Type `exit` to quit. On Windows, if emojis look garbled, first run `$env:PYTHONIOENCODING="utf-8"` in PowerShell.

### REST API

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to try the endpoints.

| Method | Endpoint | Body |
|---|---|---|
| GET | `/` | – |
| POST | `/travel/weather` | `{"query": "weather in delhi"}` |
| POST | `/travel/sightseeing` | `{"query": "jaipur"}` |
| POST | `/travel/hotels` | `{"query": "mumbai"}` |
| POST | `/travel/search` | `{"query": "flight from chennai to mumbai on 10th dec"}` |
| POST | `/travel/budget` | `{"query": "flight from delhi to goa on 15th dec"}` |

## Example queries

```
what is the weather in chennai
how is the weather in bangalore today
what is the best time to visit goa?
what should I pack for a trip to manali in winter?
suggest sightseeing in jaipur
```

Any message that contains the word "flight" goes straight to the flight search.
