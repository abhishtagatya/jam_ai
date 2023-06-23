import unittest

from jam.instrument.base import BaseProperty
from jam.instrument.base import BaseParameter
from jam.instrument.base import BaseFunction
from jam.instrument.base import BaseInstrument

from jam.interface.base import BaseInterface


class TestBaseProperty(unittest.TestCase):

    def setUp(self) -> None:
        self.a_property = BaseProperty(name='A', obj_type='int', description='A', enum=['X', 'Y'])
        self.a_property_dict = {
            'A': {
                'type': 'int',
                'description': 'A',
                'enum': ['X', 'Y']
            }
        }
        self.a_property_dict_val = {
            'type': 'int',
            'description': 'A',
            'enum': ['X', 'Y']
        }

        self.b_property = BaseProperty(name='B', description='B')
        self.b_property_dict = {
            'B': {
                'type': 'string',
                'description': 'B'
            }
        }
        self.b_property_dict_val = {
            'type': 'string',
            'description': 'B'
        }

    def test_class_identity(self):
        self.assertIsInstance(self.a_property, BaseProperty)
        self.assertIsInstance(self.b_property, BaseProperty)

    def test_class_equality(self):
        self.assertEqual(self.a_property.as_dict(), self.a_property_dict)
        self.assertEqual(self.a_property.as_dict(value_only=True), self.a_property_dict_val)

        self.assertEqual(self.b_property.as_dict(), self.b_property_dict)
        self.assertEqual(self.b_property.as_dict(value_only=True), self.b_property_dict_val)

    def test_class_inequality(self):
        self.assertNotEqual(self.a_property, self.a_property_dict)
        self.assertNotEqual(self.b_property, self.b_property_dict)

    def tearDown(self) -> None:
        pass


class TestBaseParameter(unittest.TestCase):

    def setUp(self) -> None:
        self.a_property = BaseProperty(name='A', obj_type='int', description='A', enum=['X', 'Y'])
        self.b_property = {'B': {'type': 'string', 'description': 'B'}}

        self.a_parameter = BaseParameter(properties=[self.a_property, self.b_property])
        self.b_parameter = BaseParameter(properties=[self.a_property], required=[self.a_property])
        self.c_parameter = BaseParameter(properties=[self.a_property], required=['A'])
        self.d_parameter = BaseParameter(properties=[self.b_property], required=['B'])

        self.a_parameter_dict = {
            'type': 'object',
            'properties': {self.a_property.name: self.a_property.as_dict(value_only=True),
                           'B': {'type': 'string', 'description': 'B'}},
            'required': []
        }
        self.b_parameter_dict = {
            'type': 'object',
            'properties': self.a_property.as_dict(),
            'required': [self.a_property.name]
        }
        self.c_parameter_dict = {
            'type': 'object',
            'properties': self.a_property.as_dict(),
            'required': ['A']
        }
        self.d_parameter_dict = {
            'type': 'object',
            'properties': self.b_property,
            'required': ['B']
        }

    def test_class_identity(self):
        self.assertIsInstance(self.a_parameter, BaseParameter)
        self.assertIsInstance(self.b_parameter, BaseParameter)
        self.assertIsInstance(self.c_parameter, BaseParameter)
        self.assertIsInstance(self.d_parameter, BaseParameter)

    def test_class_equality(self):
        self.assertEqual(self.a_parameter.as_dict(), self.a_parameter_dict)
        self.assertEqual(self.b_parameter.as_dict(), self.b_parameter_dict)
        self.assertEqual(self.c_parameter.as_dict(), self.c_parameter_dict)
        self.assertEqual(self.d_parameter.as_dict(), self.d_parameter_dict)

    def test_class_inequality(self):
        self.assertNotEqual(self.a_parameter, self.a_parameter_dict)
        self.assertNotEqual(self.b_parameter, self.b_parameter_dict)
        self.assertNotEqual(self.c_parameter, self.c_parameter_dict)
        self.assertNotEqual(self.d_parameter, self.d_parameter_dict)

    def test_class_attributes_property(self):
        self.assertEqual(self.a_parameter.properties, self.a_parameter_dict['properties'])
        self.assertEqual(self.b_parameter.properties, self.b_parameter_dict['properties'])
        self.assertEqual(self.c_parameter.properties, self.c_parameter_dict['properties'])
        self.assertEqual(self.d_parameter.properties, self.d_parameter_dict['properties'])

        self.assertEqual(self.b_parameter.properties, self.c_parameter.properties)
        self.assertNotEqual(self.a_parameter.properties, self.d_parameter.properties)

    def test_class_attributes_required(self):
        self.assertEqual(self.a_parameter.required, self.a_parameter_dict['required'])
        self.assertEqual(self.b_parameter.required, self.b_parameter_dict['required'])
        self.assertEqual(self.c_parameter.required, self.c_parameter_dict['required'])
        self.assertEqual(self.d_parameter.required, self.d_parameter_dict['required'])

        self.assertIn(self.a_property.name, self.b_parameter.required)
        self.assertNotIn(self.a_property.name, self.d_parameter.required)

    def tearDown(self) -> None:
        pass


