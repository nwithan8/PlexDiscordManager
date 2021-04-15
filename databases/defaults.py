from sqlalchemy import Column, Integer, String, Boolean, BigInteger, null
from enum import Enum

class ColumnType(Enum):
    DiscordRoleName = String(100)
    DiscordUserID = BigInteger
    DiscordServerID = BigInteger
    DiscordUserName = BigInteger
    URL = String(1400)


DiscordRoleName = String(100)
DiscordUserID = BigInteger
DiscordServerID = BigInteger
DiscordUserName = String(100)