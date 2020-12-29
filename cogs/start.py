import discord
from discord.ext import commands
from data import const
from data import variable
import time
import random
from cogs import initialization
from data import retrieve

class Start(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=const.commands["start"])
  async def start(self, ctx):
    await initialization.Initialization.initialization(self, ctx)

    variable.players_joined = []
    
    guild_id = ctx.guild.id
    main_cheannel, wolves_channel, witches_channel, prophets_channel = retrieve.retrieve_channels(self, guild_id)
    villagers_role, wolves_role, witches_role, prophets_role, deaths_role = retrieve.retrieve_roles(self, guild_id)
    await wolves_channel.purge(limit=99)
    await witches_channel.purge(limit=99)
    await prophets_channel.purge(limit=99)
    embed = discord.Embed(title="Starting...", description=const.starting_str, color=const.color_green)
    msg = await ctx.message.channel.send(embed=embed)
    variable.bot_message_id["start"] = msg.id
    await msg.add_reaction(const.emoji_check)
    for i in range(5, 0, -1):
      time.sleep(1)
      embed.description = const.starting_str + f"\nGame starts in {i} second(s)"
      await msg.edit(embed=embed)
    await msg.delete()
    await startgame(self, ctx)


  @commands.command(aliases=['eg'])
  async def endGame(self, ctx):
    await endGame(self, ctx.guild.id)

  @commands.command(aliases=['ri'])
  async def resetInGame(self, ctx):
    variable.players_joined = []
    await ctx.message.add_reaction(const.emoji_check)

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    guild_id = payload.guild_id
    main_channel, wolves_channel, witches_channel, prophets_channel = retrieve.retrieve_channels(self, guild_id)
    if not payload.member.bot:
      if payload.emoji.name == const.emoji_check and payload.member.name not in variable.players_joined and payload.message_id == variable.bot_message_id["start"]:
        variable.players_joined.append(payload.member)

      elif variable.wolf_message != None and payload.message_id == variable.wolf_message.id:
        for num in const.numbers:
          if payload.emoji.name == const.numbers[num]:
            variable.killing = variable.state_dict[num][0]
        embed = discord.Embed(title = f"{const.emoji_blood} You've killed {variable.killing.name}.", color = const.color_red)
        msg = await wolves_channel.send(embed=embed)
        await variable.wolf_message.delete()
        for i in range(5,0,-1): 
          time.sleep(1)
          embed.description = f"This message will be dismissed in {i} second(s)"
          await msg.edit(embed=embed)
        await msg.delete()
        await roundWitch1(self, payload)
      
      elif variable.witch_message1 != None and payload.message_id == variable.witch_message1.id:
        if payload.emoji.name == const.emoji_syringe:
          variable.witch_rescue = False
          await variable.witch_message1.delete()
          await witches_channel.purge(limit=1)
          embed = discord.Embed(title = f"{const.emoji_syringe} You rescued {variable.killing.name}.", color = const.color_green)
          msg = await witches_channel.send(embed=embed)
          variable.killing = None
          for i in range(5,0,-1): 
            time.sleep(1)
            embed.description = f"This message will be dismissed in {i} second(s)"
            await msg.edit(embed=embed)
          await msg.delete()
          await roundProphet(self, payload)

        elif payload.emoji.name == const.emoji_knife:
          variable.witch_kill = False
          await variable.witch_message1.delete()
          await roundWitch2(self, payload)

        elif payload.emoji.name == const.emoji_cross:
          await variable.witch_message1.delete()
          embed = discord.Embed(title = f"{const.emoji_cross} You've skipped this turn.", color = const.color_red)
          msg = await witches_channel.send(embed=embed)
          for i in range(5,0,-1): 
            time.sleep(1)
            embed.description = f"This message will be dismissed in {i} second(s)"
            await msg.edit(embed=embed)
          await msg.delete()
          await witches_channel.purge(limit=1)
          await roundProphet(self, payload)
      
      elif variable.witch_message2 != None and payload.message_id == variable.witch_message2.id:
        for num in const.numbers:
          if payload.emoji.name == const.numbers[num]:
            variable.witch_killing = variable.state_dict[num][0]
        embed = discord.Embed(title = f"Killing: {variable.witch_killing.name}", color = const.color_red)
        msg = await witches_channel.send(embed=embed)
        for i in range(5,0,-1): 
            time.sleep(1)
            embed.description = f"This message will be dismissed in {i} second(s)"
            await msg.edit(embed=embed)
        await msg.delete()
        await variable.witch_message2.delete()
        await roundProphet(self, payload)

      elif variable.prophet_message != None and payload.message_id == variable.prophet_message.id:
        for num in const.numbers:
          if payload.emoji.name == const.numbers[num]:
            variable.prophet_search = variable.state_dict[num][0]
        await variable.prophet_message.delete()
        for player in variable.role_dict:
          if player == variable.prophet_search:
            if variable.role_dict[player][1] != "Wolf":
              embed = discord.Embed(title=f"{player.name} is {const.emoji_good}")
              msg = await prophets_channel.send(embed=embed)
              for i in range(5,0,-1): 
                time.sleep(1)
                embed.description = f"This message will be dismissed in {i} second(s)"
                await msg.edit(embed=embed)
              await msg.delete()
            else:
              embed = discord.Embed(title=f"{player.name} is {const.emoji_bad}")
              msg = await prophets_channel.send(embed=embed)
              for i in range(5,0,-1): 
                time.sleep(1)
                embed.description = f"This message will be dismissed in {i} second(s)"
                await msg.edit(embed=embed)
              await msg.delete()
        await roundDay(self, payload)

      elif variable.vote_message != None and payload.message_id == variable.vote_message.id and payload.member.id not in variable.voted:
        for num in const.numbers:
          if payload.emoji.name == const.numbers[num]:
            variable.votes[variable.state_dict[num][0]].append(payload.member)
        variable.voted.append(payload.member.id)
        await variable.vote_message.remove_reaction(payload.emoji, payload.member)
        await main_channel.send(f"{payload.member} has voted.")

