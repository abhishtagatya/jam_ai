import unittest

from typing import AnyStr

from jam.interface.base import JIOutput
from jam.interface.base import BaseInterface


class TestJIOutput(unittest.TestCase):

    def setUp(self) -> None:
        self.ji_1 = JIOutput()
        self.ji_2 = JIOutput(out_type=JIOutput.JIO_FILE, output='any.file', function='file_maker')
        self.ji_3 = JIOutput(success=False)

    def test_class_identity(self):
        self.assertIsInstance(self.ji_1, JIOutput)
        self.assertIsInstance(self.ji_2, JIOutput)
        self.assertIsInstance(self.ji_3, JIOutput)

    def test_class_attribute_out_type(self):
        self.assertEqual(self.ji_1.out_type, JIOutput.JIO_TEXT)
        self.assertEqual(self.ji_2.out_type, JIOutput.JIO_FILE)
        self.assertEqual(self.ji_3.out_type, JIOutput.JIO_TEXT)

    def test_class_attribute_output(self):
        self.assertEqual(self.ji_1.output, '')
        self.assertEqual(self.ji_2.output, 'any.file')
        self.assertEqual(self.ji_3.output, '')

    def test_class_attribute_function(self):
        self.assertEqual(self.ji_1.function, None)
        self.assertEqual(self.ji_2.function, 'file_maker')
        self.assertEqual(self.ji_3.function, None)

    def test_class_attribute_success(self):
        self.assertEqual(self.ji_1.success, True)
        self.assertEqual(self.ji_2.success, True)
        self.assertEqual(self.ji_3.success, False)

    def tearDown(self) -> None:
        pass


class BaseInterfaceAlter(BaseInterface):

    def call(self, x: AnyStr = None) -> JIOutput:
        return JIOutput(output=x, success=False)


class TestBaseInterface(unittest.TestCase):

    def setUp(self) -> None:
        self.bi_1 = BaseInterface()
        self.bi_2 = BaseInterface()

    def test_class_identity(self):
        self.assertIsInstance(self.bi_1, BaseInterface)
        self.assertIsInstance(self.bi_2, BaseInterface)

    def test_class_method_call(self):
        self.assertIsInstance(self.bi_1.call(), JIOutput)
        self.assertIsInstance(self.bi_2.call(), JIOutput)

        bi_1_call = self.bi_1.call()
        self.assertEqual(bi_1_call.out_type, JIOutput.JIO_TEXT)
        self.assertEqual(bi_1_call.output, '')
        self.assertEqual(bi_1_call.function, None)
        self.assertEqual(bi_1_call.success, True)

        bi_2_call = self.bi_2.call()
        self.assertEqual(bi_2_call.out_type, JIOutput.JIO_TEXT)
        self.assertEqual(bi_2_call.output, '')
        self.assertEqual(bi_2_call.function, None)
        self.assertEqual(bi_2_call.success, True)


