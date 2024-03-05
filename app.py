import os
from better_profanity import profanity
from flask import Flask
from flask_discord_interactions import DiscordInteractions
import discord
import asyncio
from discord import Intents, Client, Message
from flask import Flask, render_template, request, redirect, session, jsonify

application = app = Flask(__name__)
discord_interactions = DiscordInteractions(app)

# Discord bot token
TOKEN = "MTIxMTU5MDM0MTA2NTcwMzQ1NA.GOkwyY.RD4kMakGayodkTH6clkr5SykQqIWSSRzTO563c"

# Define intents
intents: Intents = discord.Intents.default()
intents.message_content = True
intents.members = True # This is necessary to receive messages
intents.guilds = True  # This is necessary for the bot to work with guild information

# Initialize discord.py client with intents
client: Client = Client(intents=intents)

app.config["DISCORD_CLIENT_ID"] =1211590341065703454
app.config["DISCORD_PUBLIC_KEY"] = "40e38db8f8df99fa966bab0ec482437b3a216393a633c2ddec3806dee11d2a41"
app.config["DISCORD_CLIENT_SECRET"] = "DVFAzYrm3oJWLAvdL9L-kQPjqNWTmBVt"

def censor_bad_words(text: str) -> str:
    return profanity.censor(text)


@app.route("/createchannel", methods=["POST"])
def create_channel():
    response = asyncio.run(create_channel_async())
    return response

async def create_channel_async():
    channelname = request.form.get('channelname')
    print(channelname)
    role = request.form.get('role')
    print(role)
    username = request.form.get('username')
    print(username)
    guild = get_guilds()
    if guild is None:
        print("Guild not found. Check the guild ID and bot's guild membership.")
        return jsonify({'status': 'error', 'message': 'Guild not found'}), 404
    clan_category = discord.utils.get(guild.categories, name="Clan")
    print(clan_category)
    # Check if the channel already exists dont create it, else create it
    existing_channel = discord.utils.get(guild.channels, name=channelname)
    if existing_channel:
        return jsonify({"message": "Channel already exists"})
    else:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        role = discord.utils.get(guild.roles, name=role)
        member = discord.utils.get(guild.members, name=username)
        if not role:
            role = await guild.create_role(name=role)
        if not member:
            return jsonify({"message": "User not found"})
        new_channel = await clan_category.create_text_channel(name=channelname, overwrites=overwrites)
        await new_channel.set_permissions(role, read_messages=True, send_messages=True)
        await member.add_roles(role)
        return jsonify({"message": "Channel created successfully"})
    

@discord_interactions.command()
def ping(ctx):
    "Respond with a friendly 'pong'!"
    return "Pong!"



def get_guilds():
    file = open("/home/Dhanushliebe/discord_bot/guilds.txt", "r")
    guilds = file.readlines()
    file.close()
    return client.get_guild(int(guilds[0].split(" - ")[1]))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    censored_message = censor_bad_words(message.content)
    if censored_message != message.content:
        await message.delete()
        await message.channel.send(f"{message.author.mention} said: {censored_message}, your message contained prohibited words and has been censored. Please adhere to the community guidelines.")

discord_interactions.set_route("/interactions")
discord_interactions.update_commands(guild_id=1211624982237417542)

@client.event
async def on_ready():
    file = open("guilds.txt", "w+")
    guild = client.get_guild(1211624982237417542)
    file.write(f"{guild.name} - {guild.id}")
    file.close()
    print(f'{client.user} has connected to Discord!')
    
    


def run_discord_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client.start(TOKEN))

if __name__ == '__main__':
    from threading import Thread
    t = Thread(target=run_discord_bot)
    t.start()
    app.run()
