from datetime import datetime
from typing import List, Optional

from jam.persistence.base import BasePersistence
from jam.persistence.base import PersistenceObject
from jam.util.generate import generate_id


class Node:

    def __init__(self, data: PersistenceObject):
        self.data = data
        self.prev = None
        self.next = None


class DoubleLinkedList:

    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.length = 0

    def append(self, data: PersistenceObject):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            new_node.prev = current
            self.tail = new_node
        self.length += 1

    def find(self, key: str, value: List[str], limit: int = 5):
        result = []
        current = self.tail
        if current is None:
            return result

        while current is not None and len(result) < limit:
            if current.data.__dict__[key] in value and current.data.mention in value:
                result.insert(0, current.data)
            current = current.prev
        return result

    def all(self):
        result = []
        current = self.tail
        while current is not None:
            result.append(current.data)
            current = current.prev
        return result


class MemoryPersistence(BasePersistence):

    def __init__(self):
        super(MemoryPersistence, self).__init__()
        self.db: DoubleLinkedList = DoubleLinkedList()

    def save(self,
             role: str,
             author: str,
             content: str,
             mentions: List[str] = None,
             function: str = None,
             success: bool = True):
        saved_objs = []
        if mentions is None:
            mentions = ['user']

        for mention in mentions:
            data_obj = PersistenceObject(
                uid=generate_id(16),
                role=role,
                author=author,
                content=content,
                mention=mention,
                function=function,
                timestamp=datetime.now(),
                success=success
            )
            self.db.append(data_obj)
            saved_objs.append(data_obj)
        return saved_objs

    def find(self, key: str, value: List[str] = None, limit: int = 5):
        result = self.db.find(key, value, limit)
        return result

    def all(self):
        result = self.db.all()
        return result

    def count(self):
        return self.db.length
