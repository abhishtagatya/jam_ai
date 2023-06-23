from typing import Union, Dict, AnyStr

from jam.instrument.base import BaseInstrument, BaseParameter, BaseProperty
from jam.interface.base import BaseInterface
from jam.interface.openai import OpenAIImageGen

_OpenAIImageGen = OpenAIImageGen()
_PromptPainterPromptProperty = BaseProperty(
    name='prompt', description='The text prompt to generate the image'
)
_PromptPainterParameters = BaseParameter(
    properties=[_PromptPainterPromptProperty],
    required=[_PromptPainterPromptProperty]
)


class PromptPainter(BaseInstrument):

    def __init__(self,
                 name: str = 'prompt_painter',
                 description: str = 'Generates image from text prompt',
                 parameters: Union[BaseParameter, Dict] = _PromptPainterParameters,
                 interface: BaseInterface = _OpenAIImageGen):
        super().__init__(name, description, parameters, interface)

    def activate(self, prompt: AnyStr = None):
        if prompt is None:
            return

        response = self.interface.call(prompt)
        return response
