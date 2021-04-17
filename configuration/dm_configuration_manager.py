from typing import Union

import discord
from discord.ext import commands

from databases.media_server_connector.table_connector import ConfigType, config_type_to_table_schema, \
    string_to_config_type, table_schema_to_table, config_type_to_string
from databases.tools import get_table_schema_name, human_type_to_python_type, \
    table_schema_to_discord_embed, table_values_to_discord_embeds, table_schema_to_name_type_pairs
from modules.load_config import get_database
from modules import discord_helper
from modules.classes.dm_session import DMSession

collected_config = []

def generate_config_options_messages(config_type: ConfigType):
    table_schema = config_type_to_table_schema(config_type=config_type)
    table = table_schema_to_table(table_schema=table_schema)
    table_schema_name = get_table_schema_name(table=table_schema)
    return [f"These are the available {discord_helper.bold(table_schema_name)} variables.\n",
            table_schema_to_discord_embed(table_name=table_schema_name, table=table)]

def _add_to_initial_config(message):
    collected_config.append(message.content)
    return True, "Thank you."


class DMConfigurationSession(DMSession):
    def __init__(self, bot: commands.Bot, user: Union[discord.User, discord.Member]):
        super().__init__(bot, user)
        self._database = get_database()

    def generate_setup_script(self, config_type: ConfigType):
        table_schema = config_type_to_table_schema(config_type=config_type)
        table = table_schema_to_table(table_schema=table_schema)
        name_type_pairs = table_schema_to_name_type_pairs(table=table)
        prompt_callback_pairs = []
        for name, type_ in name_type_pairs.items():
            pair = {
                f"{name} ({type_}): ": _add_to_initial_config
            }
            prompt_callback_pairs.append(pair)
        return prompt_callback_pairs

    async def send_config_sections(self):
        section_names = [config_type_to_string(config_type=config_type) for config_type in ConfigType]
        message = "\n".join(section_names)
        await self.send_message(message=message)

    async def send_config_options_message(self, config_type: ConfigType):
        messages = generate_config_options_messages(config_type=config_type)
        await self.send_messages(messages=messages)

    async def send_current_config(self, config_type: ConfigType):
        table_schema = config_type_to_table_schema(config_type=config_type)
        if not table_schema:
            await self.send_message(message="That table_schema does not exist.")
        else:
            table = table_schema_to_table(table_schema=table_schema)
            table_schema_name = get_table_schema_name(table=table_schema)
            get_all = False
            if config_type == ConfigType.Roles:
                get_all = True
            embeds = table_values_to_discord_embeds(database=self._database, table_name=table_schema_name, table=table,
                                                    get_all=get_all)
            await self.send_messages(messages=embeds)

    async def update_config(self, config_type: str, variable_name: str, variable_value: str):
        config_type = string_to_config_type(config_type_string=config_type)
        if config_type:
            table = config_type_to_table_schema(config_type=config_type)
            if table:
                variable_value = human_type_to_python_type(human_type=variable_value)
                if self._database.update_config(table=table, setting_name=variable_name, setting_value=variable_value):
                    await self.send_message(message=f"{variable_name} updated successfully.")
                else:
                    await self.send_message(message=f"Could not update {variable_name}.")

    async def _make_new_config(self, config_type: ConfigType, name_value_pairs: dict):
        table_schema = config_type_to_table_schema(config_type=config_type)
        return self._database.create_initial_config(table=table_schema, **name_value_pairs)

    async def initialize_config(self, config_type: ConfigType):
        global collected_config
        collected_config = []

        prompt_callback_pairs = self.generate_setup_script(config_type=config_type)
        await self.start_interactive_session(prompt_and_callbacks=prompt_callback_pairs, starting_message="Hello", ending_message="End")
        new_variables = collected_config

        name_value_pairs = {}
        table_schema = config_type_to_table_schema(config_type=config_type)
        table = table_schema_to_table(table_schema=table_schema)
        i = 0
        for column in table.columns:
            variable_value = human_type_to_python_type(human_type=new_variables[i])
            name_value_pairs[column.name] = variable_value
            i += 1

        collected_config = []

        success = await self._make_new_config(config_type=config_type, name_value_pairs=name_value_pairs)
        if success:
            await self.send_message(message="New config saved successfully.")
        else:
            await self.send_message(message="Could not save new config.")