class TestBaseFunction(unittest.TestCase):

    def setUp(self) -> None:
        self.a_property = BaseProperty(name='A', obj_type='int', description='A', enum=['X', 'Y'])
        self.b_property = {'B': {'type': 'string', 'description': 'B'}}

        self.a_parameter = BaseParameter(properties=[self.a_property, self.b_property])
        self.b_parameter = BaseParameter(properties=[self.a_property], required=[self.a_property])

        self.a_function = BaseFunction(name='X', description='X', parameters=self.a_parameter)
        self.b_function = BaseFunction(name='Y', description='Y', parameters=self.b_parameter)

        self.a_function_dict = {
            'name': 'X',
            'description': 'X',
            'parameters': {
                'type': 'object',
                'properties': {self.a_property.name: self.a_property.as_dict(value_only=True),
                               'B': {'type': 'string', 'description': 'B'}},
                'required': []
            }
        }

        self.b_function_dict = {
            'name': 'Y',
            'description': 'Y',
            'parameters': {
                'type': 'object',
                'properties': self.a_property.as_dict(),
                'required': [self.a_property.name]
            }
        }

    def test_class_identity(self):
        self.assertIsInstance(self.a_function, BaseFunction)
        self.assertIsInstance(self.b_function, BaseFunction)

    def test_class_equality(self):
        self.assertEqual(self.a_function.as_dict(), self.a_function_dict)
        self.assertEqual(self.b_function.as_dict(), self.b_function_dict)

    def test_class_inequality(self):
        self.assertNotEqual(self.a_function, self.a_function_dict)
        self.assertNotEqual(self.b_function, self.b_function_dict)

    def test_class_attributes_parameters(self):
        self.assertEqual(self.a_function.parameters, self.a_function_dict['parameters'])
        self.assertEqual(self.b_function.parameters, self.b_function_dict['parameters'])

        self.assertNotEqual(self.a_function.parameters, self.b_function.parameters)

    def tearDown(self) -> None:
        pass


class TestBaseInstrument(unittest.TestCase):

    def setUp(self) -> None:
        self.a_property = BaseProperty(name='A', obj_type='int', description='A', enum=['X', 'Y'])
        self.b_property = {'B': {'type': 'string', 'description': 'B'}}

        self.a_parameter = BaseParameter(properties=[self.a_property, self.b_property])
        self.b_parameter = BaseParameter(properties=[self.a_property], required=[self.a_property])

        self.a_interface = BaseInterface()
        self.b_interface = BaseInterface()

        self.a_instrument = BaseInstrument(name='X', description='X', parameters=self.a_parameter,
                                           interface=self.a_interface)
        self.b_instrument = BaseInstrument(name='Y', description='Y', parameters=self.b_parameter,
                                           interface=self.b_interface)

        self.a_instrument_dict = {
            'name': 'X',
            'description': 'X',
            'parameters': {
                'type': 'object',
                'properties': {self.a_property.name: self.a_property.as_dict(value_only=True),
                               'B': {'type': 'string', 'description': 'B'}},
                'required': []
            }
        }

        self.b_instrument_dict = {
            'name': 'Y',
            'description': 'Y',
            'parameters': {
                'type': 'object',
                'properties': self.a_property.as_dict(),
                'required': [self.a_property.name]
            }
        }

    def test_class_identity(self):
        self.assertIsInstance(self.a_instrument, BaseInstrument)
        self.assertIsInstance(self.a_instrument, BaseInstrument)

    def test_class_equality(self):
        self.assertEqual(self.a_instrument.as_dict(), self.a_instrument_dict)
        self.assertEqual(self.b_instrument.as_dict(), self.b_instrument_dict)

    def test_class_inequality(self):
        self.assertNotEqual(self.a_instrument, self.a_instrument_dict)
        self.assertNotEqual(self.b_instrument, self.b_instrument_dict)

    def test_class_attributes_parameters(self):
        self.assertEqual(self.a_instrument.parameters, self.a_instrument_dict['parameters'])
        self.assertEqual(self.b_instrument.parameters, self.b_instrument_dict['parameters'])

        self.assertNotEqual(self.a_instrument.parameters, self.b_instrument.parameters)

    def test_class_attributes_interface(self):
        self.assertEqual(self.a_instrument.interface, self.a_interface)
        self.assertEqual(self.b_instrument.interface, self.b_interface)

        self.assertNotEqual(self.a_instrument.interface, self.b_interface)
        self.assertNotEqual(self.b_instrument.interface, self.a_interface)

    def tearDown(self) -> None:
        pass
