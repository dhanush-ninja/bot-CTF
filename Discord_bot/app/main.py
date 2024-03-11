from fastapi import FastAPI
from api.endpoints import router as api_router
from discord_bot.bot import client, TOKEN
import asyncio

app = FastAPI(title="Discord Bot API", version="0.1.0", redoc_url=None)
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def start_discord_bot():
    asyncio.create_task(client.start(TOKEN))
