from fastapi import FastAPI
from pydantic import BaseModel
import math

app = FastAPI()

class Location(BaseModel):
    lat: float
    lon: float

class RequestData(BaseModel):
    locations: list[Location]

def distance(a, b):
    return math.sqrt((a.lat - b.lat)**2 + (a.lon - b.lon)**2)

@app.get("/")
def home():
    return {"message": "API is working"}

@app.post("/optimize-route")
def optimize_route(data: RequestData):
    points = data.locations[:]
    route = [points.pop(0)]

    while points:
        last = route[-1]
        next_point = min(points, key=lambda x: distance(last, x))
        route.append(next_point)
        points.remove(next_point)

    return {"route": route}