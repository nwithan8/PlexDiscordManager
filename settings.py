# Bot settings
DISCORD_BOT_TOKEN = "XXXXXXXXXX"
DISCORD_BOT_PREFIX = "*"


# Plex playing settings
TERMINATE_MESSAGE = "Please direct message the admin in the Discord server."


# Plex watchlist settings
SUBSCRIBER_WATCHLIST_TITLE = "{}'s Watchlist"
SUBSCRIBER_PLAYLIST_TITLE = "{}'s Playlist"


# Blacklist settings
ENABLE_BLACKLIST = True


# Discord settings
DISCORD_SERVER_ID = 'XXXXXXXX'
DISCORD_ADMIN_ID = 'XXXXXXXXXXX'
DISCORD_ADMIN_ROLE_NAME = 'Admin'


# Subscriber settings
INVITED_ROLE = "Invited" # Role given after someone is added to Plex
AUTO_CHECK_SUBS = False
SUB_ROLES = ["Monthly Subscriber", "Yearly Subscriber", "Winner", "Lifetime Subscriber", "Bot"]  # Users with any of these roles is exempt from removal
EXEMPT_SUBS = [DISCORD_ADMIN_ID]  # Discord IDs for users exempt from subscriber checks/deletion, separated by commas
SUB_CHECK_TIME = 7  # days
CURRENTLY_PLAYING_ROLE_NAME = 'Watching'


# Trial settings
TRIAL_ROLE_NAME = "Trial"  # Role given to a trial user
TRIAL_LENGTH = 24 * 60 * 60  # (seconds) How long a trial lasts
TRIAL_CHECK_FREQUENCY = 15  # (minutes) How often the bot checks for trial expirations


# Credentials settings
CREDENTIALS_FOLDER = 'credentials'
