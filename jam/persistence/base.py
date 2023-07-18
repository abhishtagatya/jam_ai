from datetime import datetime
from typing import Dict, AnyStr, List

from jam.persistence.model import ConversationHistory


class PersistenceObject:

    def __init__(self,
                 uid: AnyStr,
                 cid: AnyStr,
                 author: str,
                 role: str,
                 content: AnyStr,
                 mention: AnyStr,
                 function: AnyStr,
                 timestamp: datetime = None,
                 success: bool = True):
        self.uid = uid
        self.cid = cid
        self.author = author
        self.role = role
        self.content = content
        self.mention = mention
        self.function = function
        self.timestamp = timestamp
        self.success = success

    def as_message(self):
        return {
            'role': self.role,
            'content': self.content,
            'name': self.function
        }

    def __repr__(self):
        return f'<PersistenceObject (cid={self.cid}, author={self.author}, content={self.content}, mention={self.mention})'


class BasePersistence(object):

    def __init__(self):
        pass

    @staticmethod
    def transform(data: ConversationHistory) -> PersistenceObject:
        data_obj = PersistenceObject(
            uid=data.uid,
            cid=data.cid,
            role=data.role,
            author=data.author,
            content=data.content,
            mention=data.mention,
            function=data.function,
            timestamp=data.timestamp,
            success=data.success
        )
        return data_obj

    def save(self,
             cid: str,
             role: str,
             author: str,
             content: str,
             mentions: List[str] = None,
             function: str = None,
             success: bool = True):
        return []

    def find(self, conditions: Dict, limit: int = 5):
        return []

    def all(self):
        return []

    def count(self):
        return 0

    def clear(self):
        return
