import discord
from discord.ext import commands
import const
import time
import os
from keep_alive import keep_alive

in_game = []
current_command = ""
players = 0
bot_message_id = ""
client = discord.Client()
# reaction = discord.reaction()

def main():
  keep_alive()
  client.run(os.getenv("TOKEN"))


async def askForPlayer(message):
  playermsg = await message.channel.send('>>> ```Number of players: ```')
  global bot_message_id
  bot_message_id = playermsg.id
  for i in range(1, 10):
    await playermsg.add_reaction(const.numbers[i])


async def createlist(message):
  role = []

@client.event
async def on_raw_reaction_add(payload):
  global bot_message_id
  global current_command
  if bot_message_id == payload.message_id and not(payload.member.bot):
    if current_command == "help":
      pass
    elif current_command == "settings":
      pass
    elif current_command == "start":
      if payload.emoji.name == const.emoji_check:
        in_game.append(payload.member.name)
      pass
    elif current_command == "players":
      for number in const.numbers:
        if const.numbers[number] == payload.emoji.name:
          global players
          players = number
          print(f'Players:{players}')
    
  


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  print(message.content)
  global current_command
  if message.author == client.user:
    return

  if message.content.startswith('$help'):
    current_command = 'help'
    await message.channel.send(const.settings_str)

  if message.content.startswith('$settings') or message.content.startswith('$set'):
    current_command = 'settings'
    await message.channel.send(f'''The settings now:
>>> ```Amount of players in game: {len(in_game)}```
```Amount of players until start: {players}
Players```''')
  
  if message.content.startswith('$players') or message.content.startswith('$p'):
    current_command = 'players'
    await askForPlayer(message)

  if message.content.startswith('$start'):
    current_command = 'start'
    start = await message.channel.send(const.Starting_str)
    await start.add_reaction(const.emoji_check)

main()