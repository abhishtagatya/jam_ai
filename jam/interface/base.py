from typing import Any, AnyStr


class JIOutput(object):
    JIO_TEXT = 'text'
    JIO_IMAGE = 'image'
    JIO_AUDIO = 'audio'
    JIO_VIDEO = 'video'
    JIO_FILE = 'file'
    JIO_OTHER = 'other'

    def __init__(self, out_type: str = JIO_TEXT, output: Any = '', function: AnyStr = None, success: bool = True):
        self.out_type = out_type
        self.output = output
        self.function = function
        self.success = success

    def __repr__(self):
        return f'<JIOutput output:{self.output}, function:{self.function}, success:{self.success}>'


class BaseInterface(object):

    def __init__(self):
        pass

    def call(self) -> JIOutput:
        return JIOutput()
