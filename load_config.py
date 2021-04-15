from databases.media_server_connector.base import DiscordMediaServerConnectorDatabase

def get_database(media_server_type: str = "plex", **kwargs):
    db_file_path = "databases/media_server_connector/database.db"
    return DiscordMediaServerConnectorDatabase(sqlite_file=db_file_path,
                                               encrypted=False,
                                               media_server_type=media_server_type,
                                               **kwargs)
    # media_server_type is just a formality here for queries involving the media server type. No effect on system config queries

def _read_token_from_file():
    file_path = ".token"
    with open(file_path, 'r') as f:
        return f.read()

def get_bot_token():
    database = get_database()
    token = database.bot_token
    if not token:
        token = _read_token_from_file()
        database.set_bot_token(token)
    return token

def get_bot_prefix():
    database = get_database()
    prefix = database.bot_prefix
    if not prefix:
        prefix = "*"
        database.set_bot_prefix(prefix)
    return prefix