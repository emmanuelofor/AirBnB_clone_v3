#!/usr/bin/python3
'''
    This script defines the DatabaseStorage class.
'''
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.state import State
from models.city import City
from models.base_model import Base


class DBStorage:
    '''
        A class to interact with the SQLalchemy database.
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
            Constructs a DBStorage instance, creating a connection to the MySQL database.
        '''
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        envv = getenv("HBNB_ENV", "none")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        if envv == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
            Queries the current database session.
        '''
        db_dict = {}
        if cls != "":
            objs = self.__session.query(models.classes[cls]).all()
            for obj in objs:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                db_dict[key] = obj
            return db_dict
        else:
            for k, v in models.classes.items():
                if k != "BaseModel":
                    objs = self.__session.query(v).all()
                    if len(objs) > 0:
                        for obj in objs:
                            key = "{}.{}".format(obj.__class__.__name__,
                                                 obj.id)
                            db_dict[key] = obj
            return db_dict

    def new(self, obj):
        '''
            Adds an object to the current database session.
        '''
        self.__session.add(obj)

    def save(self):
        '''
            Commits all changes made in the current database session.
        '''
        self.__session.commit()

    def delete(self, obj=None):
        '''
            Deletes an object from the current database session.
        '''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        '''
            Reloads all objects from the current database session.
        '''
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        '''
            Closes the current database session.
        '''
        self.__session.close()

    def get(self, cls, id):
        '''
            Retrieves an object using its class name and id.
        '''
        result = None
        try:
            objs = self.__session.query(models.classes[cls]).all()
            for obj in objs:
                if obj.id == id:
                    result = obj
        except BaseException:
            pass
        return result

    def count(self, cls=None):
        '''
            Counts the number of objects in DBstorage.
        '''
        cls_counter = 0

        if cls is not None:
            objs = self.__session.query(models.classes[cls]).all()
            cls_counter = len(objs)
        else:
            for k, v in models.classes.items():
                if k != "BaseModel":
                    objs = self.__session.query(models.classes[k]).all()
                    cls_counter += len(objs)
        return cls_counter
