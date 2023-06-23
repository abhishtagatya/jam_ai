import string
import random


def generate_id(length: int = 8) -> str:
    source = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(source) for i in range(length)))
    return result_str
