from fastapi import FastAPI
from workout_api.contrib.routers import api_router

app = FastAPI(title="Workout API")
app.include_router(api_router)
