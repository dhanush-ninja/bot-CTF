from typing import Union
import asyncio
from fastapi import FastAPI, status, HTTPException
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from fastapi.responses import JSONResponse
from src.Discord import Channel
from pydantic import BaseModel
app = FastAPI(
    title="Discord Bot API",
    redoc_url=None,
    version="0.1.0"
)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)



@app.get("/")
async def read_root():
    return {"Hello": "World"}

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


class SendMessageRequest(BaseModel):
    message: str
    channel_id: int

class ChannelCreationData(BaseModel):
    channel_name: str
    role_name: str
    username: str
    
@app.post("/api/v1/send_message")
async def send_message(body: SendMessageRequest):
    channel = client.get_channel(body.channel_id)
    if channel:
        await channel.send(body.message)
        return JSONResponse(content={"message": "Message sent", "status": "success"}, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=404, detail="Channel not found")

@app.post("/api/v1/create_channel")
async def create_channel(data: ChannelCreationData):
    guild = client.get_guild(799478076491694101)
    if not guild:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guild not found")

    clan_category = discord.utils.get(guild.categories, name="Clan")
    if not clan_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clan category not found")

    existing_channel = discord.utils.get(guild.channels, name=data.channel_name)
    if existing_channel:
        return JSONResponse(content={"message": "Channel already exists", "status": "error"}, status_code=status.HTTP_400_BAD_REQUEST)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
    }
    new_channel = await clan_category.create_text_channel(name=data.channel_name, overwrites=overwrites)
    role = discord.utils.get(guild.roles, name=data.role_name)
    if role is None:
        role = await guild.create_role(name=data.role_name)

    await new_channel.set_permissions(role, read_messages=True, send_messages=True)

    member = discord.utils.get(guild.members, name=data.username)
    if member:
        if role not in member.roles:
            await member.add_roles(role)
            return JSONResponse(content={"message": "Channel and role assigned successfully", "status": "success"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "User already has the role", "status": "error"}, status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return JSONResponse(content={"message": "User not found", "status": "error"}, status_code=status.HTTP_404_NOT_FOUND)

    
@app.post("/api/v1/delete_channel")
async def delete_channel(channel_name: str):
    guild = client.get_guild(1211624982237417542)
    channel = discord.utils.get(guild.channels, name=channel_name)
    if channel:
        await channel.delete()
        return JSONResponse(content={"message": "Channel deleted", "status": "success"}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "Channel not found", "status": "error"}, status_code=status.HTTP_404_NOT_FOUND)
    
@app.post("/api/v1/check_user")
async def check_user(username: str):
    guild = client.get_guild(1211624982237417542)
    member = discord.utils.get(guild.members, name=username)
    if member:
        return JSONResponse(content={"message": "User found", "status": "success"}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "User not found", "status": "error"}, status_code=status.HTTP_404_NOT_FOUND)

async def run():
    try:
        await client.start(TOKEN)
    except KeyboardInterrupt:
        await client.close()


asyncio.create_task(run())
