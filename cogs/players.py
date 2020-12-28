import discord
from discord.ext import commands
from data import const
from data import variable
import sqlite3

class Players(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  def createEmbed(guild_id):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT players_no FROM main WHERE guild_id = {guild_id} LIMIT 1")
    db.commit()
    players_no = cursor.fetchone()[0]
    embed = discord.Embed(title="Players" + const.emoji_players, description=const.players_str, color=0xffff00)
    embed.add_field(name = "Now: ", value=players_no)
    embed.add_field(name = "Max: ", value=const.players_max)
    embed.add_field(name = "Min: ", value=const.players_min)
    cursor.close()
    db.close()
    return embed

  @commands.command(aliases=const.commands["players"])
  async def players(self, ctx):
    global msg
    msg = await ctx.message.channel.send(embed = Players.createEmbed(ctx.guild.id))
    variable.bot_message_id["players"] = msg.id
    await msg.add_reaction(const.emoji_plus)
    await msg.add_reaction(const.emoji_minus)

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    global msg
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT players_no FROM main WHERE guild_id = {payload.guild_id} LIMIT 1")
    db.commit()
    players_no = cursor.fetchone()[0]
    if payload.message_id == variable.bot_message_id["players"] and not payload.member.bot:
      if const.emoji_plus == payload.emoji.name and players_no < const.players_max:
        sql = ("UPDATE main SET players_no = ? WHERE guild_id = ?")
        val = (players_no + 1, payload.guild_id)
        cursor.execute(sql, val)
        db.commit()
        await msg.edit(embed = Players.createEmbed(payload.guild_id))
      elif const.emoji_minus == payload.emoji.name and players_no > const.players_min:
        sql = ("UPDATE main SET players_no = ? WHERE guild_id = ?")
        val = (players_no - 1, payload.guild_id)
        cursor.execute(sql, val)
        db.commit()
        await msg.edit(embed = Players.createEmbed(payload.guild_id))
    cursor.close()
    db.close()

def setup(bot):
  bot.add_cog(Players(bot))
  print("players.py is loaded")