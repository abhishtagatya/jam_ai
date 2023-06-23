from typing import Optional, List

from jam.instrument.base import BaseInstrument
from jam.personnel.base import BasePersonnel
from jam.persistence.memory import MemoryPersistence


class BaseJam(object):

    def __init__(self,
                 members: Optional[List[BasePersonnel]],
                 instruments: List[BaseInstrument] = None,
                 persistence: Optional[str] = None):
        self.members = members
        self.instruments = instruments

        self.persistence = persistence
        if self.persistence is None:
            self.persistence = MemoryPersistence()

        self.setup()

    def setup(self):
        for member in self.members:
            member.setup(self.instruments, self.persistence)

    def compose(self, message: str):
        pass
