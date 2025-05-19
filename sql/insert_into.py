import os


def insert_into_table(
    *,
    table_name: str,
    attributes: list,
    rows: list,
    output_path: str,
    append: bool = False,
):
    columns = ", ".join(attributes)
    values = []
    for row in rows:
        value_tuple = []
        for attr in attributes:
            value = row.get(attr, "")
            if isinstance(value, str):
                value_tuple.append(f"'{value.replace("'", "''")}'")
            else:
                value_tuple.append(str(value))
        values.append(f"({', '.join(value_tuple)})")
    sql = (
        f"--{table_name}\n"
        f"INSERT INTO {table_name} ({columns})\nVALUES\n    "
        + ",\n    ".join(values)
        + "\n;\n"
    )
    sql += (
        "SELECT *\n"
        f"FROM {table_name}\n"
        "OFFSET (\n"
        f"        SELECT COUNT(*)\n"
        f"        FROM {table_name}\n"
        "    ) - 10\n;\n\n"
    )
    mode = "a" if append else "w"
    with open(output_path, mode, encoding="utf-8") as f:
        f.write(sql)


if __name__ == "__main__":
    rows1 = [
        {"col1": "a", "col2": "b", "col3": "c"},
        {"col1": "x", "col2": "y", "col3": "z"},
    ]
    rows2 = [
        {"foo": 1, "bar": 2},
        {"foo": 3, "bar": 4},
    ]
    output_path = os.path.join(os.path.dirname(__file__), "insert_into.sql")
    insert_into_table(
        table_name="my_table",
        attributes=["col1", "col2", "col3"],
        rows=rows1,
        output_path=output_path,
        append=False,
    )
    insert_into_table(
        table_name="another_table",
        attributes=["foo", "bar"],
        rows=rows2,
        output_path=output_path,
        append=True,
    )
