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
    embed = discord.Embed(title="Starting...", description=const.starting_str, color=0x0000ff)
    msg = await ctx.message.channel.send(embed=embed)
    variable.bot_message_id["start"] = msg.id
    await msg.add_reaction(const.emoji_check)

  @commands.command()
  async def teststart(self, ctx):
    await startgame(ctx)

  @commands.command(aliases=['ri'])
  async def resetInGame(self, ctx):
    variable.players_joined = []
    await ctx.message.add_reaction(const.emoji_check)


  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.emoji.name == const.emoji_check and payload.member.name not in variable.players_joined and not payload.member.bot:
      variable.players_joined.append(payload.member.name)

def createlist():
  role = []
  for _ in range(variable.wolves_no):
    role.append('wolf')
  for _ in range(variable.witches_no):
    role.append('witch')
  for _ in range(variable.prophets_no):
    role.append('prophet')
  random.shuffle(role)
  role.insert(0,'wolf')
  print(f'Role: {role}')
  return role

def genRoleDict():
  variable.role_dict = {}
  role = createlist()
  temp_players = variable.players_joined[:]
  random.shuffle(temp_players)
  for i in range(len(variable.players_joined)):
    try:
      variable.role_dict[temp_players.pop()] = role.pop()
    except:
      variable.role_dict[temp_players.pop()] = 'Trash'

async def startgame(ctx):
  genRoleDict()
  await ctx.send(variable.role_dict)

def setup(bot):
  bot.add_cog(Start(bot))
  print("start.py is loaded")