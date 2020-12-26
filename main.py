import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

bot_message_id = ""
emoji_1 = '\U00000031'
emoji_2 = '\U00000032'
emoji_3 = '\U00000033'
emoji_check = '\U00002705'
client = discord.Client()
# reaction = discord.reaction()
wolf_message = False


async def createlist(message):
  role = []
  global wolf_message
  wolf_message = True
  await message.channel.send('Number of wolves: ')


@client.event
async def on_reaction_add(reaction, user):
    await print("1")


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  global wolf_message
  if wolf_message:
    await message.add_reaction(emoji_check)
    # await message.add_reaction(emoji_2)
    # await message.add_reaction(emoji_3)
    wolf_message = False
  
  if message.author == client.user:
    return

  print(message.author.bot)

  if message.content.startswith('$hello'):
    await message.add_reaction(emoji_1)
    await message.add_reaction(emoji_2)
    await message.add_reaction(emoji_3)
    await message.channel.send('Hello!')
    
  if message.content.startswith('$start'):
    await createlist(message)

keep_alive()
client.run(os.getenv("TOKEN"))