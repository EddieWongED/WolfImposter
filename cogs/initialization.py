import discord
from discord.ext import commands
from data import const
from data import variable

class Initialization(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=const.commands["initialization"])
  async def initialization(self, ctx):
    variable.category = getCategory(ctx,"WolfImposter")
    variable.wolf_channel = getChannel(ctx, "wolf-channel")
    variable.witch_channel = getChannel(ctx, "witch-channel")
    variable.prophet_channel = getChannel(ctx, "prophet-channel")
    print(ctx.guild.channels)
    
    if variable.category == None:
      await ctx.guild.create_category("WolfImposter")
      variable.category = getCategory(ctx,"WolfImposter")
    
    if variable.wolf_channel == None:
      await ctx.guild.create_text_channel('wolf-channel', category=variable.category)
      variable.wolf_channel = getChannel(ctx, "wolf-channel")
      embed = discord.Embed(title=const.creating_channel_title["wolf"], description=const.creating_channel_description["wolf"], color=0x0000ff)
      msg = await ctx.message.channel.send(embed=embed)

    if variable.witch_channel == None:
      await ctx.guild.create_text_channel('witch-channel', category=variable.category)
      variable.witch_channel = getChannel(ctx, "witch-channel")
      embed = discord.Embed(title=const.creating_channel_title["witch"], description=const.creating_channel_description["witch"], color=0x0000ff)
      msg = await ctx.message.channel.send(embed=embed)

    if variable.prophet_channel == None:
      await ctx.guild.create_text_channel('prophet-channel', category=variable.category)
      variable.prophet_channel = getChannel(ctx, "prophet-channel")
      embed = discord.Embed(title=const.creating_channel_title["prophet"], description=const.creating_channel_description["prophet"], color=0x0000ff)
      msg = await ctx.message.channel.send(embed=embed)

    if variable.wolf_channel.category != variable.category:
      await variable.wolf_channel.edit(category = variable.category)

    if variable.witch_channel.category != variable.category:
      await variable.witch_channel.edit(category = variable.category)

    if variable.prophet_channel.category != variable.category:
      await variable.prophet_channel.edit(category = variable.category)

    
def getChannel(ctx,name):
  for text_channel in ctx.guild.channels:
    if text_channel.name == name:
      return text_channel

def getCategory(ctx, name):
  for category in ctx.guild.categories:
      if category.name == name:
        return category
  
  
def setup(bot):
  bot.add_cog(Initialization(bot))
  print("initialization.py is loaded")