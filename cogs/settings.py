import discord
from discord.ext import commands
from data import const
from data import variable
from cogs import players, wolves, witches, prophets
from data import retrieve
import sqlite3
class Settings(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.group(aliases=const.commands["settings"], invoke_without_command=True)
  async def settings(self, ctx):
    players_no, wolves_no, witches_no, prophets_no = retrieve.retrieve_nos(self, ctx.guild.id)
    prefix = retrieve.retrieve_prefix(self, ctx.guild.id)
    embed = discord.Embed(title="Settings", description="React to change the settings", color=0x00ff00)
    embed.add_field(name="Number of Players" + const.emoji_players + ":", value=players_no, inline=True)
    embed.add_field(name="Number of Wolves" + const.emoji_wolves + ":", value=wolves_no, inline=True)
    embed.add_field(name="Number of Prophets" + const.emoji_prophets + ":", value=prophets_no, inline=True)
    embed.add_field(name="Number of Witches" + const.emoji_witches + ":", value=witches_no, inline=True)
    embed.add_field(name="Prefix" + ":", value=prefix, inline=True)
    msg = await ctx.message.channel.send(embed=embed)
    for role in const.role_emoji_dict:
      await msg.add_reaction(const.role_emoji_dict[role])
    variable.bot_message_id["settings"] = msg.id
    variable.last_ctx = ctx

  
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

  @settings.command()
  async def prefix(self, ctx, arg):
    print(arg)
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    sql = ("UPDATE main SET prefix = ? WHERE guild_id = ?")
    val = (arg, ctx.guild.id)
    cursor.execute(sql, val)
    db.commit()
    await ctx.message.add_reaction(const.emoji_check)
    cursor.close()
    db.close()



def setup(bot):
  bot.add_cog(Settings(bot))
  print("settings.py is loaded")