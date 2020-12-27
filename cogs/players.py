import discord
from discord.ext import commands
from data import const
from data import variable

class Players(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(aliases=const.commands["players"])
  async def players(self, ctx):
    msg = await ctx.message.channel.send('>>> ```Number of players: ```')
    variable.bot_message_id["players"] = msg.id
    for i in range(1, 10):
      await msg.add_reaction(const.numbers[i])

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.message_id == variable.bot_message_id["players"]:
      for number in const.numbers:
        if const.numbers[number] == payload.emoji.name:
          variable.players_no = number

def setup(bot):
  bot.add_cog(Players(bot))
  print("players.py is loaded")