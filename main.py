import discord
from discord.ext import commands
import os
import sqlite3
from data import const
from data import variable
from keep_alive import keep_alive


prefix = "$"
client = commands.Bot(command_prefix = prefix)
client.remove_command("help")

@client.command(aliases = ['l'])
async def load(ctx, extension):
  try:
    client.load_extension(f'cogs.{extension}')
    await ctx.message.add_reaction(const.emoji_check)
  except Exception as e:
    embed = discord.Embed(title="Error Occurred " + const.emoji_cross, description=f"error occurred while loading module {extension}:\n{e}", color=0xffff00)
    await ctx.send(embed=embed)
    await ctx.message.add_reaction(const.emoji_cross)

@client.command(aliases = ['ul'])
async def unload(ctx, extension):
  try:
    client.unload_extension(f'cogs.{extension}')
    await ctx.message.add_reaction(const.emoji_check)
  except Exception as e:
    embed = discord.Embed(title="Error Occurred " + const.emoji_cross, description=f"error occurred while unloading module {extension}:\n{e}", color=0xffff00)
    await ctx.send(embed=embed)
    await ctx.message.add_reaction(const.emoji_cross)

@client.command(aliases = ['rl'])
async def reload(ctx, extension):
  error = False
  try:
    client.unload_extension(f'cogs.{extension}')
  except Exception as e:
    error = True
    embed = discord.Embed(title="Error Occurred " + const.emoji_cross, description=f"error occurred while unloading module {extension}:\n{e}", color=0xffff00)
    await ctx.send(embed=embed)
    await ctx.message.add_reaction(const.emoji_cross)
  
  try:
    client.load_extension(f'cogs.{extension}')
    await ctx.message.add_reaction(const.emoji_check)
  except Exception as e:
    error = True
    embed = discord.Embed(title="Error Occurred " + const.emoji_cross, description=f"error occurred while loading module {extension}:\n{e}", color=0xffff00)
    await ctx.send(embed=embed)
    await ctx.message.add_reaction(const.emoji_cross)
  if not error:
    await ctx.message.add_reaction(const.emoji_check)

@client.command(aliases = ['rlall','rla'])
async def reloadall(ctx):
  error = False
  for extension in os.listdir('./cogs'):
    if extension.endswith(".py"):
      try:
          client.unload_extension(str("cogs." + extension)[:-3])
      except Exception as e:
        error = True
        embed = discord.Embed(title="Error Occurred " + const.emoji_cross, description=f"error occurred while unloading module {extension}:\n{e}", color=0xffff00)
        await ctx.send(embed=embed)
        await ctx.message.add_reaction(const.emoji_cross)
      try:
          client.load_extension(str("cogs." + extension)[:-3])
      except Exception as e:
        error = True
        embed = discord.Embed(title="Error Occurred " + const.emoji_cross, description=f"error occurred while loading module {extension}:\n{e}", color=0xffff00)
        await ctx.send(embed=embed)
        await ctx.message.add_reaction(const.emoji_cross)
  if not error:
    await ctx.message.add_reaction(const.emoji_check)

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
    sql = (f"INSERT INTO main(guild_id, players_no, wolves_no, witches_no, prophets_no) VALUES({message.guild.id}, 5, 1, 1, 1)")
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
    sql = (f"INSERT INTO main(guild_id, players_no, wolves_no, witches_no, prophets_no) VALUES({guild.id}, 5, 1, 1, 1)")
    cursor.execute(sql)
    print("db has created")
  db.commit()
  cursor.close()
  db.close()


main()