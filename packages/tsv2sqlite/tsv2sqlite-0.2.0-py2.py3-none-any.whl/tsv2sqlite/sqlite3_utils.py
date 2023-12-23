import logging
import sqlite3
import copy

from typing import List
from datetime import datetime


TEST_MODE = False


__sqlite_conn = None


def create_database(database_file: str) -> None:
    """Create connection with SQLite3 database instance."""
    # Connect to SQLite database (or create it if it doesn't exist)
    global __sqlite_conn
    __sqlite_conn = sqlite3.connect(database_file)
    logging.info(f"Established connection with SQLite3 database '{database_file}'")


def create_provenance_table() -> None:
    # Create a cursor object to interact with the database
    cursor = __sqlite_conn.cursor()

    # Create a table named 'provenance'
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS provenance (
            bytesize INTEGER NOT NULL,
            abspath TEXT NOT NULL,
            md5checksum TEXT NOT NULL,
            date_created TEXT NOT NULL
        )
    """
    )
    logging.info("Created table 'provenance'")


def create_columnmaps_table() -> None:
    # Create a cursor object to interact with the database
    cursor = __sqlite_conn.cursor()

    # Create a table named 'columnmaps'
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS columnmaps (
            column_num INTEGER NOT NULL PRIMARY KEY,
            name TEXT NOT NULL,
            norm_name TEXT NOT NULL,
            UNIQUE (name, norm_name)
        )
    """
    )
    logging.info("Created table 'columnmaps'")


def create_records_table() -> None:
    # Create a cursor object to interact with the database
    cursor = __sqlite_conn.cursor()

    # Create a table named 'records'
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS records (
            line_num INTEGER NOT NULL,
            column_num INTEGER NOT NULL,
            value TEXT NOT NULL,
            UNIQUE (line_num, column_num),
            FOREIGN KEY (column_num) REFERENCES columnmaps (column_num)
        )
    """
    )
    logging.info("Created table 'records'")


def insert_provenance_table(
    bytesize: int, checksum: str, date_created: datetime, infile: str
) -> None:
    cursor = __sqlite_conn.cursor()
    cursor.execute(
        "INSERT INTO provenance (bytesize, abspath, md5checksum, date_created) VALUES (?, ?, ?, ?)",
        (bytesize, infile, checksum, date_created),
    )
    logging.info(f"Inserted metadata into provenance table for file '{infile}'")
    __sqlite_conn.commit()


def insert_columnmaps_table(column_num: int, name: str, normalized_name: str) -> None:
    cursor = __sqlite_conn.cursor()
    cursor.execute(
        "INSERT INTO columnmaps (column_num, name, norm_name) VALUES (?, ?, ?)",
        (column_num, name, normalized_name),
    )
    logging.info(
        f"Inserted mapping into columnmaps table for original column name '{name}'"
    )
    __sqlite_conn.commit()


def insert_records_table(line_num: int, column_num: int, value: str) -> None:
    cursor = __sqlite_conn.cursor()
    cursor.execute(
        "INSERT INTO records (line_num, column_num, value) VALUES (?, ?, ?)",
        (line_num, column_num, value),
    )
    logging.info(
        f"Inserted value into records table for line '{line_num}' column '{column_num}' value '{value}'"
    )
    __sqlite_conn.commit()


def create_table(table_name: str, column_names: List[str]) -> None:
    # Create a cursor object to interact with the database
    cursor = __sqlite_conn.cursor()

    column_datatype = [f"{column} TEXT" for column in column_names]
    column_datatype.append("line_number INTEGER NOT NULL")
    columns = ",\n".join(column_datatype)
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (" + columns + ")"

    if TEST_MODE:
        print(f"Running in test mode - would have executed '{create_table_sql}'")
    else:
        cursor.execute(create_table_sql)
        logging.info("Created table 'records'")


def insert_record(table_name: str, column_names: List[str], record: List[str], line_number: int) -> None:

    cursor = __sqlite_conn.cursor()

    column_names_copy = copy.copy(column_names)
    column_names_copy.append("line_number")
    columns = ", ".join(column_names_copy)

    values = ", ".join(record)
    # values = ", ".join(record) + ", " + line_number
    placeholders = []
    for _ in range(len(column_names_copy)):
        placeholders.append("?")

    # placeholders.append("?")
    placeholder = ", ".join(placeholders)

    # print(f"{columns=}")
    # print(f"{placeholder=}")
    # print(f"{values=}")

    record.append(line_number)
    # record_tuple = tuple(record)
    insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholder})"
    # insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholder}) ({values}, " + line_number + ")"

    if TEST_MODE:
        print(f"Running in test mode - would have executed '{insert_sql}' with values {record}")
    else:
        cursor.execute(insert_sql, record)
        logging.info(f"Inserted create into {table_name}")
        __sqlite_conn.commit()

