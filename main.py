from typing import Union
import asyncio
from fastapi import FastAPI, status
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from fastapi.responses import JSONResponse
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


@app.post("/send_message")
async def send_message(message: str, channel_id: int):
    channel = client.get_channel(channel_id)
    await channel.send(message)
    return JSONResponse(content={"message": "Message sent", "status": "success"}, status_code=status.HTTP_200_OK)

@app.post("/create_channel")
async def create_channel(channel_name: str, role_name: str, username: str):
    guild = client.get_guild(1211624982237417542)
    clan_category = discord.utils.get(guild.categories, name="Clan")
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if existing_channel is None and clan_category:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        new_channel = await clan_category.create_text_channel(name=channel_name, overwrites=overwrites)
        role = discord.utils.get(guild.roles, name=role_name)
        if role is None:
            role = await guild.create_role(name=role_name)
            print(f"Role {role.name} created")
        await new_channel.set_permissions(role, read_messages=True, send_messages=True)
    member = discord.utils.get(guild.members, name=username)
    if member:
        if role not in member.roles:
            await member.add_roles(role)
            print(f"Added role {role.name} to {member.name}")
            return JSONResponse(content={"message": "Channel created", "status": "success"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "User already has role", "status": "error"}, status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return JSONResponse(content={"message": "User not found", "status": "error"}, status_code=status.HTTP_404_NOT_FOUND)
    
@app.post("/delete_channel")
async def delete_channel(channel_name: str):
    guild = client.get_guild(1211624982237417542)
    channel = discord.utils.get(guild.channels, name=channel_name)
    if channel:
        await channel.delete()
        return JSONResponse(content={"message": "Channel deleted", "status": "success"}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "Channel not found", "status": "error"}, status_code=status.HTTP_404_NOT_FOUND)
    
@app.post("/check_user")
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
