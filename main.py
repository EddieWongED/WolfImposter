import discord
import os
from replit import db
from keep_alive import keep_alive


client = discord.Client()
# reaction = discord.reaction()

async def createlist(message):
  role = []
  await message.channel.send('Number of wolves: ')
  await discord.message.add_reaction(':zero:')

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')
    msgid = message.channel.send("text")
    msgid = msgid.channel.fetch_message(messageid)
    emoji = '\N{THUMBS UP SIGN}'
    await msgid.add_reaction(emoji)
  
  if message.content.startswith('$start'):
    await createlist(message)

keep_alive()
client.run(os.getenv("TOKEN"))