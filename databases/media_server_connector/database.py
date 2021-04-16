import time

import databases.database_class as db

from databases.media_server_connector.tables.blacklist import *
from databases.media_server_connector.tables.users import *
from databases.media_server_connector.tables.config import *
from databases.media_server_connector.tables.media_server_settings import *
from databases.database_class import false_if_error


class DiscordMediaServerConnectorDatabase(db.SQLAlchemyDatabase):
    def __init__(self,
                 sqlite_file: str,
                 encrypted: bool = False,
                 key_file: str = None,
                 media_server_type: str = Union['plex', 'jellyfin', 'emby'],
                 trial_length: int = 0,
                 multi_plex: bool = False):
        self.platform = media_server_type
        self.trial_length = trial_length
        self.multi_plex = multi_plex
        super().__init__(sqlite_file=sqlite_file, encrypted=encrypted, key_file=key_file)
        PlexUser.__table__.create(bind=self.engine, checkfirst=True)
        JellyfinUser.__table__.create(bind=self.engine, checkfirst=True)
        EmbyUser.__table__.create(bind=self.engine, checkfirst=True)
        MediaServerConfiguration.__table__.create(bind=self.engine, checkfirst=True)
        SubscriberConfiguration.__table__.create(bind=self.engine, checkfirst=True)
        SubscriberRoles.__table__.create(bind=self.engine, checkfirst=True)
        WinnerConfiguration.__table__.create(bind=self.engine, checkfirst=True)
        TrialConfiguration.__table__.create(bind=self.engine, checkfirst=True)
        ExemptUsers.__table__.create(bind=self.engine, checkfirst=True)
        DiscordConfiguration.__table__.create(bind=self.engine, checkfirst=True)
        BlacklistEntry.__table__.create(bind=self.engine, checkfirst=True)
        PlexSettings.__table__.create(bind=self.engine, checkfirst=True)
        TautulliSettings.__table__.create(bind=self.engine, checkfirst=True)
        OmbiSettings.__table__.create(bind=self.engine, checkfirst=True)

    # Media Server Users

    @property
    def _user_table(self):
        if self.platform == "plex":
            return PlexUser
        elif self.platform == "emby":
            return EmbyUser
        elif self.platform == "jellyfin":
            return JellyfinUser
        return None

    def make_user(self, **kwargs):
        if self.platform == "plex":
            return PlexUser(**kwargs)
        elif self.platform == "emby":
            return EmbyUser(**kwargs)
        elif self.platform == "jellyfin":
            return JellyfinUser(**kwargs)

    @property
    def users(self) -> List[Union[PlexUser, JellyfinUser, EmbyUser]]:
        if not self._user_table:
            return []
        return self.session.query(self._user_table).all()

    def get_user(self, discord_id=None, media_server_username=None, media_server_id=None,
                 first_match_only: bool = False) -> List[Union[PlexUser, JellyfinUser, EmbyUser]]:
        users = []
        for user in self.users:
            if (discord_id and user.DiscordID == discord_id) or (
                    media_server_username and user.MediaServerUsername == media_server_username) or (
                    media_server_id and user.MediaServerID == media_server_id):
                users.append(user)
        if first_match_only:
            return [users[0]] if users else []
        return users

    def add_user_to_database(self, user: Union[PlexUser, EmbyUser, JellyfinUser]) -> bool:
        self.session.add(user)
        self.commit()
        return True

    def remove_user_from_database(self, user: Union[PlexUser, EmbyUser, JellyfinUser]):
        if not self._user_table:
            return False
        self.session.query(self._user_table).filter(self._user_table.DiscordID == user.DiscordID).delete()
        self.commit()
        return True

    def edit_user(self, user: Union[PlexUser, EmbyUser, JellyfinUser], **kwargs):
        user_attribute_names = dir(user)
        for k, v in kwargs.items():
            if k in user_attribute_names:
                setattr(__obj=user, __name=k, __value=v)
        self.commit()

    @property
    def winners(self) -> List[Union[PlexUser, EmbyUser, JellyfinUser]]:
        if not self._user_table:
            return []
        return self.session.query(self._user_table).filter(self._user_table.SubType == 'Winner').all()

    @property
    def trials(self) -> List[Union[PlexUser, EmbyUser, JellyfinUser]]:
        if not self._user_table:
            return []
        return self.session.query(self._user_table).filter(self._user_table.SubType == 'Trial').all()

    @property
    def expired_trials(self) -> List[Union[PlexUser, EmbyUser, JellyfinUser]]:
        if not self._user_table:
            return []
        return self.session.query(self._user_table).filter(self._user_table.SubType == 'Trial').filter(
            self._user_table.ExpirationStamp <= int(time.time())).all()

    def on_blacklist(self, names_and_ids: List) -> bool:
        for elem in names_and_ids:
            results = self.session.query(BlacklistEntry).filter(BlacklistEntry.IDorUsername == elem).all()
            if results:
                return True
        return False

    def add_to_blacklist(self, name_or_id: Union[str, int]) -> bool:
        if isinstance(name_or_id, int):
            name_or_id = str(name_or_id)
        new_entry = BlacklistEntry(id_or_username=name_or_id)
        self.session.add(new_entry)
        self.commit()
        return True

    def remove_from_blacklist(self, name_or_id: Union[str, int]) -> bool:
        if isinstance(name_or_id, int):
            name_or_id = str(name_or_id)
        self.session.query(BlacklistEntry).filter(BlacklistEntry.IDorUsername == name_or_id).delete()
        self.commit()
        return True

    @property
    def blacklist(self) -> List[BlacklistEntry]:
        return self.session.query(BlacklistEntry).all()

    # Configuration
    @property
    def _discord_config(self):
        return self.get_first_entry(table_schema=DiscordConfiguration)

    @property
    def _winner_config(self):
        return self.get_first_entry(table_schema=WinnerConfiguration)

    @property
    def _trial_config(self):
        return self.get_first_entry(table_schema=TrialConfiguration)

    @property
    def _subscriber_config(self):
        return self.get_first_entry(table_schema=SubscriberConfiguration)

    @property
    def _media_config(self):
        return self.get_first_entry(table_schema=MediaServerConfiguration)

    @property
    def _subscriber_roles(self):
        return self.get_all_entries(table_schema=SubscriberRoles)

    @property
    def _exempt_users(self):
        return self.get_all_entries(table_schema=ExemptUsers)

    @property
    def bot_prefix(self):
        return self.get_attribute_from_first_entry(table_schema=DiscordConfiguration, field_name="BotPrefix")

    def set_bot_prefix(self, prefix: str) -> bool:
        return self.set_attribute_of_first_entry(table_schema=DiscordConfiguration, field_name="BotPrefix",
                                                 field_value=prefix)

    @property
    def admin_id(self):
        if not self._discord_config:
            return None
        return self._discord_config.AdminID

    def set_admin_id(self, admin_id: str) -> bool:
        return self.set_attribute_of_first_entry(table_schema=DiscordConfiguration, field_name="AdminID",
                                                 field_value=admin_id)

    @property
    def admin_role_name(self):
        if not self._discord_config:
            return None
        return self._discord_config.AdminRoleName

    def set_admin_role_name(self, admin_role_name: str) -> bool:
        return self.set_attribute_of_first_entry(table_schema=DiscordConfiguration,
                                                 field_name="AdminRoleName",
                                                 field_value=admin_role_name)

    # don't need decorator. The create_first_entry one already has it
    def set_media_server_configuration(self, **kwargs) -> bool:
        return self.create_first_entry(table_schema=MediaServerConfiguration, **kwargs)

    @property
    def trial_role_name(self):
        if not self._trial_config:
            return None
        return self._trial_config.RoleName

    # don't need decorator. The create_first_entry one already has it
    def set_trial_configuration(self, **kwargs) -> bool:
        return self.create_first_entry(table_schema=TrialConfiguration, **kwargs)

    @property
    def winner_role_name(self):
        if not self._winner_config:
            return None
        return self._winner_config.RoleName

    # don't need decorator. The create_first_entry one already has it
    def set_winner_configuration(self, **kwargs) -> bool:
        return self.create_first_entry(table_schema=WinnerConfiguration, **kwargs)

    # don't need decorator. The create_first_entry one already has it
    def set_subscriber_configuration(self, **kwargs) -> bool:
        return self.create_first_entry(table_schema=SubscriberConfiguration, **kwargs)

    @property
    def subscriber_role_names(self):
        return [entry.RoleName for entry in self._subscriber_roles]

    def add_subscriber_role(self, role_name: str) -> bool:
        return self.create_entry(table_schema=SubscriberRoles, RoleName=role_name)

    @false_if_error
    def remove_subscriber_role(self, role_name: str) -> bool:
        self.session.delete(SubscriberRoles).where(SubscriberRoles.RoleName == role_name)
        return True

    # don't need decorator. The create_entry one already has it
    def add_exempt_user(self, user_id: int) -> bool:
        return self.create_entry(table_schema=SubscriberRoles, UserID=user_id)

    @false_if_error
    def remove_exempt_user(self, user_id: int) -> bool:
        self.session.delete(ExemptUsers).where(ExemptUsers.UserID == user_id)
        return True

    # don't need decorator. The update_entry one already has it
    def update_config(self, table, setting_name, setting_value) -> bool:
        entry = self.get_first_entry(table_schema=table)
        return self.update_entry_single_field(entry=entry, field_name=setting_name, field_value=setting_value)

    def create_initial_config(self, table, **kwargs) -> bool:
        return self.replace_first_entry(table_schema=table, **kwargs)

    # Media Server Settings
    @property
    def _plex_settings(self):
        return self.get_first_entry(table_schema=PlexSettings)

    # don't need decorator. The create_first_entry one already has it
    def set_plex_settings(self, **kwargs) -> bool:
        return self.create_first_entry(table_schema=PlexSettings, **kwargs)

    # don't need decorator. The update_first_entry one already has it
    def edit_plex_setting(self, field_name, field_value) -> bool:
        return self.update_first_entry(table_schema=PlexSettings, field_name=field_name, field_value=field_value)

    @property
    def _tautulli_settings(self):
        return self.get_first_entry(table_schema=TautulliSettings)

    # don't need decorator. The create_first_entry one already has it
    def set_tautulli_settings(self, **kwargs) -> bool:
        return self.create_first_entry(table_schema=TautulliSettings, **kwargs)

    # don't need decorator. The update_first_entry one already has it
    def edit_tautulli_setting(self, field_name, field_value) -> bool:
        return self.update_first_entry(table_schema=TautulliSettings, field_name=field_name, field_value=field_value)

    @property
    def _ombi_settings(self):
        return self.get_first_entry(table_schema=OmbiSettings)

    # don't need decorator. The create_first_entry one already has it
    def set_ombi_settings(self, **kwargs) -> bool:
        return self.create_first_entry(table_schema=OmbiSettings, **kwargs)

    # don't need decorator. The update_first_entry one already has it
    def edit_ombi_setting(self, field_name, field_value) -> bool:
        return self.update_first_entry(table_schema=OmbiSettings, field_name=field_name, field_value=field_value)
