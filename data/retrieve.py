import sqlite3

def retrieve_channels(self, guild_id):
  db = sqlite3.connect("main.sqlite")
  cursor = db.cursor()
  cursor.execute(f"SELECT main_channel_id, wolves_channel_id, witches_channel_id, prophets_channel_id FROM main WHERE guild_id = {guild_id}")
  db.commit()
  main_channel_id, wolves_channel_id, witches_channel_id, prophets_channel_id = cursor.fetchone()
  cursor.close()
  db.close()
  main_channel = self.bot.get_guild(guild_id).get_channel(main_channel_id)
  wolves_channel = self.bot.get_guild(guild_id).get_channel(wolves_channel_id)
  witches_channel = self.bot.get_guild(guild_id).get_channel(witches_channel_id)
  prophets_channel = self.bot.get_guild(guild_id).get_channel(prophets_channel_id)
  return main_channel, wolves_channel, witches_channel, prophets_channel

def retrieve_roles(self, guild_id):
  db = sqlite3.connect("main.sqlite")
  cursor = db.cursor()
  cursor.execute(f"SELECT villagers_role_id, wolves_role_id, witches_role_id, prophets_role_id, deaths_role_id FROM main WHERE guild_id = {guild_id}")
  db.commit()
  villagers_role_id, wolves_role_id, witches_role_id, prophets_role_id, deaths_role_id = cursor.fetchone()
  cursor.close()
  db.close()
  villagers_role = self.bot.get_guild(guild_id).get_role(villagers_role_id)
  wolves_role = self.bot.get_guild(guild_id).get_role(wolves_role_id)
  witches_role = self.bot.get_guild(guild_id).get_role(witches_role_id)
  prophets_role = self.bot.get_guild(guild_id).get_role(prophets_role_id)
  deaths_role = self.bot.get_guild(guild_id).get_role(deaths_role_id)
  return villagers_role, wolves_role, witches_role, prophets_role, deaths_role

def retrieve_nos(self, guild_id):
  db = sqlite3.connect("main.sqlite")
  cursor = db.cursor()
  cursor.execute(f"SELECT players_no, wolves_no, witches_no, prophets_no FROM main WHERE guild_id = {guild_id}")
  db.commit()
  players_no, wolves_no, witches_no, prophets_no = cursor.fetchone()
  cursor.close()
  db.close()
  return players_no, wolves_no, witches_no, prophets_no

def retrieve_prefix(self, guild_id):
  db = sqlite3.connect("main.sqlite")
  cursor = db.cursor()
  cursor.execute(f"SELECT prefix FROM main WHERE guild_id = {guild_id}")
  db.commit()
  prefix = cursor.fetchone()
  cursor.close()
  db.close()
  return prefix[0]

def retrieve_category_id(self, guild_id):
  db = sqlite3.connect("main.sqlite")
  cursor = db.cursor()
  cursor.execute(f"SELECT category_id From main where guild_id = {guild_id}")
  db.commit()
  category_id = cursor.fetchone()
  cursor.close()
  db.close()
  return category_id[0]
  