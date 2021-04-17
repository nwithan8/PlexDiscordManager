from typing import List

from sqlalchemy import Table
from sqlalchemy.orm import declarative_base, DeclarativeMeta
from databases.defaults import *
from modules import utils, discord_helper

Base = declarative_base()


def get_column(column_type: ColumnType, **kwargs):
    sql_type = None
    if column_type == ColumnType.DiscordRoleName:
        sql_type = DiscordRoleName
    elif column_type == ColumnType.DiscordUserID:
        sql_type = DiscordUserID
    elif column_type == ColumnType.DiscordServerID:
        sql_type = DiscordServerID
    elif column_type == ColumnType.DiscordUserName:
        sql_type = DiscordUserName
    elif column_type == ColumnType.URL:
        sql_type = URL
    return Column(sql_type, **kwargs)


def get_table_schema_name(table: DeclarativeMeta) -> str:
    return getattr(table, "__name__", None)


def get_table_columns(table: Table) -> List[Column]:
    return table.columns._all_columns


def get_table_column_names(table: Table) -> List[str]:
    columns = get_table_columns(table=table)
    return [column.name for column in columns]


def table_schema_to_name_type_pairs(table: Table):
    columns = get_table_columns(table=table)
    pairs = {}
    ignore_columns = getattr(table, "_ignore", [])
    for column in columns:
        if column not in ignore_columns:
            pairs[column.name] = sql_type_to_human_type_string(column.type)
    return pairs


def table_schema_to_discord_embed(table_name: str, table: Table):
    name_type_pairs = table_schema_to_name_type_pairs(table=table)
    return discord_helper.generate_embed(title=table_name, **name_type_pairs)


def table_values_to_discord_embeds(database, table_name: str, table: Table, get_all: bool = False):
    column_names = [column.name for column in table.columns]
    embeds = []
    if get_all:
        entries = database.get_all_entries(table_schema=table)
    else:
        entries = [database.get_first_entry(table_schema=table)]
    if not entries:
        embeds.append(f"There are no {table_name} entries currently.")
        return embeds
    for entry in entries:
        kwargs = {}
        for column_name in column_names:
            kwargs[column_name] = getattr(entry, column_name, None)
        embed = discord_helper.generate_embed(title=table_name, **kwargs)
        embeds.append(embed)
    return embeds


def sql_type_to_human_type_string(sql_type) -> str:
    if not hasattr(sql_type, "python_type"):
        return ""

    python_type = sql_type.python_type
    if python_type == str:
        return "String"
    elif python_type in [int, float]:
        return "Number"
    elif python_type == bool:
        return "True/False"
    return ""


def human_type_to_python_type(human_type: str):
    try:
        return float(human_type)  # is it a float?
    except:
        try:
            return int(human_type)  # is it an int?
        except:
            bool_value = utils.convert_to_bool(bool_string=human_type)
            if bool_value is not None:  # is is a boolean?
                return bool_value
            else:
                return human_type  # it's a string
