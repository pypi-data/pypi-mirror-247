import copy
from collections import defaultdict
from dataclasses import fields
from typing import Dict, List

from fragment.math_parser import eval_expr
from fragment.types import (
    BaseEntry,
    LedgerAccount,
    LedgerEntry,
    LedgerLine,
    LedgerLineSource,
    Schema,
)
from fragment.utils import (
    convert_instance_path_to_structural_path,
    fill_object_params,
    get_ancestors_for_instance_path,
)


def create_ledger_entry(schema: Schema, entry: BaseEntry) -> LedgerEntry:
    # Validate entry type
    if entry.__LEDGER_ENTRY_TYPE__ not in schema.entries:
        raise Exception(f"Invalid entry type: {entry.__LEDGER_ENTRY_TYPE__}")

    # Extract parameters
    parameters = dict()
    for field in fields(entry):
        if field.name == "__LEDGER_ENTRY_TYPE__":
            continue
        parameters[field.name] = getattr(entry, field.name)
    entry_schema = schema.entries[entry.__LEDGER_ENTRY_TYPE__]

    # Validate parameters
    for required_parameter in entry_schema.required_parameters:
        if required_parameter not in parameters:
            raise Exception(f"Invalid entry: missing parameter {required_parameter}")
    for parameter in parameters:
        if parameter not in entry_schema.required_parameters:
            raise Exception(f"Invalid entry: unknown parameter {parameter}")

    lines: List[LedgerLine] = []
    evaluated_entry_schema = copy.deepcopy(entry_schema)
    evaluated_entry_schema = fill_object_params(evaluated_entry_schema, parameters)

    for lineSchema in evaluated_entry_schema.lines:
        ## Math here later
        amount = eval_expr(lineSchema.amount)
        accountStructuralPath = convert_instance_path_to_structural_path(
            lineSchema.parameterized_path
        )
        schemaAccount = schema.accounts[accountStructuralPath]

        lines.append(
            LedgerLine(
                account=LedgerAccount(
                    path=lineSchema.parameterized_path,
                    template=schemaAccount.template,
                    type=schemaAccount.type,
                    name=schemaAccount.name,
                    currency_mode=schemaAccount.currency_mode,
                    currency=schemaAccount.currency,
                ),
                amount=amount,
                source=LedgerLineSource.ENTRY,
            )
        )

    account_to_amount: Dict[str, int] = defaultdict(int)
    aggregated_lines = []
    for line in lines:
        ancestorPaths = get_ancestors_for_instance_path(line.account.path)
        for ancestorPath in ancestorPaths:
            account_to_amount[ancestorPath] += line.amount

    for accountPath, amount in account_to_amount.items():
        structuralPath = convert_instance_path_to_structural_path(accountPath)
        schemaAccount = schema.accounts[structuralPath]
        aggregated_lines.append(
            LedgerLine(
                account=LedgerAccount(
                    path=accountPath,
                    template=schemaAccount.template,
                    type=schemaAccount.type,
                    name=schemaAccount.name,
                    currency_mode=schemaAccount.currency_mode,
                    currency=schemaAccount.currency,
                ),
                amount=amount,
                source=LedgerLineSource.AGGREGATED,
            )
        )

    return LedgerEntry(
        type=entry_schema.type,
        lines=lines,
        description=evaluated_entry_schema.description,
        aggregated_lines=aggregated_lines,
    )
