import discord
from discord.ext import commands
from data import const
from data import variable
from cogs import players, wolves, witches, prophets

class Settings(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=const.commands["settings"])
  async def settings(self, ctx):
    embed = discord.Embed(title="Settings", description="React to change the settings", color=0x00ff00)
    for role in variable.role_no_emoji_dict:
      embed.add_field(name="Number of " + role + variable.role_no_emoji_dict[role][1] + ":", value=variable.role_no_emoji_dict[role][0], inline=True)
    msg = await ctx.message.channel.send(embed=embed)
    for role in variable.role_no_emoji_dict:
      await msg.add_reaction(variable.role_no_emoji_dict[role][1])
    variable.bot_message_id["settings"] = msg.id
    variable.last_ctx = ctx
  
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.member.bot:
      return
    if payload.message_id == variable.bot_message_id["settings"]:
      if payload.emoji.name == const.emoji_players:
        await players.Players.players(self,variable.last_ctx)
      elif payload.emoji.name == const.emoji_wolves:
        await wolves.Wolves.wolves(self,variable.last_ctx)
      elif payload.emoji.name == const.emoji_witches:
        await witches.Witches.witches(self,variable.last_ctx)
      elif payload.emoji.name == const.emoji_prophets:
        await prophets.Prophets.prophets(self,variable.last_ctx)

def setup(bot):
  bot.add_cog(Settings(bot))
  print("settings.py is loaded")