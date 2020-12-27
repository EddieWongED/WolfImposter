import discord
from discord.ext import commands
from data import const
from data import variable

class Witches(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(aliases=const.commands["witches"])
  async def witches(self, ctx):
    embed = discord.Embed(title="Witches", description=const.witches_str, color=0xffff00)
    msg = await ctx.message.channel.send(embed = embed)
    variable.bot_message_id["witches"] = msg.id
    for i in range(1, 4):
      await msg.add_reaction(const.numbers[i])

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.message_id == variable.bot_message_id["witches"]:
      for number in const.numbers:
        if const.numbers[number] == payload.emoji.name:
          variable.witches_no = number

def setup(bot):
  bot.add_cog(Witches(bot))
  print("witches.py is loaded")