import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
TOKEN = config["settings"]["TOKEN"]
ADMINS = config["settings"]["admins"].split(",")
ADMINS = [int(admin) for admin in ADMINS]
channel_id = config["settings"]["channel_id"]
