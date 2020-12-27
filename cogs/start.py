import discord
from discord.ext import commands
from data import const
from data import variable
import random

class Start(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=const.commands["start"])
  async def start(self, ctx):
    msg = await ctx.message.channel.send(const.starting_str)
    variable.bot_message_id["start"] = msg.id
    await msg.add_reaction(const.emoji_check)

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.emoji.name == const.emoji_check and payload.member.name not in variable.players_joined:
      variable.players_joined.append(payload.member.name)

def createlist():
  role = []
  for _ in range(variable.wolves_no):
    role.append('wolf')
  for _ in range(variable.witch_no):
    role.append('witch')
  for _ in range(variable.prophet_no):
    role.append('prophet')
  return role

async def startgame(message):
  variable.role_dict = {}
  role = createlist()
  if len(role) > len(variable.players_joined):
    await message.channel.send(const.tooManyRoleError)
    return
  temp_players = variable.players_joined[:]
  random.shuffle(temp_players)
  for i in range(len(in_game)):
    try:
      role_dict[temp_players.pop()] = temp_role.pop()
    except:
      role_dict[temp_players.pop()] = 'Trash'
  await message.channel.send(const.GameStart)

def setup(bot):
  bot.add_cog(Start(bot))
  print("start.py is loaded")