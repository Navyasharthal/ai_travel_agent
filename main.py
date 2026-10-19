from fastapi import FastAPI
from pydantic import BaseModel

from tools.travel_tool import get_travel_info
from tools.budget_tool import estimate_budget
from tools.hotel_tool import find_hotels
from tools.sightseeing_tool import get_sightseeing
from tools.weather_tool import get_weather

app = FastAPI(
    title="AI Travel Assistant API",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {"status": "Travel API running"}


@app.post("/travel/search")
def travel(payload: QueryRequest):
    return {"result": get_travel_info(payload.query)}


@app.post("/travel/budget")
def budget(payload: QueryRequest):
    return {"result": estimate_budget(payload.query)}


@app.post("/travel/hotels")
def hotels(payload: QueryRequest):
    return {"result": find_hotels(payload.query)}


@app.post("/travel/sightseeing")
def sightseeing(payload: QueryRequest):
    return {"result": get_sightseeing(payload.query)}


@app.post("/travel/weather")
def weather(payload: QueryRequest):
    return {"result": get_weather(payload.query)}
