from data import const

bot_message_id = {}
players_joined = []
last_ctx = None
role_dict = {}    #key=name, value=(role object, name of role)
state_dict = {}
state_str = {}

main_channel = None
wolf_message = None
witch_message1 = None
witch_message2 = None
prophet_message = None
vote_message = None
voted = []
votes = {}

killing = None #Member object
witch_kill = True
witch_rescue = True
witch_killing = None #Member object
prophet_search = None

just_dead = []