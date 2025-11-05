from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# --- Clase modelo de datos (Pydantic) ---
class Weather(BaseModel):
    city: str
    temperature: float
    description: str


# --- Clase que maneja la "base de datos" y la lógica del clima ---
class WeatherService:
    def __init__(self):
        self.weather_data = {
            "Bogotá": {"temperature": 18.5, "description": "Nublado"},
            "Medellín": {"temperature": 25.2, "description": "Soleado"}
        }

    def get_weather(self, city: str):
        if city in self.weather_data:
            return {"city": city, "data": self.weather_data[city]}
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")

    def get_all_weather(self):
        return {"climas": self.weather_data}

    def add_or_update_weather(self, weather: Weather):
        self.weather_data[weather.city] = {
            "temperature": weather.temperature,
            "description": weather.description
        }
        return {"message": f"Clima de {weather.city} actualizado correctamente."}

    def delete_weather(self, city: str):
        if city in self.weather_data:
            del self.weather_data[city]
            return {"message": f"Clima de {city} eliminado correctamente."}
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")


# --- Instancia del servicio ---
weather_service = WeatherService()


# --- Endpoints de la API ---
@app.get("/clima/{city}")
def get_weather(city: str):
    return weather_service.get_weather(city)

@app.get("/clima/")
def get_all_weather():
    return weather_service.get_all_weather()

@app.post("/clima/")
def set_weather(weather: Weather):
    return weather_service.add_or_update_weather(weather)

@app.delete("/clima/{city}")
def delete_weather(city: str):
    return weather_service.delete_weather(city)
