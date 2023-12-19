from fragment.entry import create_ledger_entry
from fragment.schema_parser import parse_schema
from fragment.types import BaseEntry, LedgerEntry, Schema
from fragment.utils import read_file_as_json


class Fragment:
    schema: Schema

    def __init__(self, filePath: str) -> None:
        raw_schema = read_file_as_json(filePath)
        self.schema = parse_schema(raw_schema)

    def generate_entry(self, entry: BaseEntry) -> LedgerEntry:
        return create_ledger_entry(self.schema, entry)
