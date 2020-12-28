import discord
from discord.ext import commands
from data import const

class Help(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=const.commands["help"])
  async def help(self, ctx):
    print("testing")
    await ctx.send(const.settings_str)

def setup(bot):
  bot.add_cog(Help(bot))
  print("help.py is loaded")