import discord
from discord.ext import commands
from data import const
from data import variable
import sqlite3
from data import retrieve
class Initialization(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=const.commands["initialization"])
  async def initialization(self, ctx):
    guild_id = ctx.guild.id
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT main_channel_id, wolves_channel_id, witches_channel_id, prophets_channel_id FROM main WHERE guild_id = {guild_id}")
    db.commit()
    category_id = retrieve.retrieve_category_id(self, guild_id)
    main_channel_id, wolves_channel_id, witches_channel_id, prophets_channel_id = cursor.fetchone()

    category = ctx.guild.get_channel(category_id)
    print(category)
    if category_id == None or category == None:
      category = await ctx.guild.create_category("WolfImposter")
      category_id = category.id
      cursor.execute(f"UPDATE main SET category_id = {category_id} WHERE guild_id = {guild_id}")
  
    category = ctx.guild.get_channel(category_id)

    wolves_channel = self.bot.get_guild(guild_id).get_channel(wolves_channel_id)
    
    if wolves_channel_id == None or wolves_channel == None:
      wolves_channel = await ctx.guild.create_text_channel(const.emoji_wolves + ' wolves-channel',category=category)
      wolves_channel_id = wolves_channel.id
      cursor.execute(f"UPDATE main SET wolves_channel_id = {wolves_channel_id} WHERE guild_id = {guild_id}")
      db.commit()
      embed = discord.Embed(title=const.creating_channel_title["wolves"], description=const.creating_channel_description["wolves"], color=0x0000ff)
      msg = await ctx.message.channel.send(embed=embed)
    elif wolves_channel.category != category:
        await wolves_channel.edit(category = category)

    witches_channel = self.bot.get_guild(guild_id).get_channel(witches_channel_id)

    if witches_channel_id == None or witches_channel == None:
      witches_channel = await ctx.guild.create_text_channel(const.emoji_witches + ' witches-channel',category=category)
      witches_channel_id = witches_channel.id
      cursor.execute(f"UPDATE main SET witches_channel_id = {witches_channel_id} WHERE guild_id = {guild_id}")
      db.commit()
      embed = discord.Embed(title=const.creating_channel_title["witches"], description=const.creating_channel_description["witches"], color=0x0000ff)
      msg = await ctx.message.channel.send(embed=embed)
    elif witches_channel.category != category:
      await witches_channel.edit(category = category)

    prophets_channel = self.bot.get_guild(guild_id).get_channel(prophets_channel_id)

    if prophets_channel_id == None or prophets_channel == None:
      prophets_channel = await ctx.guild.create_text_channel(const.emoji_prophets + ' prophets-channel',category=category)
      prophets_channel_id = prophets_channel.id
      cursor.execute(f"UPDATE main SET prophets_channel_id = {prophets_channel_id} WHERE guild_id = {guild_id}")
      db.commit()
      embed = discord.Embed(title=const.creating_channel_title["prophets"], description=const.creating_channel_description["prophets"], color=0x0000ff)
      msg = await ctx.message.channel.send(embed=embed)
    elif prophets_channel.category != category:
      await prophets_channel.edit(category = category)

    main_channel = self.bot.get_guild(guild_id).get_channel(main_channel_id)

    if main_channel_id == None or main_channel == None:
      main_channel = await ctx.guild.create_text_channel("    " + const.emoji_main + ' main-channel',category=category)
      main_channel_id = main_channel.id
      cursor.execute(f"UPDATE main SET main_channel_id = {main_channel_id} WHERE guild_id = {guild_id}")
      db.commit()
      embed = discord.Embed(title=const.creating_channel_title["main"], description=const.creating_channel_description["main"], color=0x0000ff)
      msg = await ctx.message.channel.send(embed=embed)
    elif main_channel.category != category:
      await main_channel.edit(category = category)

    #initializate roles
    cursor.execute(f"SELECT villagers_role_id, wolves_role_id, witches_role_id, prophets_role_id, deaths_role_id FROM main WHERE guild_id = {guild_id}")
    db.commit()

    villagers_role_id, wolves_role_id, witches_role_id, prophets_role_id, deaths_role_id = cursor.fetchone()

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

    deaths_role = self.bot.get_guild(guild_id).get_role(deaths_role_id)

    if deaths_role_id == None or deaths_role == None:
      deaths_role = await ctx.guild.create_role(name = 'Dead')
      deaths_role_id = deaths_role.id
      cursor.execute(f"UPDATE main SET deaths_role_id = {deaths_role_id} WHERE guild_id = {guild_id}")
      embed = discord.Embed(title=const.creating_role_title["deaths"], description=const.creating_role_description["deaths"], color=0xff00ff)
      msg = await ctx.message.channel.send(embed=embed)
      db.commit()
    else:
      deaths_role = self.bot.get_guild(guild_id).get_role(deaths_role_id)
    
    #initializate permission

    overwrites = wolves_channel.overwrites_for(villagers_role)
    overwrites.view_channel = False
    await wolves_channel.set_permissions(villagers_role, overwrite=overwrites)
    overwrites = wolves_channel.overwrites_for(witches_role)
    overwrites.view_channel = False
    await wolves_channel.set_permissions(witches_role, overwrite=overwrites)
    overwrites = wolves_channel.overwrites_for(prophets_role)
    overwrites.view_channel = False
    await wolves_channel.set_permissions(prophets_role, overwrite=overwrites)

    overwrites = witches_channel.overwrites_for(villagers_role)
    overwrites.view_channel = False
    await witches_channel.set_permissions(villagers_role, overwrite=overwrites)
    overwrites = witches_channel.overwrites_for(wolves_role)
    overwrites.view_channel = False
    await witches_channel.set_permissions(wolves_role, overwrite=overwrites)
    overwrites = witches_channel.overwrites_for(prophets_role)
    overwrites.view_channel = False
    await witches_channel.set_permissions(prophets_role, overwrite=overwrites)
    await ctx.message.add_reaction(const.emoji_check)

    overwrites = prophets_channel.overwrites_for(villagers_role)
    overwrites.view_channel = False
    await prophets_channel.set_permissions(villagers_role, overwrite=overwrites)
    overwrites = prophets_channel.overwrites_for(wolves_role)
    overwrites.view_channel = False
    await prophets_channel.set_permissions(wolves_role, overwrite=overwrites)
    overwrites = prophets_channel.overwrites_for(witches_role)
    overwrites.view_channel = False
    await prophets_channel.set_permissions(witches_role, overwrite=overwrites)
    
    
    #removing role from members
    role_list = retrieve.retrieve_roles(self, guild_id)
    print(ctx.guild.members)
    for member in ctx.guild.members:
      print(member)
      if not member.bot:
        for role in role_list:
          await member.remove_roles(role)
    await ctx.message.add_reaction(const.emoji_check)

    return
    overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False), wolves_role: discord.PermissionOverwrite(read_messages=True)}
    await wolves_channel.edit(overwrites = overwrites)
    overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False), witches_role: discord.PermissionOverwrite(read_messages=True)}
    await witches_channel.edit(overwrites = overwrites)
    overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False), prophets_role: discord.PermissionOverwrite(read_messages=True)}
    await prophets_channel.edit(overwrites = overwrites)
    overwrites = {deaths_role: discord.PermissionOverwrite(send_messages=False)}
    await main_channel.edit(overwrites = overwrites)
    cursor.close()
    db.close()
    

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