def createlist(self, ctx):
  guild_id = ctx.guild.id
  role = []

  players_no, wolves_no, witches_no, prophets_no = retrieve.retrieve_nos(self, guild_id)
  villagers_role, wolves_role, witches_role, prophets_role, deaths_role = retrieve.retrieve_roles(self, guild_id)

  villager_no = players_no - wolves_no - witches_no - prophets_no
  for _ in range(wolves_no - 1):
    role.append((wolves_role,"Wolf"))
  for _ in range(witches_no):
    role.append((witches_role,"Witch"))
  for _ in range(prophets_no):
    role.append((prophets_role,"Prophet"))
  for _ in range(villager_no):
    role.append((villagers_role,"Villager"))
  random.shuffle(role)
  role.insert(0,(wolves_role,"Wolf"))

  print(f'Role: {role}')
  return role

def genRoleDict(self, ctx):
  variable.role_dict = {}
  role = createlist(self, ctx)
  print(f'Player_Joined:\n{variable.players_joined}')
  print(f'Player_Joined:\n{len(variable.players_joined)}')
  temp_players = variable.players_joined[:]
  random.shuffle(temp_players)
  print(f'TEMP:\n{temp_players}')
  print(f'TEMP:\n{len(temp_players)}')
  # variable.role_dict[temp_players[0]] = role[0]
  for i in range(0,len(variable.players_joined)):
    variable.role_dict[temp_players[i]] = role[i]
  
# def genStateStr():
#   variable.state_str = ""
#   for i in variable.state_dict:
#     variable.state_str += f"{i} : {variable.state_dict[i][0].name}, {variable.state_dict[i][1]}\n"

def genStateDict():
  variable.state_dict = {}
  for i in range(0, len(variable.players_joined)):
    variable.state_dict[i+1] = [variable.players_joined[i], "Alive"]

def genDeathMsg():
  if len(variable.just_dead) == 0:
    DeathMsg = "Nobody die last night."
  elif len(variable.just_dead) == 1:
    DeathMsg = f'{variable.just_dead[0].name} was killed last night.'
  elif len(variable.just_dead) == 2:
    if variable.just_dead[0].name == variable.just_dead[1].name:
      DeathMsg = f'{variable.just_dead[0].name} was killed last night.'
    else:
      DeathMsg = f'{variable.just_dead[0].name} and {variable.just_dead[1].name} were killed last night.'
  return DeathMsg

def cleanVoteDict():
  variable.votes = {}
  for key in variable.state_dict:
    if variable.state_dict[key][1] == "Alive":
      variable.votes[variable.state_dict[key][0]] = []

def countVote():
  votes_no = {}
  for player in variable.votes:
    votes_no[player] = len(variable.votes[player])
  max_vote = max(votes_no.values())
  votingout = []
  for player in votes_no:
    if votes_no[player] == max_vote:
      votingout.append(player)
  return votingout

def genVoteResult():
  vote_result = ''
  for player in variable.votes:
    vote_result += f'{player.name}: '
    for votes in variable.votes[player]:
      vote_result += f'{votes.name} '
    vote_result += '\n'
  return vote_result


