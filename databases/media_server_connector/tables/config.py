from sqlalchemy import Column, Integer, String, Boolean

from databases.tools import Base, get_column, ColumnType
from databases.database_class import none_as_null, map_attributes


class DiscordConfiguration(Base):
    __tablename__ = "discordConfig"
    ID = Column(Integer, autoincrement=True, primary_key=True)
    BotPrefix = Column(String(5), nullable=True)
    AdminID = get_column(ColumnType.DiscordUserID, unique=True, nullable=True)
    AdminRoleName = get_column(ColumnType.DiscordRoleName, unique=True, nullable=True)

    @none_as_null
    @map_attributes
    def __init__(self,
                 **kwargs):
        pass


class ExemptUsers(Base):
    __tablename__ = "exemptUsers"
    UserID = get_column(ColumnType.DiscordUserID, primary_key=True, unique=True)

    @none_as_null
    @map_attributes
    def __init__(self,
                 **kwargs):
        pass


class TrialConfiguration(Base):
    __tablename__ = "trialConfig"
    RoleName = get_column(ColumnType.DiscordRoleName, primary_key=True, unique=True)
    AutomaticallyCheck = Column(Boolean)
    LengthSeconds = Column(Integer)
    CheckFrequencySeconds = Column(Integer)

    @none_as_null
    @map_attributes
    def __init__(self,
                 **kwargs):
        pass


class WinnerConfiguration(Base):
    __tablename__ = "winnerConfig"
    AutomaticallyCheck = Column(Boolean)
    RoleName = get_column(ColumnType.DiscordRoleName, primary_key=True, unique=True)
    CheckFrequencySeconds = Column(Integer)
    MinutesRequiredPerWeek = Column(Integer)

    @none_as_null
    @map_attributes
    def __init__(self,
                 **kwargs):
        pass


class SubscriberRoles(Base):
    __tablename__ = "userRoles"
    RoleName = get_column(ColumnType.DiscordRoleName, primary_key=True, unique=True)

    @none_as_null
    @map_attributes
    def __init__(self,
                 **kwargs):
        pass


class SubscriberConfiguration(Base):
    __tablename__ = "subscriberConfig"
    AutomaticallyCheck = Column(Boolean)
    InvitedRoleName = get_column(ColumnType.DiscordRoleName, primary_key=True, unique=True)

    @none_as_null
    @map_attributes
    def __init__(self,
                 **kwargs):
        pass


class MediaServerConfiguration(Base):
    __tablename__ = "mediaServerConfig"
    ID = Column(Integer, autoincrement=True, primary_key=True)
    SubscriberWatchlistTitleTemplate = Column(String(200))
    SubscriberPlaylistTitleTemplate = Column(String(200))
    EnableBlacklist = Column(Boolean)
    CurrentlyPlayingRoleName = get_column(ColumnType.DiscordRoleName, unique=True, nullable=True)

    @none_as_null
    @map_attributes
    def __init__(self,
                 **kwargs):
        pass
