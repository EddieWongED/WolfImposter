import discord
from discord.ext import commands
from data import const
from data import variable
import sqlite3
class Witches(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  def createEmbed(guild_id):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT witches_no FROM main WHERE guild_id = {guild_id} LIMIT 1")
    db.commit()
    witches_no = cursor.fetchone()[0]
    embed = discord.Embed(title="Witches" + const.emoji_witches, description=const.witches_str, color=0xffff00)
    embed.add_field(name = "Now: ", value=witches_no)
    embed.add_field(name = "Max: ", value=const.witches_max)
    embed.add_field(name = "Min: ", value=const.witches_min)
    cursor.close()
    db.close()
    return embed

  @commands.command(aliases=const.commands["witches"])
  async def witches(self, ctx):
    global msg
    msg = await ctx.message.channel.send(embed = Witches.createEmbed(ctx.guild.id))
    variable.bot_message_id["witches"] = msg.id
    await msg.add_reaction(const.emoji_plus)
    await msg.add_reaction(const.emoji_minus)

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    global msg
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT witches_no FROM main WHERE guild_id = {payload.guild_id} LIMIT 1")
    db.commit()
    witches_no = cursor.fetchone()[0]
    if payload.message_id == variable.bot_message_id["witches"] and not payload.member.bot:
      if const.emoji_plus == payload.emoji.name and witches_no < const.witches_max:
        sql = ("UPDATE main SET witches_no = ? WHERE guild_id = ?")
        val = (witches_no + 1, payload.guild_id)
        cursor.execute(sql, val)
        db.commit()
        await msg.edit(embed = Witches.createEmbed(payload.guild_id))
      elif const.emoji_minus == payload.emoji.name and witches_no > const.witches_min:
        sql = ("UPDATE main SET witches_no = ? WHERE guild_id = ?")
        val = (witches_no - 1, payload.guild_id)
        cursor.execute(sql, val)
        db.commit()
        await msg.edit(embed = Witches.createEmbed(payload.guild_id))
    cursor.close()
    db.close()

def setup(bot):
  bot.add_cog(Witches(bot))
  print("witches.py is loaded")