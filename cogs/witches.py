import discord
from discord.ext import commands
from data import const
from data import variable

class Witches(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  def createEmbed():
    embed = discord.Embed(title="Witches" + const.emoji_witches, description=const.witches_str, color=0xffff00)
    embed.add_field(name = "Now: ", value=variable.witches_no)
    embed.add_field(name = "Max: ", value=const.witches_max)
    embed.add_field(name = "Min: ", value=const.witches_min)
    return embed
  
  @commands.command(aliases=const.commands["witches"])
  async def witches(self, ctx):
    global msg
    msg = await ctx.message.channel.send(embed = Witches.createEmbed())
    variable.bot_message_id["witches"] = msg.id
    await msg.add_reaction(const.emoji_plus)
    await msg.add_reaction(const.emoji_minus)

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    global msg
    if payload.message_id == variable.bot_message_id["witches"] and not payload.member.bot:
      if const.emoji_plus == payload.emoji.name and variable.witches_no < const.witches_max:
        variable.witches_no +=1
        await msg.edit(embed = Witches.createEmbed())
      elif const.emoji_minus == payload.emoji.name and variable.witches_no > 0:
        variable.witches_no -=1
        await msg.edit(embed = Witches.createEmbed())

def setup(bot):
  bot.add_cog(Witches(bot))
  print("witches.py is loaded")