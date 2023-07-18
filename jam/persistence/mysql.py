from typing import List, Dict

from jam.persistence.base import BasePersistence
from jam.persistence.base import PersistenceObject
from jam.persistence.model import Base
from jam.persistence.model import ConversationHistory
from jam.util.generate import generate_id

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session


class MySQLPersistence(BasePersistence):

    def __init__(self, dbname: str = 'mysql+pymysql://root:password@localhost/mysql'):
        super(MySQLPersistence, self).__init__()
        self._dbname = dbname
        self.db = create_engine(self._dbname)
        self._metadata = MetaData()

        self.seed()

    def seed(self):
        if not self.db.dialect.has_table(self.db.connect(), 'conversation_history'):
            Base.metadata.create_all(self.db)

    def save(self,
             cid: str,
             role: str,
             author: str,
             content: str,
             mentions: List[str] = None,
             function: str = None,
             success: bool = True):
        saved_objs = []
        if mentions is None:
            mentions = ['user']

        with Session(self.db) as session:
            for mention in mentions:
                conv_history = ConversationHistory(
                    uid=generate_id(16),
                    cid=cid,
                    role=role,
                    author=author,
                    content=content,
                    mention=mention,
                    function=function,
                    success=success
                )
                session.add(conv_history)
                saved_objs.append(conv_history)
            session.commit()

            return list(map(self.transform, saved_objs))

    def find(self, conditions: Dict, limit: int = 5):
        with Session(self.db) as session:
            filter_conditions = []
            for key, value in conditions.items():
                temp_conditions = [getattr(ConversationHistory, key) == val for val in value]
                temp_conditions = or_(*temp_conditions)
                filter_conditions.append(temp_conditions)
            filter_conditions = and_(*filter_conditions)

            result = session.query(
                ConversationHistory
            ).filter(filter_conditions).order_by(ConversationHistory.timestamp.desc()).limit(limit).all()

            return list(map(self.transform, result[::-1]))

    def all(self):
        with Session(self.db) as session:
            result = session.query(ConversationHistory).all()
            return list(map(self.transform, result))

    def count(self):
        with Session(self.db) as session:
            result = session.query(ConversationHistory).count()
            return result

    def clear(self, key: str = None, value: List[str] = None):
        with Session(self.db) as session:
            if key is None or value is None:
                session.query(ConversationHistory).delete()
                session.commit()
                return

            filter_conditions = [getattr(ConversationHistory, key) == val for val in value]
            filter_conditions = or_(*filter_conditions)

            session.query(ConversationHistory).filter(filter_conditions).delete()
            session.commit()
            return

