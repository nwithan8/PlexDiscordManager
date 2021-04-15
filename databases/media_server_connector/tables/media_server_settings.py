from databases.tools import *


class TautulliSettings(Base):
    __tablename__ = "tautulliSettings"
    PlexID = Column(Integer, primary_key=True)
    Enabled = Column(Boolean)
    URL = getColumn(ColumnType.URL, unique=True)
    ApiKey = Column(String(100))

    @none_as_null
    def __init__(self,
                 plex_id: int,
                 enabled: bool = False,
                 url: str = null(),
                 api_key: str = null()):
        self.PlexID = plex_id
        self.Enabled = enabled
        self.URL = url
        self.ApiKey = api_key


class OmbiSettings(Base):
    __tablename__ = "ombiSettings"
    PlexID = Column(Integer, primary_key=True)
    Enabled = Column(Boolean)
    URL = getColumn(ColumnType.URL, unique=True)
    ApiKey = Column(String(100))

    @none_as_null
    def __init__(self,
                 plex_id: int,
                 enabled: bool = False,
                 url: str = null(),
                 api_key: str = null()):
        self.PlexID = plex_id
        self.Enabled = enabled
        self.URL = url
        self.ApiKey = api_key


class PlexSettings(Base):
    __tablename__ = "plexSettings"
    ID = Column(Integer, autoincrement=True, primary_key=True)
    URL = getColumn(ColumnType.URL, unique=True)
    Token = Column(String(100))
    Name = Column(String(100))
    AltName = Column(String(100))
    TerminateMessage = Column(String(100))

    @none_as_null
    def __init__(self,
                 url: str,
                 token: str,
                 name: str,
                 alt_name: str = null(),
                 terminate_message: str = null()):
        self.URL = url
        self.Token = token
        self.Name = name
        self.AltName = alt_name
        self.TerminateMessage = terminate_message
