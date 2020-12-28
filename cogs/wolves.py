import discord
from discord.ext import commands
from data import const
from data import variable
import sqlite3
class Wolves(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  def createEmbed(guild_id):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT wolves_no FROM main WHERE guild_id = {guild_id} LIMIT 1")
    db.commit()
    wolves_no = cursor.fetchone()[0]
    embed = discord.Embed(title="Wolves" + const.emoji_wolves, description=const.wolves_str, color=0xffff00)
    embed.add_field(name = "Now: ", value=wolves_no)
    embed.add_field(name = "Max: ", value=const.wolves_max)
    embed.add_field(name = "Min: ", value=const.wolves_min)
    cursor.close()
    db.close()
    return embed

  @commands.command(aliases=const.commands["wolves"])
  async def wolves(self, ctx):
    global msg
    msg = await ctx.message.channel.send(embed = Wolves.createEmbed(ctx.guild.id))
    variable.bot_message_id["wolves"] = msg.id
    await msg.add_reaction(const.emoji_plus)
    await msg.add_reaction(const.emoji_minus)

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    global msg
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT wolves_no FROM main WHERE guild_id = {payload.guild_id} LIMIT 1")
    db.commit()
    wolves_no = cursor.fetchone()[0]
    if payload.message_id == variable.bot_message_id["wolves"] and not payload.member.bot:
      if const.emoji_plus == payload.emoji.name and wolves_no < const.wolves_max:
        sql = ("UPDATE main SET wolves_no = ? WHERE guild_id = ?")
        val = (wolves_no + 1, payload.guild_id)
        cursor.execute(sql, val)
        db.commit()
        await msg.edit(embed = Wolves.createEmbed(payload.guild_id))
      elif const.emoji_minus == payload.emoji.name and wolves_no > const.wolves_min:
        sql = ("UPDATE main SET wolves_no = ? WHERE guild_id = ?")
        val = (wolves_no - 1, payload.guild_id)
        cursor.execute(sql, val)
        db.commit()
        await msg.edit(embed = Wolves.createEmbed(payload.guild_id))
    cursor.close()
    db.close()


def setup(bot):
  bot.add_cog(Wolves(bot))
  print("wolves.py is loaded")