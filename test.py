import os
import discord
from discord import Message
import json
from better_profanity import profanity

with open('badword_list.json', 'r') as file:
    bad_words_data = json.load(file)
    BAD_WORDS = bad_words_data["bad_words_english"]

def censor_bad_words(text: str) -> str:
    censored_text = profanity.censor(text)
    return censored_text
my_secret = os.environ['TOKEN']
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!'
            await guild.system_channel.send(to_send)

    async def on_message(message: Message) -> None:
        if message.author == client.user:
            return

        censored_message = censor_bad_words(message.content)

        if censored_message != message.content:
            await message.delete()  # Delete the original message
            await message.channel.send(f"{message.author.mention} said: {censored_message}, your message contained prohibited words and has been censored. Please adhere to the community guidelines.")
        # if message.content is empty, return
        else:
            return


intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)
client.run('MTIxMTU5MDM0MTA2NTcwMzQ1NA.GzogAy.7g-i4DxyB9oQ1JKFgi3vy0IuMowCoYAztWe5d0')