# Plex Manager for Discord
This Discord bot will allow you to manage users on a Plex Media Server via Discord.
You can add and remove users, start trials, invite winners, check access, enforce blacklists, and match Discord users with associated Plex users.

**NOTE:** This is a standalone version of a feature from Arca, a larger multi-purpose bot that includes Plex management and statistics, as well as Emby/Jellyfin management, sports scores, and a variety of other features. This bot will likely not receive much attention from the developer, as it is meant as a temporary stop gap while Arca is undergoing a major rewrite.

# Installation
1. Fork this repo with ``git clone https://github.com/nwithan8/PlexManager.git``
2. Enter the ``PlexManager`` directory.
3. Install dependencies with ``pip install -r requirements.txt``
4. Complete ``settings.py`` with settings for your Discord and Plex servers.
   4a. Get a Discord bot token by following this tutorial to set up and invite a Discord bot to your server: https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-the-developer-portal
5. Enter the ``credentials/admin`` directory.
6. Rename ``example.json`` as ``[YOUR DISCORD SERVER ID].json`` and complete the settings inside the file.
7. Run the bot from the ``PlexManager`` directory with ``python bot.py``

# Usage
You can see all available functions by typing ``[YOUR BOT PREFIX]help pm`` in Discord.

Help message:
```
*[pm|PM|PlexMan|plexman|PlexManager|plexmanager] 

Plex admin commands

Commands:
  access     Check if you or another user has access to the Plex server
  add        Add a Discord user to Plex
  blacklist  Blacklist a Plex username or Discord ID
  cleandb    Remove old users from database_handler
  count      Check Plex share count
  details    Get Plex restrictions for a user
  edit       Update an existing Plex user's restrictions. Can edit library access, ratings and sync ability
  purge      Remove inactive winners
  remove     Remove a Discord user from Plex
  status     Check if the Plex server(s) is/are online
  subcheck   Find and removed lapsed subscribers
  trial      Start a Plex trial
  trialcheck Find and remove lapsed trials
  trials     List trials' Plex usernames
  users      List users' Plex usernames
  whois      Find Discord or Plex user
  winner     Add a winner to Plex
  winners    List winners' Plex usernames

Type *help command for more info on a command.
You can also type *help category for more info on a category.
```
