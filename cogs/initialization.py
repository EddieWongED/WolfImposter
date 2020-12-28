import discord
from discord.ext import commands
from data import const
from data import variable
import sqlite3

class Initialization(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=const.commands["initialization"])
  async def initialization(self, ctx):
    guild_id = ctx.guild.id
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    #initializate channels
    cursor.execute(f"SELECT category_id, wolves_channel_id, witches_channel_id, prophets_channel_id FROM main WHERE guild_id = {guild_id}")
    db.commit()
    category_id, wolves_channel_id, witches_channel_id, prophets_channel_id = cursor.fetchone()
    category = ctx.guild.get_channel(category_id)
    print(category)
    if category_id == None or category == None:
      category = await ctx.guild.create_category("WolfImposter")
      category_id = category.id
      cursor.execute(f"UPDATE main SET category_id = {category_id} WHERE guild_id = {guild_id}")
  
    category = ctx.guild.get_channel(category_id)

    wolves_channel = self.bot.get_guild(guild_id).get_channel(wolves_channel_id)
    
    if wolves_channel_id == None or wolves_channel == None:
      wolves_channel = await ctx.guild.create_text_channel(const.emoji_wolves + ' | wolves-channel',category=category)
      wolves_channel_id = wolves_channel.id
      cursor.execute(f"UPDATE main SET wolves_channel_id = {wolves_channel_id} WHERE guild_id = {guild_id}")
      db.commit()
      embed = discord.Embed(title=const.creating_channel_title["wolves"], description=const.creating_channel_description["wolves"], color=0x0000ff)
      msg = await ctx.message.channel.send(embed=embed)
    elif wolves_channel.category != category:
        await wolves_channel.edit(category = category)

    witches_channel = self.bot.get_guild(guild_id).get_channel(witches_channel_id)

    if witches_channel_id == None or witches_channel == None:
      witches_channel = await ctx.guild.create_text_channel(const.emoji_witches + ' | witches-channel',category=category)
      witches_channel_id = witches_channel.id
      cursor.execute(f"UPDATE main SET witches_channel_id = {witches_channel_id} WHERE guild_id = {guild_id}")
      db.commit()
      embed = discord.Embed(title=const.creating_channel_title["witches"], description=const.creating_channel_description["witches"], color=0x0000ff)
      msg = await ctx.message.channel.send(embed=embed)
    elif witches_channel.category != category:
      await witches_channel.edit(category = category)

    prophets_channel = self.bot.get_guild(guild_id).get_channel(prophets_channel_id)

    if prophets_channel_id == None or prophets_channel == None:
      prophets_channel = await ctx.guild.create_text_channel(const.emoji_prophets + ' | prophets-channel',category=category)
      prophets_channel_id = prophets_channel.id
      cursor.execute(f"UPDATE main SET prophets_channel_id = {prophets_channel_id} WHERE guild_id = {guild_id}")
      db.commit()
      embed = discord.Embed(title=const.creating_channel_title["prophets"], description=const.creating_channel_description["prophets"], color=0x0000ff)
      msg = await ctx.message.channel.send(embed=embed)
    elif prophets_channel.category != category:
      await prophets_channel.edit(category = category)

    #initializate roles
    cursor.execute(f"SELECT villagers_role_id, wolves_role_id, witches_role_id, prophets_role_id FROM main WHERE guild_id = {guild_id}")
    db.commit()
    villagers_role_id, wolves_role_id, witches_role_id, prophets_role_id = cursor.fetchone()
    
    villagers_role = self.bot.get_guild(guild_id).get_role(villagers_role_id)

    if villagers_role_id == None or villagers_role == None:
      villagers_role = await ctx.guild.create_role(name = 'Villagers')
      villagers_role_id = villagers_role.id
      cursor.execute(f"UPDATE main SET villagers_role_id = {villagers_role_id} WHERE guild_id = {guild_id}")
      embed = discord.Embed(title=const.creating_role_title["villagers"], description=const.creating_role_description["villagers"], color=0xff00ff)
      msg = await ctx.message.channel.send(embed=embed)
      db.commit()
    else:
      villagers_role = self.bot.get_guild(guild_id).get_role(villagers_role_id)
    
    wolves_role = self.bot.get_guild(guild_id).get_role(wolves_role_id)

    if wolves_role_id == None or wolves_role == None:
      wolves_role = await ctx.guild.create_role(name = 'Wolves')
      wolves_role_id = wolves_role.id
      cursor.execute(f"UPDATE main SET wolves_role_id = {wolves_role_id} WHERE guild_id = {guild_id}")
      db.commit()
      embed = discord.Embed(title=const.creating_role_title["wolves"], description=const.creating_role_description["wolves"], color=0xff00ff)
      msg = await ctx.message.channel.send(embed=embed)

    else:
      wolves_role = self.bot.get_guild(guild_id).get_role(wolves_role_id)

    witches_role = self.bot.get_guild(guild_id).get_role(witches_role_id)

    if witches_role_id == None or witches_role == None:
      witches_role = await ctx.guild.create_role(name = 'Witches')
      witches_role_id = witches_role.id
      cursor.execute(f"UPDATE main SET witches_role_id = {witches_role_id} WHERE guild_id = {guild_id}")
      db.commit()
      embed = discord.Embed(title=const.creating_role_title["witches"], description=const.creating_role_description["witches"], color=0xff00ff)
      msg = await ctx.message.channel.send(embed=embed)

    else:
      witches_role = self.bot.get_guild(guild_id).get_role(witches_role_id)

    prophets_role = self.bot.get_guild(guild_id).get_role(prophets_role_id)

    if prophets_role_id == None or prophets_role == None:
      prophets_role = await ctx.guild.create_role(name = 'Prophets')
      prophets_role_id = prophets_role.id
      cursor.execute(f"UPDATE main SET prophets_role_id = {prophets_role_id} WHERE guild_id = {guild_id}")
      db.commit()
      embed = discord.Embed(title=const.creating_role_title["prophets"], description=const.creating_role_description["prophets"], color=0xff00ff)
      msg = await ctx.message.channel.send(embed=embed)
    else:
      prophets_role = self.bot.get_guild(guild_id).get_role(prophets_role_id)

    #initializate permission
    overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False), wolves_role: discord.PermissionOverwrite(read_messages=True)}
    await wolves_channel.edit(overwrites = overwrites)
    overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False), witches_role: discord.PermissionOverwrite(read_messages=True)}
    await witches_channel.edit(overwrites = overwrites)
    overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False), prophets_role: discord.PermissionOverwrite(read_messages=True)}
    await prophets_channel.edit(overwrites = overwrites)
    cursor.close()
    db.close()

  @commands.command(aliases=['cr'])
  async def createrole(self, ctx):
    guild_id = ctx.guild.id
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()

    
    variable.wolf_role = await ctx.guild.create_role(name = 'InGame')
    overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False), variable.wolf_role: discord.PermissionOverwrite(read_messages=True)}
    await variable.wolf_channel.edit(overwrites = overwrites)

    variable.witch_role = await ctx.guild.create_role(name = 'InGame')
    overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False), variable.witch_role: discord.PermissionOverwrite(read_messages=True)}
    await variable.witch_channel.edit(overwrites = overwrites)

    variable.prophet_role = await ctx.guild.create_role(name = 'InGame')
    overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False), variable.prophet_role: discord.PermissionOverwrite(read_messages=True)}
    await variable.prophet_channel.edit(overwrites = overwrites)

    cursor.close()
    db.close()
    await ctx.message.add_reaction(const.emoji_check)

  @commands.command(aliases=['dr'])
  async def delrole(self, ctx):
    await delRole(ctx, 'InGame')
    await ctx.message.add_reaction(const.emoji_check)

    
def getChannel(ctx,name):
  for text_channel in ctx.guild.channels:
    if text_channel.name == name:
      return text_channel

def getCategory(ctx, name):
  for category in ctx.guild.categories:
      if category.name == name:
        return category

async def delRole(ctx, name):
  for role in ctx.guild.roles:
    if role.name == name:
      await role.delete()
  
def setup(bot):
  bot.add_cog(Initialization(bot))
  print("initialization.py is loaded")