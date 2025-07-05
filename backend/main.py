import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import alerts, pools

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alerts.router)
app.include_router(pools.router)