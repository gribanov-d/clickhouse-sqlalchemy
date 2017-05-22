from sqlalchemy import util as sa_util
from sqlalchemy.engine import default

from ..base import ClickHouseDialectBase
from . import connector


# Export connector version
VERSION = (0, 0, 1, None)


class ClickHouseExecutionContext(default.DefaultExecutionContext):
    @sa_util.memoized_property
    def should_autocommit(self):
        return False  # No DML supported, never autocommit

    def pre_exec(self):
        # TODO: refactor this mess
        if not self.isinsert and not self.isddl:
            self.statement += ' FORMAT TabSeparatedWithNamesAndTypes'


class ClickHouseHttpDialect(ClickHouseDialectBase):
    driver = 'http'
    execution_ctx_cls = ClickHouseExecutionContext

    @classmethod
    def dbapi(cls):
        return connector

    def create_connect_args(self, url):
        kwargs = {}
        protocol = url.query.pop('protocol', 'http')
        port = url.port or 8123
        db_name = url.database or 'default'

        kwargs.update(url.query)

        db_url = '%s://%s:%d/' % (protocol, url.host, port)

        return (db_url, db_name, url.username, url.password), kwargs

    def _execute(self, connection, sql):
        sql += ' FORMAT TabSeparatedWithNamesAndTypes'
        return connection.execute(sql)


dialect = ClickHouseHttpDialect
