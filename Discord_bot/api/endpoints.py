from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from models.pydantic_models import SendMessageRequest, ChannelCreationData
from discord_bot.bot import client
from core.config import GUILD_ID
import discord
from discord.ext import commands
from src.Discord import Channel

router = APIRouter()

@router.post("/send_message")
async def send_message(body: SendMessageRequest):
    channel = client.get_channel(body.channel_id)
    if channel:
        await channel.send(body.message)
        return JSONResponse(content={"message": "Message sent", "status": "success"}, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=404, detail="Channel not found")

@router.post("/create_channel")
async def create_channel(data: ChannelCreationData):
    guild = client.get_guild(int(GUILD_ID))
    clan_category = discord.utils.get(guild.categories, name="Clan")
    existing_channel = discord.utils.get(guild.channels, name=data.channel_name)
    status = "error"  # Default status
    if existing_channel is None and clan_category:
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
                status = "success"

            record_result = Channel.record_channel_creation(data.channel_name, data.role_name, data.username, status)
            return JSONResponse(content=record_result, status_code=record_result["status"])

# Add more endpoints as needed
