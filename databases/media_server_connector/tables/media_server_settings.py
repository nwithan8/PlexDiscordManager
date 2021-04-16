from databases.tools import *
from databases.database_class import none_as_null, map_attributes


class TautulliSettings(Base):
    __tablename__ = "tautulliSettings"
    Enabled = Column(Boolean)
    URL = get_column(ColumnType.URL, primary_key=True, unique=True)
    ApiKey = Column(String(100))

    @none_as_null
    @map_attributes
    def __init__(self,
                 **kwargs):
        pass


class OmbiSettings(Base):
    __tablename__ = "ombiSettings"
    Enabled = Column(Boolean)
    URL = get_column(ColumnType.URL, primary_key=True, unique=True)
    ApiKey = Column(String(100))

    @none_as_null
    @map_attributes
    def __init__(self,
                 **kwargs):
        pass


class PlexSettings(Base):
    __tablename__ = "plexSettings"
    ID = Column(Integer, autoincrement=True, primary_key=True)
    URL = get_column(ColumnType.URL, unique=True)
    Token = Column(String(100))
    Name = Column(String(100))
    AltName = Column(String(100))
    TerminateMessage = Column(String(100))

    @none_as_null
    @map_attributes
    def __init__(self,
                 **kwargs):
        pass
