import os
import warnings
from typing import AnyStr, Tuple, List, Dict

import openai
import requests
from PIL import Image

from jam.interface.base import BaseInterface, JIOutput
from jam.util.generate import generate_id

warnings.filterwarnings('ignore')


class OpenAIBase(BaseInterface):

    def __init__(self, token: str = None, model: str = None):
        super(OpenAIBase, self).__init__()
        self._token = token
        if self._token is None:
            self._token = os.getenv('OPENAI_KEY', '')

        openai.api_key = self._token
        self.open_ai = openai

        self.model = model


class OpenAIChat(OpenAIBase):
    DEFAULT_MODEL = 'gpt-3.5-turbo-0613'

    ROLE_SYSTEM = 'system'
    ROLE_USER = 'user'
    ROLE_ASSISTANT = 'assistant'
    ROLE_FUNCTION = 'function'

    def __init__(self,
                 token: str = None,
                 model: str = DEFAULT_MODEL,
                 functions: List[Dict] = None):
        super(OpenAIChat, self).__init__(token, model)
        self.functions = functions

    def call(self, messages: List[Dict] = None, functional: bool = True) -> JIOutput:
        x_message = self.form_message(messages)
        if functional:
            response = self.open_ai.ChatCompletion.create(
                model=self.model,
                messages=x_message,
                functions=self.functions,
                function_call='auto'
            )
            response_message = response['choices'][0]['message']
            return JIOutput(output=response_message)

        response = self.open_ai.ChatCompletion.create(
            model=self.model,
            messages=x_message,
        )
        response_message = response['choices'][0]['message']
        return JIOutput(output=response_message)

    @staticmethod
    def form_message(messages: List[Dict]) -> List[Dict]:
        msg_objs = []
        for message in messages:
            msg_obj = {
                'role': message.get('role', 'user'),
                'content': message.get('content', '')
            }
            if message.get('name'):
                msg_obj['name'] = message.get('name')

            msg_objs.append(msg_obj)
        return msg_objs


class OpenAIImageGen(OpenAIBase):

    def __init__(self,
                 token: str = None,
                 model: str = None,
                 samples: int = 1,
                 dimension: Tuple[int, int] = (512, 512)):
        super(OpenAIImageGen, self).__init__(token, model)

        self.samples = samples
        self.width, self.height = dimension

    def call(self, x: AnyStr = None) -> JIOutput:
        try:
            filenames = []
            response = openai.Image.create(
                prompt=x,
                n=self.samples,
                size=f'{self.width}x{self.height}'
            )

            for resp in response.get('data', []):
                filename = f'DALLE_{generate_id(8)}.png'
                img_url = resp.get('url', '')
                if img_url == '':
                    continue

                img = Image.open(requests.get(img_url, stream=True).raw)
                img.save(filename)
                filenames.append(filename)
            return JIOutput(
                out_type=JIOutput.JIO_TEXT,
                output=' '.join(filenames)
            )
        except openai.error.OpenAIError as oai_err:
            return JIOutput(
                out_type=JIOutput.JIO_TEXT,
                output=oai_err.user_message,
                success=False
            )
