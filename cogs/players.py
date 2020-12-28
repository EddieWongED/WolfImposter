import discord
from discord.ext import commands
from data import const
from data import variable

class Players(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  def createEmbed():
    embed = discord.Embed(title="Players" + const.emoji_players, description=const.players_str, color=0xffff00)
    embed.add_field(name = "Now: ", value=variable.players_no)
    embed.add_field(name = "Max: ", value=const.players_max)
    embed.add_field(name = "Min: ", value=const.players_min)
    return embed

  @commands.command(aliases=const.commands["players"])
  async def players(self, ctx):
    global msg
    msg = await ctx.message.channel.send(embed = Players.createEmbed())
    variable.bot_message_id["players"] = msg.id
    await msg.add_reaction(const.emoji_plus)
    await msg.add_reaction(const.emoji_minus)

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    global msg
    if payload.message_id == variable.bot_message_id["players"] and not payload.member.bot:
      if const.emoji_plus == payload.emoji.name and variable.players_no < const.players_max:
        variable.players_no +=1
        await msg.edit(embed = Players.createEmbed())
      elif const.emoji_minus == payload.emoji.name and variable.players_no > const.players_min:
        variable.players_no -=1
        await msg.edit(embed = Players.createEmbed())

def setup(bot):
  bot.add_cog(Players(bot))
  print("players.py is loaded")