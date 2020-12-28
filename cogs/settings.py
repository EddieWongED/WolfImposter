import discord
from discord.ext import commands
from data import const
from data import variable
from cogs import players, wolves, witches, prophets
import sqlite3
class Settings(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=const.commands["settings"])
  async def settings(self, ctx):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT players_no, wolves_no, witches_no, prophets_no FROM main WHERE guild_id = {ctx.guild.id}")
    db.commit()
    players_no, wolves_no, witches_no, prophets_no = cursor.fetchone()
    embed = discord.Embed(title="Settings", description="React to change the settings", color=0x00ff00)
    embed.add_field(name="Number of Players" + const.emoji_players + ":", value=players_no, inline=True)
    embed.add_field(name="Number of Wolves" + const.emoji_wolves + ":", value=wolves_no, inline=True)
    embed.add_field(name="Number of Prophets" + const.emoji_prophets + ":", value=prophets_no, inline=True)
    embed.add_field(name="Number of Witches" + const.emoji_witches + ":", value=witches_no, inline=True)
    msg = await ctx.message.channel.send(embed=embed)
    for role in const.role_emoji_dict:
      await msg.add_reaction(const.role_emoji_dict[role])
    variable.bot_message_id["settings"] = msg.id
    variable.last_ctx = ctx
    cursor.close()
    db.close()

  
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    guild = self.bot.get_guild(payload.guild_id)
    channel = guild.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if payload.member.bot:
      return
    if payload.message_id == variable.bot_message_id["settings"]:
      if payload.emoji.name == const.emoji_players:
        await players.Players.players(self,variable.last_ctx)
        await message.delete()
        variable.bot_message_id["settings"] = ""
      elif payload.emoji.name == const.emoji_wolves:
        await wolves.Wolves.wolves(self,variable.last_ctx)
        await message.delete()
        variable.bot_message_id["settings"] = ""
      elif payload.emoji.name == const.emoji_witches:
        await witches.Witches.witches(self,variable.last_ctx)
        await message.delete()
        variable.bot_message_id["settings"] = ""
      elif payload.emoji.name == const.emoji_prophets:
        await prophets.Prophets.prophets(self,variable.last_ctx)
        await message.delete()
        variable.bot_message_id["settings"] = ""

    

def setup(bot):
  bot.add_cog(Settings(bot))
  print("settings.py is loaded")