async def applyDeath(self, payload):
  variable.just_dead = []
  guild_id = payload.guild_id
  villagers_role, wolves_role, witches_role, prophets_role, deaths_role = retrieve.retrieve_roles(self, guild_id)

  for key in variable.state_dict:
    if variable.state_dict[key][0] == variable.killing:
      variable.state_dict[key][1] = "Killed"
      variable.just_dead.append(variable.killing)
      await variable.killing.add_roles(deaths_role)
    if variable.state_dict[key][0] == variable.witch_killing:
      variable.state_dict[key][1] = "Killed"
      variable.just_dead.append(variable.witch_killing)
      await variable.killing.add_roles(deaths_role)

  variable.killing = None
  variable.witch_killing = None

async def assignRoles():
  for player in variable.role_dict:
    await player.add_roles(variable.role_dict[player][0])

async def startgame(self, ctx):
  genRoleDict(self, ctx)
  await assignRoles()
  genStateDict()
  variable.killing = None
  variable.witch_killing = None
  variable.witch_kill = True
  variable.witch_rescue = True
  variable.voted = []
  guild_id = ctx.guild.id
  await roundNight(self,guild_id)
  clear_str = ''
  for player in variable.role_dict:
    clear_str += f'{player.name} : {variable.role_dict[player][1]}\n'
  await ctx.send(clear_str)

async def roundWolf(self, guild_id):
  main_channel, wolves_channel, witches_channel, prophets_channel = retrieve.retrieve_channels(self, guild_id)

  embed = discord.Embed(title = const.emoji_moon + " " + const.main_wolves_turn_title, description = const.main_wolves_turn_description, color = const.color_purple)
  await main_channel.send(embed = embed)
  
  embed = discord.Embed(title=const.emoji_knife + " " + const.wolves_kill_title + " " + const.emoji_wolves, description=const.wolves_kill_description, color=const.color_purple)
  for key in variable.state_dict:
    if variable.state_dict[key][1] == "Alive":
      embed.add_field(name=variable.state_dict[key][0],value=const.numbers[key], inline=True)
  variable.wolf_message = await wolves_channel.send(embed=embed)
  
  for key in variable.state_dict:
    if variable.state_dict[key][1] == "Alive":
      await variable.wolf_message.add_reaction(const.numbers[key])

async def roundWitch1(self, payload):
  guild_id = payload.guild_id
  main_channel, wolves_channel, witches_channel, prophets_channel = retrieve.retrieve_channels(self, guild_id)
  
  embed = discord.Embed(title = const.emoji_moon + " " + const.main_witches_turn_title, description = const.main_witches_turn_description, color = const.color_green)
  await main_channel.send(embed = embed)

  if variable.witch_rescue:
    embed = discord.Embed(title = const.emoji_blood + " " + const.witches_rescue_title, description = variable.killing.name + const.witches_rescue_description, color = const.color_red)
    await witches_channel.send(embed=embed)
  
  variable.witch_message1 = await witches_channel.send("Do you want to save the victim with your life potion or kill with your death potion?")

  if variable.witch_rescue:
    await variable.witch_message1.add_reaction(const.emoji_syringe)
  if variable.witch_kill:
    await variable.witch_message1.add_reaction(const.emoji_knife)
  await variable.witch_message1.add_reaction(const.emoji_cross)

async def roundWitch2(self, payload):
  guild_id = payload.guild_id
  main_channel, wolves_channel, witches_channel, prophets_channel = retrieve.retrieve_channels(self, guild_id)
  
  variable.witch_message2 = await witches_channel.send("Who do you want to kill with your death potion?")

  embed = discord.Embed(title=const.witches_kill_title, description=const.witches_kill_description, color=const.color_purple)
  for key in variable.state_dict:
    if variable.state_dict[key][1] == "Alive":
      embed.add_field(name=variable.state_dict[key][0],value=const.numbers[key], inline=True)
  variable.witch_message2 = await witches_channel.send(embed=embed)
  
  for key in variable.state_dict:
    if variable.state_dict[key][1] == "Alive":
      await variable.witch_message2.add_reaction(const.numbers[key])

async def roundProphet(self, payload):
  guild_id = payload.guild_id
  main_channel, wolves_channel, witches_channel, prophets_channel = retrieve.retrieve_channels(self, guild_id)
  
  embed = discord.Embed(title = const.emoji_moon + " " + const.main_prophets_turn_title, description = const.main_prophets_turn_description, color = const.color_purple)
  await main_channel.send(embed = embed)
  
  embed = discord.Embed(title=const.prophets_title, description=const.prophets_description, color=const.color_purple)
  for key in variable.state_dict:
    embed.add_field(name=variable.state_dict[key][0],value=const.numbers[key], inline=True)
  variable.prophet_message = await prophets_channel.send(embed=embed)
  
  for key in variable.state_dict:
    await variable.prophet_message.add_reaction(const.numbers[key])
    
