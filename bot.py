#!/usr/bin/python3

import discord
from discord.ext import commands
import settings as settings

bot = commands.Bot(command_prefix=settings.DISCORD_BOT_PREFIX)

formatter = commands.HelpCommand(show_check_failure=False)

bot.load_extension("plex.plex_manager")

@bot.event
async def on_ready():
    print(f'\n\nLogged in as : {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=f'the waiting game | {settings.DISCORD_BOT_PREFIX}'))
    print(f'Successfully logged in and booted...!\n')


print("PlexManager Copyright (C) 2020  Nathan Harris\n"
      "This program comes with ABSOLUTELY NO WARRANTY\n"
      "This is free software, and you are welcome to redistribute it under certain conditions.")

bot.run(settings.DISCORD_BOT_TOKEN)
