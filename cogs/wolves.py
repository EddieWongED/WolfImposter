import discord
from discord.ext import commands
from data import const
from data import variable

class Wolves(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  def createEmbed():
    embed = discord.Embed(title="Wolves" + const.emoji_wolves, description=const.wolves_str, color=0xffff00)
    embed.add_field(name = "Now: ", value=variable.wolves_no)
    embed.add_field(name = "Max: ", value=const.wolves_max)
    embed.add_field(name = "Min: ", value=const.wolves_min)
    return embed

  @commands.command(aliases=const.commands["wolves"])
  async def wolves(self, ctx):
    global msg
    msg = await ctx.message.channel.send(embed = Wolves.createEmbed())
    variable.bot_message_id["wolves"] = msg.id
    await msg.add_reaction(const.emoji_plus)
    await msg.add_reaction(const.emoji_minus)
  
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    global msg
    if payload.message_id == variable.bot_message_id["wolves"] and not payload.member.bot:
      if const.emoji_plus == payload.emoji.name and variable.wolves_no < const.wolves_max:
        variable.wolves_no +=1
        await msg.edit(embed = Wolves.createEmbed())
      elif const.emoji_minus == payload.emoji.name and variable.wolves_no > const.wolves_min:
        variable.wolves_no -=1
        await msg.edit(embed = Wolves.createEmbed())

def setup(bot):
  bot.add_cog(Wolves(bot))
  print("wolves.py is loaded")