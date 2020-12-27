emoji_1 = "1️⃣"
emoji_2 = "2️⃣"
emoji_3 = "3️⃣"
emoji_4 = "4️⃣"
emoji_5 = "5️⃣"
emoji_6 = "6️⃣"
emoji_7 = "7️⃣"
emoji_8 = "8️⃣"
emoji_9 = "9️⃣"
emoji_check = '✅'
numbers = {1:emoji_1, 2:emoji_2, 3:emoji_3, 4:emoji_4, 5:emoji_5, 6:emoji_6, 7:emoji_7, 8:emoji_8, 9:emoji_9}

commands = {
"settings": ["setting", "set", "s"], 
"players": ["player", "play", "p"], 
"wolves": ["imposter", "wolf"],
"witches": ["witch"],
"prophets": ["prophet","prop"], 
"start": ["begin"], 
"help": ["starter"], 
"role": ["role"]}

settings_str = '''Settings:
>>>Set the amount of players: use $players
>>>Set the amount of wolves: use $wolves
>>>Set the amount of witch: use $witch
>>>Set the amount of Prophet: use $prophet
'''

starting_str = '''Waiting for players to join...
React on the tick to join'''

tooManyRoleError = '''***Error:***
>>> ```css
As the number of roles is greater than the number of players, the game is stopped.```'''

GameStart = 'Players in game match the number of players, the game is starting.'