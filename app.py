import sys
sys.path.append('/home/Dhanushliebe/discord_bot')
from flask import Flask, request, jsonify
import discord
import asyncio
from better_profanity import profanity
from discord import Message
from queue import Queue
from dotenv import load_dotenv
import os


application = app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True 
intents.members = True

client = discord.Client(intents=intents)

def censor_bad_words(text: str) -> str:
    censored_text = profanity.censor(text)
    return censored_text

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    censored_message = censor_bad_words(message.content)

    if censored_message != message.content:
        await message.delete()  # Delete the original message
        await message.channel.send(f"{message.author.mention} said: {censored_message}, your message contained prohibited words and has been censored. Please adhere to the community guidelines.")
    else:
        return

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.form
    message = data['message']
    channel_id = data['channel_id']
    result_queue = Queue()
    print(f"Sending message to channel {channel_id}: {message}")
    
    asyncio.run_coroutine_threadsafe(
        send_discord_message(channel_id, message, result_queue),
        client.loop
    )
    result = result_queue.get(block=True)
    return jsonify({"message": "Message sent" if result else "Channel not found", "status": "success" if result else "error"}), 200 if result else 404

async def send_discord_message(channel_id, message, result_queue):
    if not channel_id:
        print(f"Channel {channel_id} not found")
        result_queue.put(False)
    channel = client.get_channel(int(channel_id))
    await channel.send(message)
    result_queue.put(True)
    
    

@app.route('/create_channel', methods=['POST'])
def create_channel():
    data = request.form
    channel_name = data['channel_name']
    role_name = data['role']
    username = data['username']
    result_queue = Queue()
    print(f"Creating channel {channel_name} for user {username} with role {role_name}")
    asyncio.run_coroutine_threadsafe(
        create_discord_channel(channel_name, role_name, username, result_queue),
        client.loop
    )
    result = result_queue.get(block=True)
    return jsonify({"message": "Channel created" if result else "something went wrong", "status": "success" if result else "error"}), 200 if result else 404
async def create_discord_channel(channel_name, role_name, username, result_queue):
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
    print(member)
    if member:
        if role not in member.roles:
            await member.add_roles(role)
            print(f"Added role {role.name} to {member.name}")
            result_queue.put(True)
        else:
            print(f"User {member.name} already has the role {role.name}")
            result_queue.put(False)
    else:
        print(f"User {username} not found in guild.")
        result_queue.put(False)

@app.route('/delete_channel', methods=['POST'])
def delete_channel():
    data = request.form
    channel_name = data['channel_name']
    result_queue = Queue()
    print(f"Deleting channel {channel_name}")
    asyncio.run_coroutine_threadsafe(
        delete_discord_channel(channel_name, result_queue),
        client.loop
    )
    result = result_queue.get(block=True)
    return jsonify({"message": "Channel deleted" if result else "Channel not found", "status": "success" if result else "error"}), 200 if result else 404
async def delete_discord_channel(channel_name, result_queue):
    guild = client.get_guild(1211624982237417542)
    channel = discord.utils.get(guild.channels, name=channel_name)
    if channel:
        await channel.delete()
        result_queue.put(True)
    else:
        print(f"Channel {channel_name} not found")
        result_queue.put(False)

@app.route('/check_user', methods=['POST'])
def check_user():
    data = request.form
    username = data['username']
    result_queue = Queue()
    asyncio.run_coroutine_threadsafe(
        check_discord_user(username, result_queue),
        client.loop
    )
    result = result_queue.get(block=True)
    return jsonify({"message": "User found" if result else "User not found", "status": "success" if result else "error"}), 200 if result else 404

async def check_discord_user(username, result_queue):
    guild = client.get_guild(1211624982237417542)
    member = discord.utils.get(guild.members, name=username)
    if member:
        print(f"User {member.name} found")
        result_queue.put(True)
    else:
        print(f"User {username} not found")
        result_queue.put(False)

def run_discord_client():
    client.run(TOKEN)

if __name__ == '__main__':
    from threading import Thread
    discord_thread = Thread(target=run_discord_client)
    discord_thread.start()
    app.run(port=5000)
