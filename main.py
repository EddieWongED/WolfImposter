import discord
from discord.ext import commands
import os
from data import const
from data import variable
from keep_alive import keep_alive


prefix = "$"
client = commands.Bot(command_prefix = prefix)

@client.command(aliases = ['l'])
async def load(ctx, extension):
  print(ctx)
  client.load_extension(f'cogs.{extension}')
  await ctx.message.add_reaction(const.emoji_check)

@client.command(aliases = ['ul'])
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')
  await ctx.message.add_reaction(const.emoji_check)

@client.command(aliases = ['rl'])
async def reload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')
  client.load_extension(f'cogs.{extension}')
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
        print(f"Failed to load extension {extension} Error: {e}")

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
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  print(message.content)
  if message.author == client.user:
    return

  await client.process_commands(message)

main()