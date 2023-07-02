import json
from typing import Dict

from jam.personnel.base import BasePersonnel
from jam.interface.openai import OpenAIComplete
from jam.util.prompt import (
    AUTO_PERSONNEL_PROMPT,
    AUTO_PERSONNEL_INSTRUCT_FIELD,
    AUTO_PERSONNEL_RESTRICT_FIELD
)


class BasicPersonnel(BasePersonnel):
    pass


class AutoPersonnel(BasePersonnel):

    @classmethod
    def from_prompt(cls, uid: str, prompt: str, mention_only: bool = False):
        x_prompt = AUTO_PERSONNEL_PROMPT.format(instruction_name=prompt.title())
        response = None
        try:
            response = OpenAIComplete().call(x_prompt)
            json_response = json.loads(response.output)

            json_response['uid'] = uid.lower().replace(' ', '_')
            json_response['instruction'] = cls._generate_instruction_field(x_dict=json_response)
            json_response['restriction'] = cls._generate_restriction_field(x_dict=json_response)

            return cls.from_dict(data=json_response, mention_only=mention_only)
        except json.decoder.JSONDecodeError as jdec_err:
            raise json.decoder.JSONDecodeError(
                msg=jdec_err.msg + f'. Got value {response.output}.',
                doc=jdec_err.doc,
                pos=jdec_err.pos
            )

    @staticmethod
    def _generate_category_str(x_dict: Dict) -> str:
        x_v = x_dict.get('categories', [])
        if len(x_v) > 1:
            return ', '.join(x_v[:-1]) + f', and {x_v[-1]}'
        return f'{x_v[-1]}'

    @staticmethod
    def _generate_instruction_field(x_dict: Dict) -> str:
        instruct_str = AUTO_PERSONNEL_INSTRUCT_FIELD.format(
            display_name=x_dict.get('display_name', ''),
            description=x_dict.get('description', ''),
            category_str=AutoPersonnel._generate_category_str(x_dict)
        )
        return instruct_str

    @staticmethod
    def _generate_restriction_field(x_dict: Dict) -> str:
        restrict_str = AUTO_PERSONNEL_RESTRICT_FIELD.format(
            category_str=AutoPersonnel._generate_category_str(x_dict)
        )
        return restrict_str
