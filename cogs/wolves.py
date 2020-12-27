import discord
from discord.ext import commands
from data import const
from data import variable

class Wolves(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=const.commands["wolves"])
  async def wolves(self, ctx):
    embed = discord.Embed(title="Wolves", description=const.wolves_str, color=0xffff00)
    msg = await ctx.message.channel.send(embed = embed)
    variable.bot_message_id["wolves"] = msg.id
    for i in range(1, 4):
      await msg.add_reaction(const.numbers[i])
  
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.message_id == variable.bot_message_id["wolves"]:
      for number in const.numbers:
        if const.numbers[number] == payload.emoji.name:
          variable.wolves_no = number

def setup(bot):
  bot.add_cog(Wolves(bot))
  print("wolves.py is loaded")