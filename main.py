import discord
import const
import os
import random
from keep_alive import keep_alive

in_game = []
role_dict = {}
current_command = ""
players = 0
wolves = 1
witch = 0
prophet = 0
bot_message_id = {}
prefix = "$"
onTask = False
client = discord.Client()
# reaction = discord.reaction()

def main():
  for command in const.commands:
    bot_message_id[command] = ""
  keep_alive()
  client.run(os.getenv("TOKEN"))


async def askForPlayer(message):
  playermsg = await message.channel.send('>>> ```Number of players: ```')
  global bot_message_id
  bot_message_id["players"] = playermsg.id
  for i in range(1, 10):
    await playermsg.add_reaction(const.numbers[i])

async def askForWolf(message):
  wolfmsg = await message.channel.send('>>> ```Number of wolves: ```')
  global bot_message_id
  bot_message_id["wolves"] = wolfmsg.id
  for i in range(1, 4):
    await wolfmsg.add_reaction(const.numbers[i])

async def askForWitch(message):
  witchmsg = await message.channel.send('>>> ```Number of witch: ```')
  global bot_message_id
  bot_message_id["witch"] = witchmsg.id
  for i in range(1, 4):
    await witchmsg.add_reaction(const.numbers[i])

async def askForProphet(message):
  prophetmsg = await message.channel.send('>>> ```Number of prophet: ```')
  global bot_message_id
  bot_message_id["prophet"] = prophetmsg.id
  for i in range(1, 4):
    await prophetmsg.add_reaction(const.numbers[i])

def createlist():
  global wolves
  global witch
  global prophet
  role = []
  for _ in range(wolves):
    role.append('wolf')
  for _ in range(witch):
    role.append('witch')
  for _ in range(prophet):
    role.append('prophet')
  print(f'Role List: {role}')
  return role

async def startgame(message):
  global role_dict
  global in_game
  role_dict = {}
  role = createlist()
  if len(role) > len(in_game):
    await message.channel.send(const.tooManyRoleError)
    return
  temp_players = in_game[:]
  temp_role = role[:]
  random.shuffle(temp_players)
  for i in range(len(in_game)):
    try:
      role_dict[temp_players.pop()] = temp_role.pop()
    except:
      role_dict[temp_players.pop()] = 'Trash'

@client.event
async def on_raw_reaction_add(payload):
  global bot_message_id
  global current_command
  global onTask
  print(f'Current CMD: {current_command}')
  print(f'Sensing {payload.emoji.name},{payload.member.name}' )
  matched = False
  for command in bot_message_id:
    if (bot_message_id[command] == payload.message_id):
      matched = True
      break
  if matched and not(payload.member.bot):
    matched = False
    if current_command == "help":
      pass
    elif current_command == "settings":
      pass
    elif current_command == "start":
      if payload.emoji.name == const.emoji_check and payload.member.name not in in_game:
        in_game.append(payload.member.name)
        print(in_game)
      pass
    elif current_command == "players":
      for number in const.numbers:
        if const.numbers[number] == payload.emoji.name:
          global players
          players = number
          onTask = False
          print(f'Players:{players}')
    elif current_command == "wolves":
      for number in const.numbers:
        if const.numbers[number] == payload.emoji.name:
          global wolves
          wolves = number
          onTask = False
          print(f'Wolves:{wolves}')
    elif current_command == "witch":
      for number in const.numbers:
        if const.numbers[number] == payload.emoji.name:
          global witch
          witch = number
          onTask = False
          print(f'Witch:{witch}')
    elif current_command == "prophet":
      for number in const.numbers:
        if const.numbers[number] == payload.emoji.name:
          global prophet
          prophet = number
          onTask = False
          print(f'Prophet:{prophet}')
    

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  global bot_message_id
  global role_dict
  global onTask
  print(bot_message_id)
  # print(f'The whole message:\n{message}')
  global current_command
  if (onTask):
    return
  first_text = message.content.split()[0]
  print(type(message.content))
  if message.author == client.user:
    return

  if first_text[1:] in const.commands["help"] and first_text[0] == prefix:
    current_command = 'help'
    await message.channel.send(const.settings_str)

  elif first_text[1:] in const.commands["settings"] and first_text[0] == prefix:
    current_command = 'settings'
    settings = await message.channel.send(f'***The settings now:***\n>>> ```css\nNumber of players: {players}``` ```css\nNumber of wolves: {wolves}``` ```css\nNumber of witch: {witch}``` ```css\nNumber of prophet: {prophet}``` ```css\nPlayers in game: {in_game}```')
    bot_message_id["settings"] = settings.id
    
  elif first_text[1:] in const.commands["players"] and first_text[0] == prefix:
    onTask = True
    current_command = 'players'
    await askForPlayer(message)

  elif first_text[1:] in const.commands["wolves"] and first_text[0] == prefix:
    onTask = True
    current_command = 'wolves'
    await askForWolf(message)
  
  elif first_text[1:] in const.commands["witch"] and first_text[0] == prefix:
    onTask = True
    current_command = 'witch'
    await askForWitch(message)

  elif first_text[1:] in const.commands["prophet"] and first_text[0] == prefix:
    onTask = True
    current_command = 'prophet'
    await askForProphet(message)

  elif first_text[1:] in const.commands["start"] and first_text[0] == prefix:
    current_command = 'start'
    start = await message.channel.send(const.Starting_str)
    bot_message_id["start"] = start.id
    await start.add_reaction(const.emoji_check)
    await startgame(message)

  elif first_text[1:] in const.commands["role"] and first_text[0] == prefix:
    await message.channel.send(role_dict)

main()