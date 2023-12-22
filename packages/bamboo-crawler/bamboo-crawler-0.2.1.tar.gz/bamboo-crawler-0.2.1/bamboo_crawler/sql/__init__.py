import json
from typing import Any, Dict, Optional, Union

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text

from ..interfaces.context import Context
from ..interfaces.inputter import Inputter
from ..interfaces.outputter import Outputter

Row = Optional[Dict]


class SQLInputter(Inputter[Row]):
    def __init__(
        self,
        url: str,
        *,
        table: Optional[str] = None,
        query: Optional[str] = None,
    ) -> None:
        if query is None and table is None:
            raise NotImplementedError("query or table must be specified")
        if query is not None and table is not None:
            raise NotImplementedError("query and table cannot be specified")

        self.engine = sqlalchemy.create_engine(url)
        select_query: sqlalchemy.sql.Select
        if table is not None:
            metadata = sqlalchemy.MetaData()
            metadata.reflect(self.engine, only=[table])
            Base = automap_base(metadata=metadata)
            Base.prepare()
            select_query = metadata.tables[table].select()
        else:
            assert query is not None
            select_query = text(query)  # type: ignore

        session = scoped_session(sessionmaker(bind=self.engine))
        self.result = session.execute(select_query)
        session.commit()
        self.keys = list(self.result.keys())

    def read(self) -> Context[Row]:
        r = self.result.fetchone()
        if r is None:
            return Context(None)
        p = dict(zip(self.keys, list(r)))
        return Context(p)


class SQLOutputter(Outputter[Any]):
    def __init__(
        self,
        url: str,
        *,
        table: Optional[str] = None,
        query: Optional[str] = None,
    ) -> None:
        self.query: Union[sqlalchemy.sql.Insert, str]
        if query is None and table is None:
            raise NotImplementedError
        if query is not None and table is not None:
            raise NotImplementedError
        self.engine = sqlalchemy.create_engine(url)
        self._type = "query"
        if table is not None:
            self._type = "table"
            metadata = sqlalchemy.MetaData()
            metadata.reflect(self.engine, only=[table])
            Base = automap_base(metadata=metadata)
            Base.prepare()
            self.query = metadata.tables[table].insert()
        else:
            assert query is not None
            self.query = query

    def write(
        self,
        value: Any,
        *,
        context: Optional[Context] = None,
    ) -> None:
        j = json.loads(value)
        insert_query: sqlalchemy.sql.Insert
        if self._type == "table":
            assert isinstance(self.query, sqlalchemy.sql.Insert)
            insert_query = self.query.values(j)
        else:
            assert isinstance(self.query, str)
            insert_query = text(self.query).bindparams(**j)  # type: ignore

        session_factory = sessionmaker(bind=self.engine)
        session = scoped_session(session_factory)
        session.execute(insert_query)
        session.commit()
