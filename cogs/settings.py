import discord
from discord.ext import commands
from data import const
from data import variable

class Settings(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=const.commands["settings"])
  async def settings(self, ctx):
    settings_embed = discord.Embed(title="Settings", description="react to change the settings", color=0x00ff00)
    settings_embed.add_field(name="Number of Players:", value=variable.players_no, inline=True)
    settings_embed.add_field(name="Number of Wolves:", value=variable.wolves_no, inline=True)
    settings_embed.add_field(name="Number of Prophets:", value=variable.prophets_no, inline=True)
    settings_embed.add_field(name="Number of Witches:", value=variable.witches_no, inline=True)
    msg = await ctx.message.channel.send(embed=settings_embed)
    variable.bot_message_id["settings"] = msg.id

def setup(bot):
  bot.add_cog(Settings(bot))
  print("settings.py is loaded")