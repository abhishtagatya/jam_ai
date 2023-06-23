from typing import List, Dict, Union, Any

from jam.interface.base import BaseInterface


class BaseProperty(object):

    def __init__(self, name: str, obj_type: str = 'string', description: str = None, enum: List[Any] = None):
        self.name = name
        self.type = obj_type
        self.description = description
        self.enum = enum

    def as_dict(self, value_only=False):
        key = ['type', 'description', 'enum']
        val = [self.type, self.description, self.enum]

        if value_only:
            return {k: v for (k, v) in zip(key, val) if v}
        return {
            self.name: {k: v for (k, v) in zip(key, val) if v}
        }


class BaseParameter(object):

    def __init__(self,
                 obj_type: str = 'object',
                 properties: List[Union[BaseProperty, Dict]] = None,
                 required: List[Union[BaseProperty, str]] = None
                 ):
        self.type = obj_type

        self._prop = properties
        self.properties = self._structure_property()

        self._req = required or []
        self.required = self._structure_required()

    def _structure_required(self):
        return [
            x.name if isinstance(x, BaseProperty) else x for x in self._req
        ]

    def _structure_property(self):
        _prop = {}
        for p in self._prop:
            if isinstance(p, BaseProperty):
                _prop[p.name] = p.as_dict(value_only=True)
                continue
            k = [*p][0]  # Get Key
            v = p[k]  # Get Value
            _prop[k] = v
        return _prop

    def as_dict(self):
        return {
            'type': self.type,
            'properties': self.properties,
            'required': self.required
        }


class BaseFunction(object):

    def __init__(self,
                 name: str,
                 description: str,
                 parameters: Union[BaseParameter, Dict]
                 ):
        self.name = name
        self.description = description

        self._param = parameters
        self.parameters = self._structure_parameters()

    def _structure_parameters(self):
        return self._param.as_dict() if isinstance(self._param, BaseParameter) else self._param

    def as_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'parameters': self.parameters
        }


class BaseInstrument(BaseFunction):

    def __init__(self,
                 name: str,
                 description: str,
                 parameters: Union[BaseParameter, Dict],
                 interface: BaseInterface):
        super().__init__(name, description, parameters)
        self.interface = interface

    def setup(self):
        return

    def activate(self):
        return
