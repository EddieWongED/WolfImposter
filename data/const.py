emoji_1 = "1️⃣"
emoji_2 = "2️⃣"
emoji_3 = "3️⃣"
emoji_4 = "4️⃣"
emoji_5 = "5️⃣"
emoji_6 = "6️⃣"
emoji_7 = "7️⃣"
emoji_8 = "8️⃣"
emoji_9 = "9️⃣"
emoji_check = "✅"
emoji_cross = "❌"
emoji_witches = "🧙"
emoji_players = "🧍"
emoji_prophets = "📖"
emoji_wolves = "🐺"
emoji_plus = "➕"
emoji_minus = "➖"
emoji_knife = "🔪"
emoji_syringe = "💉"
emoji_moon = "🌑"
emoji_sun_falling = "🌇"
emoji_sunrise = "🌅"
emoji_blood = "🩸"
emoji_crystal = "🔮"
emoji_main = "🏘️"
emoji_good = "👍🏻"
emoji_bad = "👎🏻"
color_red = 0xe74c3c
color_purple = 0x8a6cb7
color_green = 0x23a44a
numbers = {1:emoji_1, 2:emoji_2, 3:emoji_3, 4:emoji_4, 5:emoji_5, 6:emoji_6, 7:emoji_7, 8:emoji_8, 9:emoji_9}

witches_max = 1
witches_min = 0
prophets_max = 1
prophets_min = 0
wolves_max = 3
wolves_min = 1
players_max = 10
players_min = 4


commands = {
"settings": ["setting", "set", "s"], 
"players": ["player", "play", "p"], 
"wolves": ["imposter", "wolf"],
"witches": ["witch"],
"prophets": ["prophet","prop"], 
"start": ["starts", "begin"], 
"help": ["starter", "guide"], 
"role": ["role"],
"initialization": ["initialisation", "initial", "init", "ini"]}

role_emoji_dict = {
  "players": emoji_players,
  "wolves": emoji_wolves,
  "witches": emoji_witches,
  "prophets": emoji_prophets
}

settings_str = '''Settings:
>>>Set the amount of players: use $players
>>>Set the amount of wolves: use $wolves
>>>Set the amount of witch: use $witch
>>>Set the amount of Prophet: use $prophet
'''

starting_str = '''Waiting for players to join...
React on the tick to join'''

players_str = '''React to choice the number of players'''

witches_str = '''React to choice the number of witches'''

wolves_str = '''React to choice the number of wolves'''

prophets_str = '''React to choice the number of prophets'''

tooManyRoleError = '''***Error:***
>>> ```css
As the number of roles is greater than the number of players, the game is stopped.```'''

GameStart = 'Players in game match the number of players, the game is starting.'

day_end_title = "Night Starts Falling"

day_end_description = "Night is falling in the village. Everyone is going to sleep."

main_wolves_turn_title = "Night Falls"

main_wolves_turn_description = "Wolves, open your eyes and pick your choice..."

main_witches_turn_title = "Witch, Open Your Eyes"

main_witches_turn_description = "Do you want to use your life potion or death potion?"

main_prophets_turn_title = "Prophet, Open Your Eyes"

main_prophets_turn_description = "Who you want to check?"

wolves_kill_title = "Wolves, It's Yours Move Now..."

wolves_kill_description = "React to who you want to kill. The one with highest vote is getting killed."

witches_kill_title = f"{emoji_knife} Who do you want to kill with your death potion?"

witches_kill_description = "React to who you want to kill."

witches_rescue_title = "Someone was killed..."

witches_rescue_description = " was killed this night."

prophets_title = f"{emoji_crystal} Who would you like to know about?"

prophets_description = "React to who you want to know."

voting_title = "Villagers, it is your job to discover who has murdered the poor and take revenge. You can vote off someone before sunset."

voting_description = "React to who you want to vote. The one with highest vote is getting killed."

creating_channel_title = {"main":"Seems like you dont have main channel yet...\n", "wolves":"Seems like you dont have wolves channel yet...\n", "witches":"Seems like you dont have witches channel yet...\n", "prophets":"Seems like you dont have prophets channel yet...\n"}

creating_channel_description = {"main":"Creating main-channel", "wolves":"Creating wolves-channel...", "witches":"Creating witches-channel...", "prophets":"Creating prophets-channel..."}

creating_role_title = {"wolves":"Seems like you dont have wolves role yet...\n", "witches":"Seems like you dont have witches role yet...\n", "prophets":"Seems like you dont have prophets role yet...\n", "villagers":"Seems like you dont have villagers role yet...\n", "deaths":"Seems like you dont have deaths role yet...\n"}

creating_role_description = {"wolves":"Creating wolves role...", "witches":"Creating witches role...", "prophets":"Creating prophets role...", "villagers": "Creating villagers role...", "deaths":"Creating deaths role...\n"}

create_table_query = '''
      CREATE TABLE IF NOT EXISTS main(
      guild_id INTEGER,
      prefix TEXT,
      main_channel_id INTEGER,
      wolves_channel_id INTEGER,
      witches_channel_id INTEGER,
      prophets_channel_id INTEGER,
      category_id INTEGER,
      villagers_role_id INTEGER,
      wolves_role_id INTEGER,
      witches_role_id INTEGER,
      prophets_role_id INTEGER,
      deaths_role_id INTEGER,
      players_no INTEGER,
      wolves_no INTEGER,
      witches_no INTEGER,
      prophets_no INTEGER
      )
  '''