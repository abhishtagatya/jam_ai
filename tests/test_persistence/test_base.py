import unittest
from datetime import datetime
from typing import AnyStr, List

from jam.persistence.base import BasePersistence
from jam.persistence.base import PersistenceObject

from jam.util.generate import generate_id


class TestPersistenceObject(unittest.TestCase):

    def setUp(self) -> None:
        self.uid_1 = generate_id(16)
        self.author_1 = generate_id(8)
        self.role_1 = generate_id(8)
        self.content_1 = generate_id(8)
        self.mention_1 = self.author_1
        self.function_1 = generate_id(8)
        self.timestamp_1 = datetime.now()
        self.success_1 = True

        self.uid_2 = generate_id(16)
        self.author_2 = generate_id(8)
        self.role_2 = generate_id(8)
        self.content_2 = generate_id(8)
        self.mention_2 = self.author_2
        self.function_2 = generate_id(8)
        self.timestamp_2 = datetime.now()
        self.success_2 = False

        self.po_1 = PersistenceObject(
            uid=self.uid_1,
            author=self.author_1,
            role=self.role_1,
            content=self.content_1,
            mention=self.mention_1,
            function=self.function_1,
            timestamp=self.timestamp_1,
            success=self.success_1
        )

        self.po_2 = PersistenceObject(
            uid=self.uid_2,
            author=self.author_2,
            role=self.role_2,
            content=self.content_2,
            mention=self.mention_2,
            function=self.function_2,
            timestamp=self.timestamp_2,
            success=self.success_2
        )

    def test_class_identity(self):
        self.assertIsInstance(self.po_1, PersistenceObject)
        self.assertIsInstance(self.po_2, PersistenceObject)

    def test_class_attribute_uid(self):
        self.assertEqual(self.po_1.uid, self.uid_1)
        self.assertEqual(self.po_2.uid, self.uid_2)

    def test_class_attribute_author(self):
        self.assertEqual(self.po_1.author, self.author_1)
        self.assertEqual(self.po_2.author, self.author_2)

    def test_class_attribute_role(self):
        self.assertEqual(self.po_1.role, self.role_1)
        self.assertEqual(self.po_2.role, self.role_2)

    def test_class_attribute_content(self):
        self.assertEqual(self.po_1.content, self.content_1)
        self.assertEqual(self.po_2.content, self.content_2)

    def test_class_attribute_mention(self):
        self.assertEqual(self.po_1.mention, self.mention_1)
        self.assertEqual(self.po_2.mention, self.mention_2)

    def test_class_attribute_function(self):
        self.assertEqual(self.po_1.function, self.function_1)
        self.assertEqual(self.po_2.function, self.function_2)

    def test_class_attribute_timestamp(self):
        self.assertEqual(self.po_1.timestamp, self.timestamp_1)
        self.assertEqual(self.po_2.timestamp, self.timestamp_2)

    def test_class_attribute_success(self):
        self.assertEqual(self.po_1.success, self.success_1)
        self.assertEqual(self.po_2.success, self.success_2)

    def test_class_method_as_message(self):
        self.po_1_m = self.po_1.as_message()
        self.po_2_m = self.po_2.as_message()

        self.assertIn('role', self.po_1_m.keys())
        self.assertIn('content', self.po_1_m.keys())
        self.assertIn('name', self.po_1_m.keys())

        self.assertEqual(self.po_1_m.get('role'), self.po_1.role)
        self.assertEqual(self.po_1_m.get('content'), self.po_1.content)
        self.assertEqual(self.po_1_m.get('name'), self.po_1.function)

        self.assertEqual(self.po_2_m.get('role'), self.po_2.role)
        self.assertEqual(self.po_2_m.get('content'), self.po_2.content)
        self.assertEqual(self.po_2_m.get('name'), self.po_2.function)


class AlterPersistence(BasePersistence):

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
            saved_objs.append(data_obj)
        return saved_objs


class TestBasePersistence(unittest.TestCase):

    def setUp(self) -> None:
        self.per_1 = BasePersistence()
        self.per_2 = AlterPersistence()

        self.role_2 = generate_id(8)
        self.author_2 = generate_id(8)
        self.content_2 = generate_id(8)
        self.mention_2 = [self.author_2]
        self.function_2 = generate_id(8)

        self.per_2_saved = self.per_2.save(
            role=self.role_2,
            author=self.author_2,
            content=self.content_2,
            mentions=self.mention_2,
            function=self.function_2
        )

        self.per_2_saved_mock = [
            PersistenceObject(
                uid=generate_id(16),
                role=self.role_2,
                author=self.author_2,
                content=self.content_2,
                mention=self.author_2,
                function=self.function_2,
                timestamp=datetime.now()
            )
        ]

    def test_class_identity(self):
        self.assertIsInstance(self.per_1, BasePersistence)
        self.assertIsInstance(self.per_2, AlterPersistence)

    def test_class_method_save(self):
        self.assertEqual(self.per_1.save(
            role='', author='', content=''
        ), [])

        self.assertEqual(len(self.per_2_saved), len(self.per_2_saved_mock))
        self.assertEqual(self.per_2_saved[0].role, self.per_2_saved_mock[0].role)
        self.assertEqual(self.per_2_saved[0].author, self.per_2_saved_mock[0].author)
        self.assertEqual(self.per_2_saved[0].content, self.per_2_saved_mock[0].content)
        self.assertEqual(self.per_2_saved[0].mention, self.per_2_saved_mock[0].mention)
        self.assertEqual(self.per_2_saved[0].function, self.per_2_saved_mock[0].function)
        self.assertEqual(self.per_2_saved[0].success, self.per_2_saved_mock[0].success)
