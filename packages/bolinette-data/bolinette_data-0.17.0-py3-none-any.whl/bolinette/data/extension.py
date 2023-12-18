from typing import override

from bolinette import core
from bolinette.core import Cache
from bolinette.core.command import command
from bolinette.core.environment import environment
from bolinette.core.extension import Extension
from bolinette.core.injection import injectable, injection_arg_resolver
from bolinette.data import DatabaseManager, DataSection, database_system
from bolinette.data.defaults import (
    AsyncPostgreSQL,
    AsyncSessionArgResolver,
    AsyncSQLite,
    PostgreSQL,
    SQLite,
    create_db_tables,
)
from bolinette.data.relational import AsyncTransaction, EntityManager


class _DataExtension(Extension):
    def __init__(self) -> None:
        super().__init__("data", [core])

    @override
    def add_cached(self, cache: Cache) -> None:
        environment("data", cache=cache)(DataSection)

        injectable(strategy="singleton", cache=cache)(DatabaseManager)
        injectable(strategy="singleton", cache=cache)(EntityManager)
        injectable(strategy="scoped", cache=cache)(AsyncTransaction)
        injection_arg_resolver(scoped=True, cache=cache)(AsyncSessionArgResolver)

        database_system(cache=cache)(SQLite)
        database_system(cache=cache)(AsyncSQLite)
        database_system(cache=cache)(PostgreSQL)
        database_system(cache=cache)(AsyncPostgreSQL)

        command("db init", summary="Creates the tables in database", cache=cache)(create_db_tables)


data_ext = _DataExtension()
