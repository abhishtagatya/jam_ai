from datetime import datetime
from typing import Dict, AnyStr


class BasePersistence(object):

    def __init__(self):
        pass

    @staticmethod
    def transform(data: Dict) -> Dict:
        return {}

    def save(self, role: str, author: str, content: str):
        pass

    def find(self, key: str, value: str = None, limit: int = 5):
        return []

    def all(self):
        return []


class PersistenceObject:

    def __init__(self,
                 uid: AnyStr,
                 author: str,
                 role: str,
                 content: AnyStr,
                 mention: AnyStr,
                 function: AnyStr,
                 timestamp: datetime = None,
                 success: bool = True):
        self.uid = uid
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
        return f'<PersistenceObject (author={self.author}, content={self.content})'
