from load_config import get_database
from modules.basic_cog import *


class ConfigurationManager(BasicCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.group(name="config", pass_context=True)
    async def config(self, ctx: commands.Context):
        await self.what_subcommand(ctx=ctx)

    @config.command(name="prefix", pass_context=True)
    async def config_change_prefix(self, ctx: commands.Context, new_prefix: str):
        database = get_database()
        if database.set_bot_prefix(prefix=new_prefix):
            await self.respond(item="Prefix updated. You'll need to restart the bot for this to take effect.", ctx=ctx)


def setup(bot):
    bot.add_cog(ConfigurationManager(bot))