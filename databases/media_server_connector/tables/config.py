from databases.defaults import *
from databases.tools import *


class DiscordConfiguration(Base):
    __tablename__ = "discordConfig"
    ID = Column(Integer, autoincrement=True, primary_key=True)
    BotToken = Column(String(200), unique=True, nullable=True)
    BotPrefix = Column(String(5), nullable=True)
    AdminID = getColumn(ColumnType.DiscordUserID, unique=True, nullable=True)
    AdminRoleName = getColumn(ColumnType.DiscordRoleName, unique=True, nullable=True)

    @none_as_null
    @map_attributes
    def __init__(self,
                 **kwargs):
        pass


class ExemptUsers(Base):
    __tablename__ = "exemptUsers"
    UserID = getColumn(ColumnType.DiscordUserID, primary_key=True, unique=True)

    @none_as_null
    @map_attributes
    def __init__(self,
                 **kwargs):
        pass


class TrialConfiguration(Base):
    __tablename__ = "trialConfig"
    RoleName = getColumn(ColumnType.DiscordRoleName, primary_key=True, unique=True)
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
    RoleName = getColumn(ColumnType.DiscordRoleName, primary_key=True, unique=True)
    CheckFrequencySeconds = Column(Integer)
    MinutesRequiredPerWeek = Column(Integer)

    @none_as_null
    @map_attributes
    def __init__(self,
                 **kwargs):
        pass


class SubscriberRoles(Base):
    __tablename__ = "userRoles"
    RoleName = getColumn(ColumnType.DiscordRoleName, primary_key=True, unique=True)

    @none_as_null
    @map_attributes
    def __init__(self,
                 **kwargs):
        pass


class SubscriberConfiguration(Base):
    __tablename__ = "subscriberConfig"
    AutomaticallyCheck = Column(Boolean)
    InvitedRoleName = getColumn(ColumnType.DiscordRoleName, primary_key=True, unique=True)

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
    CurrentlyPlayingRoleName = getColumn(ColumnType.DiscordRoleName, unique=True, nullable=True)

    @none_as_null
    @map_attributes
    def __init__(self,
                 **kwargs):
        pass
