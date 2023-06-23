import os
import json
import pathlib
from typing import List, Dict, Any

from jam.instrument.base import BaseInstrument
from jam.persistence.base import BasePersistence
from jam.persistence.base import PersistenceObject
from jam.interface.openai import OpenAIChat
from jam.util.generate import generate_id


class BasePersonnel(object):
    BASE_TEMPLATE = {
        'uid': '<UNIQUE ID>',
        'display_name': '<DISPLAY NAME>',
        'description': '<DESCRIPTION>',
        'categories': ['<CAT-1>', '<CAT-2>']
    }

    def __init__(self,
                 uid: str,
                 display_name: str,
                 description: str,
                 categories: List[str],
                 instruction: str,
                 restriction: str,
                 extra: Dict,
                 mention_only: bool = False):
        self.uid = uid
        self.display_name = display_name
        self.description = description
        self.categories = categories
        self.instruction = instruction
        self.restriction = restriction
        self.extra = extra

        self.instruments = None
        self.persistence = None
        self.functions = None
        self.function_map = None
        self.engine = None

        self.mention_only = mention_only

        self.prompt = self.generate_prompt()

    def setup(self, instruments: List[BaseInstrument], persistence: BasePersistence):
        self.instruments = instruments
        self.persistence = persistence

        self.functions = self._structure_functions()
        self.function_map = self._structure_function_map()
        self.engine = OpenAIChat(functions=self.functions)

    def _structure_functions(self):
        return [func.as_dict() for func in self.instruments]

    def _structure_function_map(self):
        return {func.name: func.activate for func in self.instruments}

    def _retrieve_history(self):
        a = (self.persistence.find('author', [self.uid, 'user']))
        return list(map(PersistenceObject.as_message, a))

    def _retrieve_context(self):
        return [{'author': 'system', 'role': 'system', 'content': self.prompt}] + self._retrieve_history()

    def _save_message(self,
                      role: str,
                      author: str,
                      content: str,
                      function: str = None,
                      success: bool = True) -> PersistenceObject:
        return self.persistence.save(
            role=role,
            author=author,
            content=content,
            function=function,
            success=success
        )

    def call(self, x: Any, functional: bool = True) -> List[PersistenceObject]:
        po_outputs = []

        ctx_chain = self._retrieve_context()
        response = self.engine.call(messages=ctx_chain, functional=functional)

        if response.output.get('function_call'):
            f_name, f_response = self.function_call(response.output)

            if f_response.success:
                f_chain = [{'role': 'function', 'content': str(f_response.output), 'name': str(f_name)}]
                ctx_chain = self._retrieve_context() + f_chain
                after_response = self.engine.call(messages=ctx_chain, functional=False)
                saved_response = self._save_message(
                    role='assistant',
                    author=self.uid,
                    content=after_response.output['content'],
                    success=after_response.success
                )
                po_outputs += saved_response

                function_response = self._save_message(
                    role='function',
                    author=self.uid,
                    content=f_response.output,
                    function=f_name,
                    success=f_response.success
                )
                po_outputs += function_response
        else:
            saved_response = self._save_message(
                role='assistant',
                author=self.uid,
                content=response.output['content'],
                success=response.success
            )
            po_outputs += saved_response

        return po_outputs

    def function_call(self, x: Any):
        f_name = x['function_call']['name']
        f_call = self.function_map[f_name]
        f_args = json.loads(x['function_call']['arguments'])
        f_response = f_call(**f_args)

        return f_name, f_response

    @classmethod
    def get_template(cls, filepath: str = 'new-agent.json'):
        filename, file_extension = os.path.splitext(filepath)
        if file_extension == '.json':
            with open(filepath, 'w') as f:
                json.dump(cls.BASE_TEMPLATE, f)
            return True
        return False

    def generate_prompt(self):
        prompt = "INSTRUCTION:\n{instruction}\n\n".format(instruction=self.instruction)
        prompt += "RESTRICTIONS:\n{restriction}\n\n".format(restriction=self.restriction)
        prompt += "CHARACTER:\nName: {display_name}\nDescription: {description}\nCategories: {categories}\n\n".format(
            display_name=self.display_name,
            description=self.description,
            categories=', '.join(self.categories)
        )
        prompt += "EXTRA:\n{extra}\n".format(
            extra='\n'.join([
                '{key}: {value}'.format(
                    key=key.title().replace('_', ' '),
                    value=value
                ) for key, value in self.extra.items()
            ])
        )

        return prompt

    @classmethod
    def from_dict(cls, data: Dict, mention_only: bool = False):
        """
        Load Character from Dict

        :param instruments:
        :param mention_only:
        :param data: Dict
        :return: Instance
        """

        uid = data.get('uid', generate_id(8))
        display_name = data.get('display_name', 'No Name')
        description = data.get('description', '')
        categories = data.get('categories', [])
        instruction = data.get('instruction', '')
        restriction = data.get('restriction', '')
        extra = data.get('extra', {})

        return cls(
            uid=uid,
            display_name=display_name,
            description=description,
            categories=categories,
            instruction=instruction,
            restriction=restriction,
            extra=extra,
            mention_only=mention_only
        )

    @classmethod
    def from_json(cls, filepath: str = None, mention_only: bool = False):
        if os.path.exists(filepath):
            ext_file_df = pathlib.Path(filepath).suffix
            if ext_file_df == '.json' or ext_file_df == '.jsonl':
                with open(filepath, 'r') as config_file:
                    config_json = json.load(config_file)

                return cls.from_dict(data=config_json, mention_only=mention_only)
        raise ValueError(f'File {filepath} is not JSON. Please try another format.')
