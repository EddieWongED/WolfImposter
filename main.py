import discord
from discord.ext import commands
import os
from keep_alive import keep_alive


client = discord.Client()
# reaction = discord.reaction()

async def createlist(message):
  role = []
  await message.channel.send('Number of wolves: ')
  await bot.react(message, "name:one")

@client.event
async def on_reaction_add(reaction, user):
    await print("1")


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
    await message.react(':upside_down:')

  if message.content.startswith('$start'):
    await createlist(message)

keep_alive()
client.run(os.getenv("TOKEN"))