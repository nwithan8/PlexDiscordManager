from configuration.dm_configuration_manager import DMConfigurationSession
from databases.media_server_connector.tables.table_connector import string_to_config_type
from load_config import get_database
from modules import discord_helper
from modules.basic_cog import *


class ConfigurationManager(BasicCog):
    def __init__(self, bot):
        super().__init__(bot)
        self._dm_session = None

    def start_dm_session(self, user):
        self._dm_session = DMConfigurationSession(bot=self.bot, user=user)

    async def direct_user_to_dm_if_needed(self, ctx: commands.Context):
        if ctx.channel != ctx.author.dm_channel:
            await self.respond("Please see the direct message from the bot.", ctx=ctx)

    @commands.group(name="config", pass_context=True)
    async def config(self, ctx: commands.Context):
        await self.what_subcommand(ctx=ctx)

    @config.command(name="prefix", pass_context=True)
    async def config_change_prefix(self, ctx: commands.Context, new_prefix: str):
        """
        Change the bot's command prefix
        """
        database = get_database()
        admin_id = database.admin_id

        if admin_id != ctx.author.id:  # None =\= something, so will still be locked even if no admin
            await self.respond("This command is locked to admins.", ctx=ctx)
            return

        if database.set_bot_prefix(prefix=new_prefix):  # no need to go into a DM for this
            await self.respond(item="Prefix updated. You'll need to restart the bot for this to take effect.", ctx=ctx)


    @config.command(name="claim", pass_context=True)
    async def config_claim_admin(self, ctx: commands.Context):
        """
        Claim yourself as admin of the bot
        """
        database = get_database()
        admin_id = database.admin_id

        if not admin_id:
            database.set_admin_id(admin_id=ctx.author.id)
            await self.respond("You are now registered as the admin of this bot.", ctx=ctx)
        else:
            await self.respond(f"{discord_helper.mention_user(admin_id)} is already registered as the admin of this bot.", ctx=ctx)

    @config.command(name="vars", pass_context=True)
    async def config_variables(self, ctx: commands.Context, section: str):
        """
        See the variables names and types
        """
        database = get_database()
        admin_id = database.admin_id

        if admin_id != ctx.author.id:  # None =\= something, so will still be locked even if no admin
            await self.respond("This command is locked to admins.", ctx=ctx)
            return

        config_type = string_to_config_type(config_type_string=section)
        if not config_type:
            await self.respond(f"{section} is not a valid configuration section.", ctx=ctx)
            return

        self.start_dm_session(user=ctx.author)
        await self._dm_session.send_config_options_message(config_type=config_type)
        await self.direct_user_to_dm_if_needed(ctx=ctx)

    @config.command(name="show", pass_context=True)
    async def config_show(self, ctx: commands.Context, section: str):
        """
        See the current settings
        """
        database = get_database()
        admin_id = database.admin_id

        if admin_id != ctx.author.id: # None =\= something, so will still be locked even if no admin
            await self.respond("This command is locked to admins.", ctx=ctx)
            return

        config_type = string_to_config_type(config_type_string=section)
        if not config_type:
            await self.respond(f"{section} is not a valid configuration section.", ctx=ctx)
            return

        self.start_dm_session(user=ctx.author)
        await self._dm_session.send_current_config(config_type=config_type)
        await self.direct_user_to_dm_if_needed(ctx=ctx)

    @config.command(name="edit", pass_context=True)
    async def config_edit(self, ctx: commands.Context, section: str, setting_name: str, setting_value: str):
        """
        Edit the settings
        """
        database = get_database()
        admin_id = database.admin_id

        if admin_id != ctx.author.id: # None =\= something, so will still be locked even if no admin
            await self.respond("This command is locked to admins.", ctx=ctx)
            return

        if ctx.channel != ctx.author.dm_channel:
            await ctx.message.delete()
            await self.respond("Please change settings via a direct message with the bot.", ctx=ctx)
            return

        config_type = string_to_config_type(config_type_string=section)
        if not config_type:
            await self.respond(f"{section} is not a valid configuration section.", ctx=ctx)
            return

        # We only get here if we're already in a direct message, so no need to direct user to the DM
        self.start_dm_session(user=ctx.author)
        await self._dm_session.update_config(config_type=section, variable_name=setting_name, variable_value=setting_value)

    @config.command(name="setup", pass_context=True)
    async def config_setup(self, ctx: commands.Context, section: str):
        """
        Setup a settings section for the first time
        """
        database = get_database()
        admin_id = database.admin_id

        if admin_id != ctx.author.id:  # None =\= something, so will still be locked even if no admin
            await self.respond("This command is locked to admins.", ctx=ctx)
            return

        config_type = string_to_config_type(config_type_string=section)
        if not config_type:
            await self.respond(f"{section} is not a valid configuration section.", ctx=ctx)
            return

        self.start_dm_session(user=ctx.author)
        await self.direct_user_to_dm_if_needed(ctx=ctx)
        await self._dm_session.initialize_config(config_type=config_type)


def setup(bot):
    bot.add_cog(ConfigurationManager(bot))