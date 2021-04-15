from load_config import get_database
from modules.basic_cog import *


class ConfigurationManager(BasicCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.group(name="config", pass_context=True)
    async def config(self, ctx: commands.Context):
        database = get_database()
        print(database.admin_role_name)

def setup(bot):
    bot.add_cog(ConfigurationManager(bot))