import re
from datetime import datetime, timedelta
from typing import Any, Optional, Union
from zoneinfo import ZoneInfo

import sqlalchemy as sa
from ezloggers import get_logger
from sqlalchemy.engine import Compiled, Engine
from sqlalchemy.orm.decl_api import DeclarativeMeta

logger = get_logger("pg-components", stdout=True)


def execute_sql(sql: Any, engine: Engine):
    """Execute a SQL statement."""
    logger.info(sql)
    if isinstance(sql, str):
        sql = sa.text(sql)
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        return conn.execute(sql)


def compile_sa(engine: Engine, statement: Any) -> str:
    """Compile a SQLAlchemy statement and bind query parameters."""
    if isinstance(statement, (str, Compiled)):
        return statement
    with engine.begin() as conn:
        return statement.compile(conn, compile_kwargs={"literal_binds": True})


_ws_re = re.compile(r"\s+")
_camel_re = re.compile(r"([a-z0-9])([A-Z])")
_digit_start_re = re.compile(r"^\d")


def to_snake_case(name: str) -> str:
    """Convert `name` to snake case and also add a leading underscore to variables starting with a digit.

    Args:
        name (str): The name to convert.

    Returns:
        str: The converted name.
    """
    # remove trailing space.
    name = name.strip()
    # convert space to underscores.
    name = _ws_re.sub("_", name)
    # convert camel case to underscores.
    if not name.isupper():
        name = _camel_re.sub(lambda m: f"{m.group(1)}_{m.group(2)}", name)
    # variable names can't start with number, so add leading underscore.
    if _digit_start_re.match(name):
        name = f"_{name}"
    # make name lowercase.
    return name.lower()


def to_table(table: Union[sa.Table, DeclarativeMeta]) -> sa.Table:
    """Extract the SQLAlchemy table from an entity, or return the passed argument if argument is already a table.

    Args:
        table (Union[sa.Table, DeclarativeMeta]): An entity or table object.

    Raises:
        ValueError: If argument is not an entity or table object.

    Returns:
        sa.Table: The table corresponding to the passed argument.
    """
    if isinstance(table, sa.Table):
        return table
    elif hasattr(table, "__table__"):
        return table.__table__
    raise ValueError(
        f"Object {table} is not an entity or table! Can not extract table."
    )


def schema_table(table: sa.Table) -> str:
    return f"{table.schema or 'public'}.{table.name}"


def next_time_occurrence(
    hour: int,
    minute: int = 0,
    second: int = 0,
    tz: Optional[Union[str, ZoneInfo]] = None,
) -> datetime:
    """Return the next datetime at time with specified hour/minute."""
    now = datetime.now()
    if tz:
        if isinstance(tz, str):
            tz = ZoneInfo(tz)
        now = now.astimezone(tz)
    if now.hour >= hour:
        now += timedelta(days=1)
    return now.replace(hour=hour, minute=minute, second=second, microsecond=0)
