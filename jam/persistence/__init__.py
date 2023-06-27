from jam.persistence.memory import MemoryPersistence
from jam.persistence.sqlite import SQLitePersistence

try:
    from jam.persistence.postgres import PostgresPersistence
    from jam.persistence.mysql import MySQLPersistence
except ModuleNotFoundError as mn_err:
    pass
