
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from routers.stations import router as station_router

app = FastAPI()
app.include_router(station_router)
Instrumentator().instrument(app).expose(app)
