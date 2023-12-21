from dataclasses import dataclass
from typing import Any

from phable.kinds import Grid, Ref


@dataclass
class ColIdMismatchError(Exception):
    help_msg: str


@dataclass
class ColNumMismatchError(Exception):
    help_msg: str


def merge_meta(x_meta: dict[str, Any], y_meta: dict[str, Any]) -> dict:
    """Merge two dicts.  If both dicts have the same key, then the key's value
    in y_meta is used."""
    return x_meta | y_meta


def merge_pt_data_to_his_grid_cols(
    his_grid: Grid, pt_data: Grid
) -> list[dict]:
    """Merges a point ID's data into a history grid's column metadata.  If the
    history grid's column metadata has the same key as the point ID's data,
    then the point ID's key value takes precedence."""

    # address the one point scenario if applicable
    if "id" in his_grid.meta.keys():
        return _get_cols_for_his_grid_with_two_cols(his_grid, pt_data)

    # address the multi point scenario if applicable
    else:
        return _get_cols_for_his_grid_with_multi_cols(his_grid, pt_data)


def _get_cols_for_his_grid_with_two_cols(
    his_grid: Grid, pt_data: Grid
) -> list[dict]:
    his_grid_id = his_grid.meta["id"]
    pt_grid_id = pt_data.rows[0]["id"]

    if len(pt_data.rows) > 1:
        raise ColNumMismatchError(
            "Expected only one row in the Point Data Grid "
            "and one non-ts col in the His Grid"
        )

    if his_grid_id != pt_grid_id:
        raise ColIdMismatchError(
            f"HisGrid's point ID {his_grid_id} is not equal to the point ID "
            f"{pt_grid_id} in the point data Grid as expected."
        )

    new_his_grid_cols = []
    for col in his_grid.cols:
        if col["name"] == "ts":
            new_his_grid_cols.append({"name": "ts"})
            continue

        if col.get("meta") is not None:
            new_col_meta = col["meta"] | pt_data.rows[0]
        elif col.get("meta") is None:
            new_col_meta = pt_data.rows[0]
        new_his_grid_cols.append({"name": col["name"], "meta": new_col_meta})

    return new_his_grid_cols


def _get_cols_for_his_grid_with_multi_cols(
    his_grid: Grid, pt_data: Grid
) -> list[dict]:
    if len(his_grid.cols) - 1 != len(pt_data.rows):
        raise ColNumMismatchError("")

    new_his_grid_cols = []
    for his_col in his_grid.cols:
        if his_col["name"] == "ts":
            new_his_grid_cols.append(his_col)
            continue
        his_col_id = his_col["meta"]["id"]
        pt_row = _find_pt_row_by_id(pt_data, his_col_id)
        if pt_row is None:
            raise ColIdMismatchError("")

        new_col_meta = his_col["meta"] | pt_row
        new_his_grid_cols.append(
            {"name": his_col["name"], "meta": new_col_meta}
        )

    return new_his_grid_cols


def _find_pt_row_by_id(pt_data: Grid, row_id: Ref) -> dict[Any]:
    for row in pt_data.rows:
        if row["id"] == row_id:
            return row
