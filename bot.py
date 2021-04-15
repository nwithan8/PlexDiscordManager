#!/usr/bin/python3

import discord
from discord.ext import commands

import load_config
from setup import set_defaults

set_defaults()

bot_prefix = load_config.get_bot_prefix()
bot_token = load_config.get_bot_token()

bot = commands.Bot(command_prefix=bot_prefix)

formatter = commands.HelpCommand(show_check_failure=False)

bot.load_extension("plex.plex_manager")
bot.load_extension("configuration.configuration_manager")

@bot.event
async def on_ready():
    print(f'\n\nLogged in as : {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=f'the waiting game | {bot_prefix}'))
    print(f'Successfully logged in and booted...!\n')


print("PlexManager Copyright (C) 2021  Nathan Harris\n"
      "This program comes with ABSOLUTELY NO WARRANTY\n"
      "This is free software, and you are welcome to redistribute it under certain conditions.")

bot.run(bot_token)
