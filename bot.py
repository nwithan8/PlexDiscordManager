#!/usr/bin/python3

from discord.ext import commands

from configuration.settings_manager import SettingsManager
from modules import load_config
from modules.discord_helper import get_cog_by_name
from setup import set_defaults

set_defaults()

bot_prefix = load_config.get_bot_prefix()
bot_token = load_config.get_bot_token()

bot = commands.Bot(command_prefix=bot_prefix)

formatter = commands.HelpCommand(show_check_failure=False)

bot.load_extension("plex.plex_manager")
bot.load_extension("configuration.configuration_manager")
bot.load_extension("modules.event_manager")

settings_manager = SettingsManager()
config_manager = get_cog_by_name(bot=bot, cog_name="ConfigurationManager")
config_manager.set_settings_manager(settings_manager)
plex_manager = get_cog_by_name(bot=bot, cog_name="PlexManager")
plex_manager.set_settings_manager(settings_manager)


print("PlexManager Copyright (C) 2021  Nathan Harris\n"
      "This program comes with ABSOLUTELY NO WARRANTY\n"
      "This is free software, and you are welcome to redistribute it under certain conditions.")

bot.run(bot_token)
