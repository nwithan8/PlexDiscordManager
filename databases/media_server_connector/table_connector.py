from typing import Union

from databases.media_server_connector.database import PlatformType
from databases.media_server_connector.tables.config import *
from databases.media_server_connector.tables.media_server_settings import *


class ConfigType(Enum):
    Discord = 1,
    Exemptions = 2,
    Trial = 3,
    Winner = 4,
    Subscriber = 5,
    Roles = 6,
    General = 7,
    Plex = 8,
    Tautulli = 9,
    Ombi = 10,
    Emby = 11,
    Jellyfin = 12


def config_type_to_platform_type(config_type: ConfigType) -> PlatformType:
    """
    Default to Plex as the platform for database, unless we need to specifically access Emby or Jellyfin things
    """
    if config_type in [ConfigType.Emby]:
        return PlatformType.Emby
    if config_type in [ConfigType.Jellyfin]:
        return PlatformType.Jellyfin
    return PlatformType.Plex


def _get_table_by_name(table_name: str) -> Table:
    for table in Base.metadata.sorted_tables:
        if getattr(table, "name", None) == table_name:
            return table
    return None


def table_schema_to_table(table_schema) -> Table:
    table_name = table_schema_to_table_name(table_schema=table_schema)
    return _get_table_by_name(table_name=table_name)


def table_schema_to_table_name(table_schema) -> str:
    if table_schema == DiscordConfiguration:
        return "discordConfig"
    elif table_schema == ExemptUsers:
        return "exemptUsers"
    elif table_schema == TrialConfiguration:
        return "trialConfig"
    elif table_schema == WinnerConfiguration:
        return "winnerConfig"
    elif table_schema == SubscriberConfiguration:
        return "subscriberConfig"
    elif table_schema == SubscriberRoles:
        return "userRoles"
    elif table_schema == MediaServerConfiguration:
        return "mediaServerConfig"
    elif table_schema == PlexSettings:
        return "plexSettings"
    elif table_schema == OmbiSettings:
        return "ombiSettings"
    elif table_schema == TautulliSettings:
        return "tautulliSettings"
    return ""


def get_table(table_schema: DeclarativeMeta) -> Table:
    return table_schema_to_table(table_schema=table_schema)


def get_table_name(table_schema: DeclarativeMeta) -> str:
    return table_schema_to_table_name(table_schema=table_schema)


def table_schema_to_config_type(table_schema):
    if table_schema == DiscordConfiguration:
        return ConfigType.Discord
    if table_schema == ExemptUsers:
        return ConfigType.Exemptions
    if table_schema == TrialConfiguration:
        return ConfigType.Trial
    if table_schema == WinnerConfiguration:
        return ConfigType.Winner
    if table_schema == SubscriberConfiguration:
        return ConfigType.Subscriber
    if table_schema == SubscriberRoles:
        return ConfigType.Roles
    if table_schema == MediaServerConfiguration:
        return ConfigType.General
    if table_schema == PlexSettings:
        return ConfigType.Plex
    if table_schema == TautulliSettings:
        return ConfigType.Tautulli
    if table_schema == OmbiSettings:
        return ConfigType.Ombi
    return None


def config_type_to_table_schema(config_type: ConfigType):
    if config_type == ConfigType.Discord:
        return DiscordConfiguration
    if config_type == ConfigType.Exemptions:
        return ExemptUsers
    if config_type == ConfigType.Trial:
        return TrialConfiguration
    if config_type == ConfigType.Winner:
        return WinnerConfiguration
    if config_type == ConfigType.Subscriber:
        return SubscriberConfiguration
    if config_type == ConfigType.Roles:
        return SubscriberRoles
    if config_type == ConfigType.General:
        return MediaServerConfiguration
    if config_type == ConfigType.Plex:
        return PlexSettings
    if config_type == ConfigType.Ombi:
        return OmbiSettings
    if config_type == ConfigType.Tautulli:
        return TautulliSettings
    return None


def config_type_to_string(config_type: ConfigType) -> str:
    if config_type == ConfigType.Discord:
        return "discord"
    if config_type == ConfigType.Exemptions:
        return "exemptions"
    if config_type == ConfigType.Trial:
        return "trials"
    if config_type == ConfigType.Winner:
        return "winners"
    if config_type == ConfigType.Subscriber:
        return "subscribers"
    if config_type == ConfigType.Roles:
        return "roles"
    if config_type == ConfigType.General:
        return "general"
    if config_type == ConfigType.Plex:
        return "plex"
    if config_type == ConfigType.Ombi:
        return "ombi"
    if config_type == ConfigType.Tautulli:
        return "tautulli"
    return ""


def string_to_config_type(config_type_string: str) -> Union[ConfigType, None]:
    if config_type_string == "discord":
        return ConfigType.Discord
    if config_type_string == "exemptions":
        return ConfigType.Exemptions
    if config_type_string == "trials":
        return ConfigType.Trial
    if config_type_string == "winners":
        return ConfigType.Winner
    if config_type_string == "subscribers":
        return ConfigType.Subscriber
    if config_type_string == "roles":
        return ConfigType.Roles
    if config_type_string == "general":
        return ConfigType.General
    if config_type_string == "plex":
        return ConfigType.Plex
    if config_type_string == "ombi":
        return ConfigType.Ombi
    if config_type_string == "tautulli":
        return ConfigType.Tautulli
    return None


def string_to_table_schema(config_type_string: str) -> Union[Table, None]:
    config_type = string_to_config_type(config_type_string)
    return config_type_to_table_schema(config_type)
