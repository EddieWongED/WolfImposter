import discord
from discord.ext import commands
import os
import sqlite3
import traceback
import datetime
from data import const
from data import variable
from data import retrieve
from keep_alive import keep_alive

def get_prefix(client, message):
  db = sqlite3.connect("main.sqlite")
  cursor = db.cursor()
  cursor.execute(f"SELECT prefix FROM main WHERE guild_id = {message.guild.id}")
  prefix = cursor.fetchone()
  db.commit()
  cursor.close()
  db.close()
  return prefix

client = commands.Bot(command_prefix = get_prefix)
client.remove_command("help")

@client.command(aliases = ['l'])
async def load(ctx, extension):
  try:
    client.load_extension(f'cogs.{extension}')
    await ctx.message.add_reaction(const.emoji_check)
  except Exception as e:
    embed = discord.Embed(title="Error Occurred While Loading Module " + const.emoji_cross, color=const.color_red)
    embed.add_field(name="Exception", value=e)
    embed.add_field(name="Traceback", value=traceback.format_exc())
    await ctx.send(embed=embed)
    await ctx.message.add_reaction(const.emoji_cross)

@client.command(aliases = ['ul'])
async def unload(ctx, extension):
  try:
    client.unload_extension(f'cogs.{extension}')
    await ctx.message.add_reaction(const.emoji_check)
  except Exception as e:
    embed = discord.Embed(title="Error Occurred While Unloading Module " + const.emoji_cross, color=const.color_red)
    embed.add_field(name="Exception", value=e)
    embed.add_field(name="Traceback", value=traceback.format_exc())
    await ctx.send(embed=embed)
    await ctx.message.add_reaction(const.emoji_cross)

@client.command(aliases = ['rl'])
async def reload(ctx, extension):
  error = False
  try:
    client.unload_extension(f'cogs.{extension}')
  except Exception as e:
    error = True
    embed = discord.Embed(title="Error Occurred While Unloading Module " + const.emoji_cross, color=const.color_red)
    embed.add_field(name="Exception", value=e)
    embed.add_field(name="Traceback", value=traceback.format_exc())
    await ctx.send(embed=embed)
    await ctx.message.add_reaction(const.emoji_cross)
  
  try:
    client.load_extension(f'cogs.{extension}')
    await ctx.message.add_reaction(const.emoji_check)
  except Exception as e:
    error = True
    embed = discord.Embed(title="Error Occurred While Loading Module " + const.emoji_cross, color=const.color_red)
    embed.add_field(name="Exception", value=e)
    embed.add_field(name="Traceback", value=traceback.format_exc())
    await ctx.send(embed=embed)
    await ctx.message.add_reaction(const.emoji_cross)
  if not error:
    await ctx.message.add_reaction(const.emoji_check)
  else:
    error = False

@client.command(aliases = ['rlall','rla'])
async def reloadall(ctx):
  error = False
  for extension in os.listdir('./cogs'):
    if extension.endswith(".py"):
      try:
          client.unload_extension(str("cogs." + extension)[:-3])
      except Exception as e:
        error = True
        embed = discord.Embed(title="Error Occurred While Unloading Module " + const.emoji_cross, color=const.color_red)
        embed.add_field(name="Exception", value=e)
        embed.add_field(name="Traceback", value=traceback.format_exc())
        await ctx.send(embed=embed)
        await ctx.message.add_reaction(const.emoji_cross)
      try:
          client.load_extension(str("cogs." + extension)[:-3])
      except Exception as e:
        error = True
        embed = discord.Embed(title="Error Occurred While Loading Module " + const.emoji_cross, color=const.color_red)
        embed.add_field(name="Exception", value=e)
        embed.add_field(name="Traceback", value=traceback.format_exc())
        await ctx.send(embed=embed)
        await ctx.message.add_reaction(const.emoji_cross)
  if not error:
    await ctx.message.add_reaction(const.emoji_check)
  else:
      error = False

@client.command(aliases = ['t'])
async def test(ctx):
  await ctx.message.add_reaction(const.emoji_check)

def main():
  # load extension from start
  for extension in os.listdir('./cogs'):
    if extension.endswith(".py"):
      try:
          client.load_extension(str("cogs." + extension)[:-3])
      except Exception as e:
        print(f"Error occurred at module {extension}: Exception = {e}")


  # initializate bot_message_id
  for command in const.commands:
    variable.bot_message_id[command] = ""

  # run online
  keep_alive()

  # run the bot
  client.run(os.getenv("TOKEN"))
    
@client.event
async def on_raw_reaction_add(payload):
    pass
    

@client.event
async def on_ready():
  db = sqlite3.connect('main.sqlite')
  cursor = db.cursor()
  cursor.execute(const.create_table_query)
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  print(message.content)
  db = sqlite3.connect("main.sqlite")
  cursor = db.cursor()
  cursor.execute(const.create_table_query)
  cursor.execute(f"SELECT guild_id FROM main WHERE guild_id = {message.guild.id}")
  result = cursor.fetchone()
  if result is None:
    sql = (f"INSERT INTO main(guild_id, prefix, players_no, wolves_no, witches_no, prophets_no) VALUES({message.guild.id}, '$', 5, 1, 1, 1)")
    cursor.execute(sql)
    print("db has created")
  db.commit()
  cursor.close()
  db.close()
  if message.author == client.user:
    return
  await client.process_commands(message)

@client.event
async def on_guild_join(guild):
  db = sqlite3.connect("main.sqlite")
  cursor = db.cursor()
  cursor.execute(const.create_table_query)
  cursor.execute(f"SELECT guild_id FROM main WHERE guild_id = {guild.id}")
  result = cursor.fetchone()
  if result is None:
    sql = (f"INSERT INTO main(guild_id, prefix, players_no, wolves_no, witches_no, prophets_no) VALUES({guild.id}, $, 5, 1, 1, 1)")
    cursor.execute(sql)
    print("db has created")
  db.commit()
  cursor.close()
  db.close()

@client.event
async def on_command_error(ctx, error):
  try:
    if hasattr(ctx.command, "on_error"):
      return
    else:
      embed = discord.Embed(title=f"Error in {ctx.command} {const.emoji_cross}", colour=const.color_red)
      embed.add_field(name="Exception", value=error)
      embed.add_field(name="Traceback", value=traceback.format_exc())
      await ctx.send(embed=embed)
  except:
      embed = discord.Embed(title=f"Error in {ctx.command} {const.emoji_cross}", colour=const.color_red)
      embed.add_field(name="Exception", value=error)
      embed.add_field(name="Traceback", value=traceback.format_exc())
      await ctx.send(embed=embed)

main()