import discord
from discord.ext import commands
from data import const
from data import variable

class Prophets(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(aliases=const.commands["prophets"])
  async def prophets(self, ctx):
    embed = discord.Embed(title="Prophets", description=const.prophets_str, color=0xffff00)
    msg = await ctx.message.channel.send(embed = embed)
    variable.bot_message_id["prophets"] = msg.id
    for i in range(1, 4):
      await msg.add_reaction(const.numbers[i])

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.message_id == variable.bot_message_id["prophets"]:
      for number in const.numbers:
        if const.numbers[number] == payload.emoji.name:
          variable.prophets_no = number

def setup(bot):
  bot.add_cog(Prophets(bot))
  print("prophets.py is loaded")