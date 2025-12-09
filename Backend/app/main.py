from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import auth, market, chat, health

app = FastAPI(title=settings.PROJECT_NAME)

# CORS – allow your frontend origin here
origins = [
    "http://localhost:5173",  # Vite dev
    "http://localhost:3000",
    # Add your deployed frontend URL too
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(market.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
# later: portfolio, alerts, etc.


@app.get("/")
async def root():
    return {"message": "Bullock backend is running"}
