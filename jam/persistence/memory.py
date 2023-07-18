from datetime import datetime
from typing import List, Optional, Dict

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
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            current = self.tail
            current.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.length += 1

    def find(self, conditions: Dict, limit: int = 5):
        result = []
        current = self.tail
        if current is None:
            return result

        while current is not None and len(result) < limit:
            key_flag = 0
            for key, value in conditions.items():
                if current.data.__dict__[key] in value:
                    key_flag += 1
            if key_flag >= len(conditions):
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

    def clear(self, key: str = None, value: List[str] = None):
        if key is None or value is None:
            self.head = self.tail = None
            self.length = 0
        else:
            current = self.tail
            while current:
                if current.data.__dict__[key] in value:
                    if current.prev:
                        current.prev.next = current.next
                    else:
                        self.head = current.next

                    if current.next:
                        current.next.prev = current.prev
                    else:
                        self.tail = current.prev
                    self.length -= 1

                current = current.prev


class MemoryPersistence(BasePersistence):

    def __init__(self):
        super(MemoryPersistence, self).__init__()
        self.db: DoubleLinkedList = DoubleLinkedList()

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

        for mention in mentions:
            data_obj = PersistenceObject(
                uid=generate_id(16),
                cid=cid,
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

    def find(self, conditions: Dict, limit: int = 5):
        result = self.db.find(conditions, limit)
        return result

    def all(self):
        result = self.db.all()
        return result

    def count(self):
        return self.db.length

    def clear(self, key: str = None, value: List[str] = None):
        self.db.clear(key=key, value=value)
        return

