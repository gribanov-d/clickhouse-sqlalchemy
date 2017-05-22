from ..base import ClickHouseDialectBase
from . import connector


# Export connector version
VERSION = (0, 0, 1, None)


class ClickHouseHttpDialect(ClickHouseDialectBase):
    driver = 'native'

    @classmethod
    def dbapi(cls):
        return connector

    def create_connect_args(self, url):
        kwargs = {}
        port = url.port or 9000
        db_name = url.database or 'default'

        kwargs.update(url.query)

        return (url.host, port, db_name, url.username, url.password), kwargs

    def _execute(self, connection, sql):
        return connection.execute(sql)


dialect = ClickHouseHttpDialect
