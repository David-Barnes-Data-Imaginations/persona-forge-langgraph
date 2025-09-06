import duckdb
from dataclasses import dataclass
import os

@dataclass
class TableSchema:
    name:str
    columns:dict[str, str]
    primary_key:list[str]


def get_device_table_schema():
    return TableSchema(
        name="device",
        columns={
            "device_id" : "VARCHAR",
            "name": "VARCHAR",
            "ip_address": "VARCHAR",
        },
        primary_key=["device_id"],
    )