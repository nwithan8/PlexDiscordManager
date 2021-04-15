from typing import Union, List

from sqlalchemy.orm import declarative_base
import modules.database_class as db
from databases.defaults import *

from modules.database_class import none_as_null, map_attributes

Base = declarative_base()

def getColumn(column_type: ColumnType, **kwargs):
    sql_type = None
    if column_type == ColumnType.DiscordRoleName:
        sql_type = DiscordRoleName
    elif column_type == ColumnType.DiscordUserID:
        sql_type = DiscordUserID
    elif column_type == ColumnType.DiscordServerID:
        sql_type = DiscordServerID
    elif column_type == ColumnType.DiscordUserName:
        sql_type = DiscordUserName
    return Column(sql_type, **kwargs)
