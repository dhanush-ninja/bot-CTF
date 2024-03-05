from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response 
import json
from better_profanity import profanity
from discord.ext import commands, tasks
import discord

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

# bot setup
intents: Intents = Intents.default()
intents.members = True
intents.message_content = True
client: Client = Client(intents=intents)


def censor_bad_words(text: str) -> str:
    censored_text = profanity.censor(text)
    return censored_text


async def send_message(message: Message, user_message : str) -> None:
    if not user_message:
        print("No response")
        return
    
    
    if is_private:=user_message[0] == "?":
        user_message = user_message[1:]

    try:
        response:str = get_response(user_message, message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)

    except NotImplementedError as e:
        print(e)

@tasks.loop(minutes=60)  # This will run the function every 60 minutes
async def create_channels_from_api():
    response = {
        "entries": [
            {
                "channelName": "Clan1",
                "role": "team1",
                "username": "myste_ry007"  # Assuming the full username includes the discriminator
            },
            {
                "channelName": "Clan2",
                "role": "team2",
                "username": "myste_ry001#2345"
            }
        ]
    }

    guild = client.get_guild(1211624982237417542)  # Replace with your guild ID
    clan_category = discord.utils.get(guild.categories, name="Clan")

    for entry in response['entries']:
        channel_name = entry['channelName']
        role_name = entry['role']
        username = entry['username']

        # Check if the channel already exists
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if existing_channel is None and clan_category:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            new_channel = await clan_category.create_text_channel(name=channel_name, overwrites=overwrites)

            # Check if the role exists, if not create it
            role = discord.utils.get(guild.roles, name=role_name)
            if role is None:
                role = await guild.create_role(name=role_name)
            
            await new_channel.set_permissions(role, read_messages=True, send_messages=True)

        # Find user by username and discriminator

        member = discord.utils.get(guild.members, name=username)
        print(member)
        if member:
            # Check if the user already has the role
            if role not in member.roles:
                await member.add_roles(role)
                print(f"Added role {role.name} to {member.name}")
            else:
                print(f"User {member.name} already has the role {role.name}")
        else:
            print(f"User {username} not found in guild.")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    create_channels_from_api.start()

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

@client.event
async def on_member_join(member):
    welcome_channel_id = 1211624982237417546
    welcome_message = f"Welcome {member.mention} to the server! 🎉 Feel free to introduce yourself."
    channel = client.get_channel(welcome_channel_id)
    await channel.send(welcome_message)


def main() -> None:
    client.run(token=TOKEN)


if __name__ == "__main__":
    main()