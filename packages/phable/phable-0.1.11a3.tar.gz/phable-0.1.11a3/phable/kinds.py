"""
The following Haystack types map directly to their Python equivalent types:
 - Bool
 - Str
 - List
 - Dict
 - Time
 - Date
 - DateTime
"""


from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, getcontext
from typing import Any

import pandas as pd

# -----------------------------------------------------------------------------
# Project Haystack supported kinds
# -----------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Grid:
    meta: dict[str, Any]
    cols: list[dict[str, Any]]
    rows: list[dict[str, Any]]

    def __str__(self):
        return "Haystack Grid"

    def get_ids(self) -> list[Ref]:
        # TODO: need to handle this differently if his_grid or standard grid
        return [row["id"] for row in self.rows]

    # TODO: Is this necessary?
    @staticmethod
    def to_grid(rows: dict[str, Any] | list[dict[str, Any]]) -> Grid:
        if isinstance(rows, dict):
            rows = [rows]

        cols = [{"name": name} for name in rows[0].keys()]
        meta = {"ver": "3.0"}

        return Grid(meta=meta, cols=cols, rows=rows)

    def to_pandas(self) -> pd.DataFrame:
        from phable.parsers.pandas import grid_to_pandas

        return grid_to_pandas(self)

    # TODO: add get_col_meta_by_id and get_col_meta_by_name


@dataclass(frozen=True, slots=True)
class Number:
    val: int | float
    unit: str | None = None

    def __str__(self):
        if self.unit is not None:
            return f"{self.val}{self.unit}"
        else:
            return f"{self.val}"


# Marker() is a singleton
class Marker:
    __instance = None

    def __new__(cls):
        if Marker.__instance is None:
            Marker.__instance = object.__new__(cls)
        return Marker.__instance

    def __str__(self):
        return "\u2713"


# Remove() is a singleton
class Remove:
    __instance = None

    def __new__(cls):
        if Remove.__instance is None:
            Remove.__instance = object.__new__(cls)
        return Remove.__instance

    def __str__(self):
        return "remove"


# NA() is a singleton
class NA:
    __instance = None

    def __new__(cls):
        if NA.__instance is None:
            NA.__instance = object.__new__(cls)
        return NA.__instance

    def __str__(self):
        return "NA"


@dataclass(frozen=True, slots=True)
class Ref:
    val: str
    dis: str | None = None

    def __str__(self) -> str:
        if self.dis is not None:
            return self.dis
        else:
            return f"@{self.val}"


@dataclass(frozen=True, slots=True)
class Uri:
    val: str

    def __str__(self):
        return self.val


@dataclass(frozen=True, slots=True)
class Coord:
    lat: Decimal
    lng: Decimal

    def __str__(self):
        getcontext().prec = 6
        return f"C({self.lat}, {self.lng})"


@dataclass(frozen=True, slots=True)
class XStr:
    type: str
    val: str

    def __str__(self):
        return f"({self.type}, {self.val})"


@dataclass(frozen=True, slots=True)
class Symbol:
    val: str

    def __str__(self):
        return f"^{self.val}"


# -----------------------------------------------------------------------------
# Additional kinds not supported by Project Haystack
# -----------------------------------------------------------------------------


# TODO: introduce generic Range which is DateRange | DateTimeRange | Date?


@dataclass(frozen=True, slots=True)
class DateRange:
    """DateRange describes a time range from midnight of the start date
    (inclusive) until midnight of the end date (exclusive).
    """

    start: date
    end: date

    def __str__(self):
        return self.start.isoformat() + "," + self.end.isoformat()


@dataclass(frozen=True, slots=True)
class DateTimeRange:
    """DateTimeRange describes a time range from a start timestamp (inclusive)
    until an end timestamp (exclusive).

    If end is undefined, then assume end to be when the last data value was
    recorded.
    """

    start: datetime
    end: datetime | None = None

    def __str__(self):
        if self.end is None:
            return _to_haystack_datetime(self.start)
        else:
            return (
                _to_haystack_datetime(self.start)
                + ","
                + _to_haystack_datetime(self.end)
            )


# -----------------------------------------------------------------------------
# Misc support functions
# -----------------------------------------------------------------------------


def _to_haystack_datetime(x: datetime) -> str:
    iana_tz = str(x.tzinfo)
    if "/" in iana_tz:
        haystack_tz = iana_tz.split("/")[-1]
    else:
        haystack_tz = iana_tz

    if x.microsecond == 0:
        dt = x.isoformat(timespec="seconds")
    else:
        dt = x.isoformat(timespec="milliseconds")

    return f"{dt} {haystack_tz}"
