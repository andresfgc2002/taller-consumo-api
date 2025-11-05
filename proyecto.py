from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# --- Modelo de datos para registrar información del clima ---
class Weather(BaseModel):
    city: str
    temperature: float
    description: str

# --- Base de datos simulada (solo para ejemplo) ---
weather_data = {
    "Bogotá": {"temperature": 18.5, "description": "Nublado"},
    "Medellín": {"temperature": 25.2, "description": "Soleado"}
}

# --- GET: Obtener el clima de una ciudad ---
@app.get("/clima/{city}")
def get_weather(city: str):
    if city in weather_data:
        return {"city": city, "data": weather_data[city]}
    return {"error": "Ciudad no encontrada"}

# --- POST (SET): Registrar o actualizar el clima de una ciudad ---
@app.post("/clima/")
def set_weather(info: Weather):
    weather_data[info.city] = {
        "temperature": info.temperature,
        "description": info.description
    }
    return {"message": f"Clima de {info.city} actualizado correctamente."}

# --- GET general: listar todas las ciudades registradas ---
@app.get("/clima/")
def get_all_weather():
    return {"climas": weather_data}
