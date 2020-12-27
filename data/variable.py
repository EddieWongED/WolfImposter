from data import const

bot_message_id = {}
players_joined = []
players_no = 0
wolves_no = 0
witches_no = 0
prophets_no = 0
last_ctx = None
role_dict = {}
role_no_emoji_dict = {
  "players": [players_no, const.emoji_players],
  "wolves": [f'At least 1 + {wolves_no}', const.emoji_wolves],
  "witches": [witches_no, const.emoji_witches],
  "prophets": [prophets_no, const.emoji_prophets]}