from databases.media_server_connector.database import PlatformType
from databases.media_server_connector.table_connector import table_schema_to_config_type, config_type_to_platform_type, \
    table_schema_to_table_name, ConfigType, config_type_to_table_schema
from modules.load_config import get_database


def _pull_settings(platform_type, table_schema, get_all: bool = False):
    database = get_database(media_server_type=platform_type)
    if get_all:
        return database.get_all_entries(table_schema=table_schema)
    return database.get_first_entry(table_schema=table_schema)


def _need_all(config_type):
    return config_type in [ConfigType.Roles]


class SettingsManager:
    def __init__(self):
        self._settings = {}
        self._load_settings()

    def _load_settings(self):
        for config_type in ConfigType:
            self.refresh_settings(config_type=config_type)

    def refresh_settings(self, config_type):
        platform_type = config_type_to_platform_type(config_type=config_type)
        table_schema = config_type_to_table_schema(config_type=config_type)
        table_name = table_schema_to_table_name(table_schema=table_schema)

        get_all = _need_all(config_type=config_type)
        new_settings = _pull_settings(platform_type=platform_type, table_schema=table_schema, get_all=get_all)
        self._settings[table_name] = new_settings

    def get_settings(self, config_type):
        table_schema = config_type_to_table_schema(config_type=config_type)
        table_name = table_schema_to_table_name(table_schema=table_schema)
        return self._settings.get(table_name, None)

    @property
    def all_settings(self):
        if not self._settings:
            self._load_settings()
        return self._settings

    @property
    def plex_settings(self):
        return self.get_settings(config_type=ConfigType.Plex)

    @property
    def ombi_settings(self):
        return self.get_settings(config_type=ConfigType.Ombi)

    @property
    def tautulli_settings(self):
        return self.get_settings(config_type=ConfigType.Tautulli)
