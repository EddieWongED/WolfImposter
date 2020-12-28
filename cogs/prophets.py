import discord
from discord.ext import commands
from data import const
from data import variable

class Prophets(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  def createEmbed():
    embed = discord.Embed(title="Prophets" + const.emoji_prophets, description=const.prophets_str, color=0xffff00)
    embed.add_field(name = "Now: ", value=variable.prophets_no)
    embed.add_field(name = "Max: ", value=const.prophets_max)
    embed.add_field(name = "Min: ", value=const.prophets_min)
    return embed
  
  @commands.command(aliases=const.commands["prophets"])
  async def prophets(self, ctx):
    global msg
    msg = await ctx.message.channel.send(embed = Prophets.createEmbed())
    variable.bot_message_id["prophets"] = msg.id
    await msg.add_reaction(const.emoji_plus)
    await msg.add_reaction(const.emoji_minus)

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    global msg
    if payload.message_id == variable.bot_message_id["prophets"] and not payload.member.bot:
      if const.emoji_plus == payload.emoji.name and variable.prophets_no < const.prophets_max:
        variable.prophets_no +=1
        await msg.edit(embed = Prophets.createEmbed())
      elif const.emoji_minus == payload.emoji.name and variable.prophets_no > const.prophets_min:
        variable.prophets_no -=1
        await msg.edit(embed = Prophets.createEmbed())

def setup(bot):
  bot.add_cog(Prophets(bot))
  print("prophets.py is loaded")