import json
import os
from typing import AnyStr, Tuple

from jam.interface.base import BaseInterface, JIOutput
from jam.util.generate import generate_id

import requests
from PIL import Image


class WriteSonicBase(BaseInterface):

    def __init__(self,
                 api_key: str = None,
                 product: str = None,
                 engine: str = None,
                 language: str = 'en'):
        super(WriteSonicBase, self).__init__()
        self._api_key = api_key
        if self._api_key is None:
            self._api_key = os.getenv('WRITESONIC_KEY', '')

        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": self._api_key
        }

        self.product = product
        self.base_url = 'https://api.writesonic.com/v2/business/content/{product}'.format(
            product=self.product
        )
        self.engine = engine
        self.language = language


class PhotoSonicText2Image(WriteSonicBase):

    def __init__(self,
                 api_key: str = None,
                 product: str = 'generate-image',
                 engine: str = 'premium',
                 language: str = 'en',
                 num_copies: int = 1,
                 num_images: int = 1,
                 dimension: Tuple[int, int] = (512, 512),
                 ):
        super().__init__(api_key, product, engine, language)
        self.num_copies = num_copies
        self.num_images = num_images
        self.width, self.height = dimension

    def call(self, x: AnyStr = None) -> JIOutput:
        filenames = []

        self.headers['num_copies'] = str(self.num_copies)
        payload = {
            "num_images": self.num_images,
            "image_width": self.width,
            "image_height": self.height,
            "prompt": x
        }

        response = requests.post(self.base_url, json=payload, headers=self.headers)
        json_response = json.loads(response.text)

        if response.status_code == 200:
            for img_url in json_response.get('images', []):
                filename = f'PhotoSonic_{generate_id(8)}.png'
                img = Image.open(requests.get(img_url, stream=True).raw)
                img.save(filename)
                filenames.append(filename)
            return JIOutput(
                out_type=JIOutput.JIO_TEXT,
                output=' '.join(filenames)
            )
        return JIOutput(
            out_type=JIOutput.JIO_FILE,
            output=json_response.get('msg', ''),
            success=False
        )


