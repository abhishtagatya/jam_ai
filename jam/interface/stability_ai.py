import os
import io
import warnings
from typing import AnyStr, Tuple

from jam.interface.base import BaseInterface, JIOutput

from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation


class StabilityAIBase(BaseInterface):

    def __init__(self,
                 engine: str,
                 api_key: str = None,
                 host: str = 'grpc.stability.ai:443',
                 verbose: bool = True,
                 step: int = 30,
                 cfg_scale: float = 8.0,
                 dimension: Tuple[int, int] = (512, 512),
                 samples: int = 1,
                 sampler: int = generation.SAMPLER_K_DPMPP_2M
                 ):
        super(StabilityAIBase, self).__init__()
        self.engine = engine
        self._api_key = api_key
        if self._api_key is None:
            self._api_key = os.getenv('STABILITY_KEY', '')

        self._host = host
        if self._host is None:
            self._host = os.getenv('STABILITY_HOST', '')

        self.verbose = verbose
        self.stability_api = client.StabilityInference(
            key=self._api_key,
            verbose=self.verbose,
            engine=self.engine,
        )

        # Generation Config
        self.step = step
        self.cfg_scale = cfg_scale
        self.width, self.height = dimension
        self.samples = samples
        self.sampler = sampler


class StabilityText2Image(StabilityAIBase):

    def __init__(self,
                 engine: str = 'stable-diffusion-v1',
                 api_key: str = None,
                 host: str = 'grpc.stability.ai:443',
                 verbose: bool = True):
        super(StabilityText2Image, self).__init__(engine, api_key, host, verbose)

    def call(self, x: AnyStr = None) -> JIOutput:
        filenames = []
        response = self.stability_api.generate(
            prompt=x,
            steps=self.step,
            cfg_scale=self.cfg_scale,
            width=self.width,
            height=self.height,
            samples=self.samples,
            sampler=self.sampler
        )

        for resp in response:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    filename = 'Stability_' + str(artifact.seed) + ".png"
                    img = Image.open(io.BytesIO(artifact.binary))
                    img.save(filename)
                    filenames.append(filename)
        return JIOutput(
            out_type=JIOutput.JIO_TEXT,
            output=' '.join(filenames)
        )