async def roundDay(self, payload):
  guild_id = payload.guild_id
  main_channel, wolves_channel, witches_channel, prophets_channel = retrieve.retrieve_channels(self, guild_id)
  villagers_role, wolves_role, witches_role, prophets_role, deaths_role = retrieve.retrieve_roles(self, guild_id)
  embed = discord.Embed(title = const.emoji_sunrise + " " + "Morning arrives, and everyone wakes up.", color = const.color_purple)
  await main_channel.send(embed=embed)

  await applyDeath(self, payload)
  embed = discord.Embed(title=genDeathMsg(), color=const.color_red)
  await main_channel.send(embed=embed)
  #Add checking here
  temp = []
  players_left = 0
  for key in variable.state_dict:
    if variable.state_dict[key][1] == "Alive":
      players_left += 1
      temp.append(variable.state_dict[key][0])
  wolves_left = 0
  for key in variable.role_dict:
    if variable.role_dict[key][1] == "Wolf":
      wolves_left += 1
  print(f"wolves_left = {wolves_left}")
  print(f"players_left = {players_left}")
  if wolves_left <= 0:
    await villagersWin(self, payload)
    return
  elif wolves_left >= players_left - wolves_left:
    await wolvesWin(self, payload)
    return
  else:
    pass
  #End of checking
  embed = discord.Embed(title=const.voting_title, description=const.voting_description, color=const.color_purple)
  for key in variable.state_dict:
    if variable.state_dict[key][1] == "Alive":
      embed.add_field(name=variable.state_dict[key][0],value=const.numbers[key], inline=True)
  variable.vote_message = await main_channel.send(embed=embed)
  
  for key in variable.state_dict:
    if variable.state_dict[key][1] == "Alive":
      await variable.vote_message.add_reaction(const.numbers[key])

  cleanVoteDict()
  for i in range(10, 0, -1):
    time.sleep(1)
    embed.description = const.voting_description + f"\nDiscussion ends in {i} second(s)"
    await variable.vote_message.edit(embed=embed)
    if len(variable.voted) == len(variable.players_joined):
      break
  
  await variable.vote_message.delete()
  variable.voted = []
  votingout = countVote()
  await main_channel.send(genVoteResult())
  if len(votingout) == 1:
    embed = discord.Embed(title=f"{votingout[0].name} was voted out.", color=const.color_red)
    await main_channel.send(embed=embed)
    for key in variable.state_dict:
      if variable.state_dict[key][0] == votingout[0]:
        variable.state_dict[key][1] = "Killed"
        await votingout[0].add_roles(deaths_role)
  else:
    embed = discord.Embed(title=f"Nobody was voted out.", color=const.color_red)
    await main_channel.send(embed=embed)
  
  #Check
  temp = []
  players_left = 0
  for key in variable.state_dict:
    if variable.state_dict[key][1] == "Alive":
      players_left += 1
      temp.append(variable.state_dict[key][0])
  wolves_left = 0
  for key in variable.role_dict:
    if variable.role_dict[key][1] == "Wolf":
      wolves_left += 1
  print(f"wolves_left = {wolves_left}")
  print(f"players_left = {players_left}")
  if wolves_left <= 0:
    await villagersWin(self, payload)
  elif wolves_left >= players_left - wolves_left:
    await wolvesWin(self, payload)
  else:
    await roundNight(self, payload)

async def roundNight(self, guild_id):
  main_channel, wolves_channel, witches_channel, prophets_channel = retrieve.retrieve_channels(self, guild_id)
  embed = discord.Embed(title = const.emoji_sun_falling + " " + const.day_end_title, description = const.day_end_description, color = const.color_green)
  await main_channel.send(embed=embed)
  await roundWolf(self, guild_id)

async def villagersWin(self, payload):
  guild_id = payload.guild_id
  main_channel, wolves_channel, witches_channel, prophets_channel = retrieve.retrieve_channels(self, guild_id)
  embed = discord.Embed(title=f"Congratulations! Victory is for the villagers!", color=const.color_red)
  await main_channel.send(embed=embed)
  await endGame(self, guild_id)

async def wolvesWin(self, payload):
  guild_id = payload.guild_id
  main_channel, wolves_channel, witches_channel, prophets_channel = retrieve.retrieve_channels(self, guild_id)
  embed = discord.Embed(title=f"Congratulations! Victory is for the wolves!", color=const.color_red)
  await main_channel.send(embed=embed)
  await endGame(self, guild_id)

async def endGame(self, guild_id):
  villagers_role, wolves_role, witches_role, prophets_role, deaths_role = retrieve.retrieve_roles(self, guild_id)
  for player in variable.role_dict:
    await player.remove_roles(variable.role_dict[player][0])
    try:
      await player.remove_roles(deaths_role)
    except:
      pass

def setup(bot):
  bot.add_cog(Start(bot))
  print("start.py is loaded")