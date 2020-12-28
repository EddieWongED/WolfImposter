import discord
from discord.ext import commands
from data import const
from data import variable
import sqlite3

class Prophets(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  def createEmbed(guild_id):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT prophets_no FROM main WHERE guild_id = {guild_id} LIMIT 1")
    db.commit()
    prophets_no = cursor.fetchone()[0]
    embed = discord.Embed(title="Prophets" + const.emoji_prophets, description=const.prophets_str, color=0xffff00)
    embed.add_field(name = "Now: ", value=prophets_no)
    embed.add_field(name = "Max: ", value=const.prophets_max)
    embed.add_field(name = "Min: ", value=const.prophets_min)
    cursor.close()
    db.close()
    return embed

  @commands.command(aliases=const.commands["prophets"])
  async def prophets(self, ctx):
    global msg
    msg = await ctx.message.channel.send(embed = Prophets.createEmbed(ctx.guild.id))
    variable.bot_message_id["prophets"] = msg.id
    await msg.add_reaction(const.emoji_plus)
    await msg.add_reaction(const.emoji_minus)

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    global msg
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT prophets_no FROM main WHERE guild_id = {payload.guild_id} LIMIT 1")
    db.commit()
    prophets_no = cursor.fetchone()[0]
    if payload.message_id == variable.bot_message_id["prophets"] and not payload.member.bot:
      if const.emoji_plus == payload.emoji.name and prophets_no < const.prophets_max:
        sql = ("UPDATE main SET prophets_no = ? WHERE guild_id = ?")
        val = (prophets_no + 1, payload.guild_id)
        cursor.execute(sql, val)
        db.commit()
        await msg.edit(embed = Prophets.createEmbed(payload.guild_id))
      elif const.emoji_minus == payload.emoji.name and prophets_no > const.prophets_min:
        sql = ("UPDATE main SET prophets_no = ? WHERE guild_id = ?")
        val = (prophets_no - 1, payload.guild_id)
        cursor.execute(sql, val)
        db.commit()
        await msg.edit(embed = Prophets.createEmbed(payload.guild_id))
    cursor.close()
    db.close()

def setup(bot):
  bot.add_cog(Prophets(bot))
  print("prophets.py is loaded")