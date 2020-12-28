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
    await roundWolf(self, ctx)
    # await startgame(ctx)

  @commands.command(aliases=['ri'])
  async def resetInGame(self, ctx):
    variable.players_joined = []
    await ctx.message.add_reaction(const.emoji_check)

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.message_id != variable.bot_message_id["start"]:
      return
    if payload.emoji.name == const.emoji_check and payload.member.name not in variable.players_joined and not payload.member.bot:
      variable.players_joined.append(payload.member.name)

  

def createlist():
  role = []
  trash = variable.players_no - variable.wolves_no - variable.witches_no - variable.prophets_no
  for _ in range(variable.wolves_no):
    role.append('wolf')
  for _ in range(variable.witches_no):
    role.append('witch')
  for _ in range(variable.prophets_no):
    role.append('prophet')
  for _ in range(trash):
    role.append('trash')
  random.shuffle(role)
  role.insert(-1,'wolf')
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
      variable.role_dict[temp_players.pop()] = 'trash'

async def startgame(ctx):
  genRoleDict()
  await ctx.send(variable.role_dict)

async def roundWolf(self, ctx):
  guild = ctx.guild
  channel = ctx.channel
  await channel.send('Hi')
  # self.send_message(self.get_channel(''))

def setup(bot):
  bot.add_cog(Start(bot))
  print("start.py is loaded")