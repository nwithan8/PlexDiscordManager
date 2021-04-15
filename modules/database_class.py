from functools import wraps

from sqlalchemy import create_engine, MetaData, null
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import modules.encryption as encryption

def none_as_null(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """
        Replace None as null()
        """
        func(self, *args, **kwargs)
        for k, v in self.__dict__.items():
            if v is None:
                setattr(self, k, null())
    return wrapper

def map_attributes(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """
        Map kwargs to class attributes
        """
        func(self, *args, **kwargs)
        for k, v in kwargs.items():
            if getattr(self, k):
                setattr(self, k, v)
    return wrapper

class SQLAlchemyDatabase:
    def __init__(self,
                 sqlite_file: str,
                 encrypted: bool = False,
                 key_file: str = None,
                 use_dropbox: bool = False):
        self.sqlite_file = sqlite_file
        self.use_dropbox = use_dropbox
        self.encrypted = encrypted
        self.key_file = key_file
        if self.encrypted and not self.key_file:
            raise Exception("Missing KEY_FILE to unlock encrypted database_handler.")

        self.engine = None
        self.base = None
        self.meta = None
        self.session = None

        if self.encrypted and self.key_file:
            key = encryption.get_raw_key(self.key_file)
            self.url = f'sqlite+pysqlcipher://:{key}@/{sqlite_file}?cipher=aes-256-cfb&kdf_iter=64000'
        else:
            self.url = f'sqlite:///{sqlite_file}'

        self.setup()

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()

    def setup(self):
        if not self.url:
            return

        self.engine = create_engine(self.url)

        if not self.engine:
            return

        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        self.base = declarative_base(bind=self.engine)
        self.meta = MetaData()
        self.meta.create_all(self.engine)

        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()


    def get_attribute_from_first_entry(self, table_type, field_name):
        entry = self.session.query(table_type).first()
        return getattr(entry, field_name, None)

    def get_attribute_from_last_entry(self, table_type, field_name):
        entry = self.session.query(table_type).last()
        return getattr(entry, field_name, None)

    def set_attribute(self, table_type, field_name, field_value) -> bool:
        entry = self.session.query(table_type).first()
        if not entry:
            return self.create_first_entry(table_type=table_type, **{field_name: field_value})
        else:
            setattr(entry, field_name, field_value)
            self.commit()
            return True

    def create_first_entry(self, table_type, **kwargs) -> bool:
        entry = self.session.query(table_type).first()
        if not entry:
            entry = table_type(**kwargs)
            self.session.add(entry)
            self.commit()
        return True