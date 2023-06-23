from multiprocessing.pool import ThreadPool
from typing import List, Optional

from jam.base import BaseJam
from jam.version import version
from jam.instrument.base import BaseInstrument
from jam.persistence.base import BasePersistence
from jam.personnel.base import BasePersonnel
from jam.util.search import search_mention


class Jam(BaseJam):

    __version__ = version

    def __init__(self,
                 members: Optional[List[BasePersonnel]],
                 instruments: List[BaseInstrument] = None,
                 persistence: Optional[BasePersistence] = None):
        super(Jam, self).__init__(members, instruments, persistence)
        self.cache_output = []

    @staticmethod
    def _mention_filter(message: str, members: List[BasePersonnel]) -> List[BasePersonnel]:
        mention_filter = [member for member in members if member.uid in search_mention(message)]
        return mention_filter

    def _assign(self, member: BasePersonnel, message: str):
        call_output = member.call(message)
        self.cache_output += call_output
        return

    def _multi_assign(self, args):
        self._assign(*args)
        return

    def compose(self, message: str, multi=True):
        self.cache_output = []

        prompt_member = self._mention_filter(
            message, self.members
        ) or [member for member in self.members if not member.mention_only]
        self.persistence.save(
            role='user',
            author='user',
            content=message,
            mentions=[member.uid for member in prompt_member]
        )

        if multi:
            tasks = [(member, message) for member in prompt_member]
            with ThreadPool() as pool:
                pool.map(self._multi_assign, tasks)
        else:
            for member in prompt_member:
                self._assign(member, message)
        return self.cache_output

    def history(self):
        result = self.persistence.all()
        return result

    def clear(self):
        return
