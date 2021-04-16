import discord
from discord.ext import commands

from modules.classes.basic_cog import BasicCog


class EventManager(BasicCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\n\nLogged in as : {self.bot.user.name} - {self.bot.user.id}\nVersion: {discord.__version__}\n')
        await self.bot.change_presence(status=discord.Status.idle,
                                  activity=discord.Game(name=f'the waiting game | {self.bot.command_prefix}'))
        print(f'Successfully logged in and booted...!\n')

def setup(bot):
    bot.add_cog(EventManager(bot))