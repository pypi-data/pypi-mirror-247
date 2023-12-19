import re
from typing import Any, Dict, Optional, Set

from fragment.types import (
    CurrencyMode,
    Schema,
    SchemaLedgerAccount,
    SchemaLedgerEntry,
    SchemaLedgerLine,
)
from fragment.utils import (
    convert_parameterized_path_to_structural_path,
    get_instance_value_by_path,
    get_required_parameters,
    is_key_set,
)

Currency = tuple[str, Optional[str]]


def get_currency(currency: Any) -> Currency:
    if not is_key_set(currency, "code") or len(currency["code"]) == 0:
        raise Exception("Invalid schema: missing currency.code")
    code = currency["code"]
    if code == "CUSTOM" and (
        not is_key_set(currency, "customCurrencyId")
        or len(currency["customCurrencyId"]) == 0
    ):
        raise Exception("Invalid schema: missing currency.customCurrencyId")
    return (code, currency["customCurrencyId"] if code == "CUSTOM" else None)


def get_default_currency_mode_and_currency(
    chart_of_accounts: Any,
) -> tuple[CurrencyMode, Optional[Currency]]:
    if not is_key_set(chart_of_accounts, "defaultCurrencyMode"):
        if not is_key_set(chart_of_accounts, "defaultCurrency"):
            raise Exception(
                "Invalid schema: one of chartOfAccounts.defaultCurrencyMode or chartOfAccounts.defaultCurrency must be present"
            )
        return CurrencyMode.single, get_currency(chart_of_accounts["defaultCurrency"])
    else:
        if is_key_set(chart_of_accounts, "defaultCurrency"):
            if chart_of_accounts["defaultCurrencyMode"] != "single":
                raise Exception(
                    "Invalid schema: defaultCurrency cannot be set when defaultCurrencyMode is multi"
                )
            return CurrencyMode.single, get_currency(
                chart_of_accounts["defaultCurrency"]
            )
        return CurrencyMode(chart_of_accounts["defaultCurrencyMode"]), None


def parse_schema(
    raw_schema: Any,
) -> Schema:
    if not "key" in raw_schema:
        raise Exception("Invalid schema: missing key")

    if not "chartOfAccounts" in raw_schema:
        raise Exception("Invalid schema: missing chartOfAccounts")

    if not "ledgerEntries" in raw_schema:
        raise Exception("Invalid schema: missing ledgerEntries")

    chart_of_accounts = raw_schema["chartOfAccounts"]
    ledger_entries = raw_schema["ledgerEntries"]
    default_currency_mode, default_currency = get_default_currency_mode_and_currency(
        chart_of_accounts
    )

    if not "accounts" in chart_of_accounts:
        raise Exception("Invalid schema: missing chartOfAccounts.accounts")

    if not "types" in ledger_entries:
        raise Exception("Invalid schema: missing ledgerEntries.types")

    accounts = parse_accounts(
        chart_of_accounts["accounts"], default_currency_mode, default_currency
    )
    entries = parse_entries(ledger_entries["types"], accounts)

    return Schema(key=raw_schema["key"], accounts=accounts, entries=entries)


def get_account_type(account: Any, parent: SchemaLedgerAccount | None) -> str:
    type: str
    if parent is None:
        if "type" not in account:
            raise Exception("Invalid root account: missing type {account}")

        type = account["type"]
    else:
        if "type" in account and parent.type != account["type"]:
            raise Exception(
                "Invalid account: type different for child {account} and parent {parent}"
            )
        type = parent.type

    if type not in ["asset", "liability", "income", "expense"]:
        raise Exception(f"Invalid account type: {account['type']}")

    return type


def get_path_and_key(
    account: Any, parent: SchemaLedgerAccount | None, keys: Set[str]
) -> tuple[str, str]:
    if "key" not in account or len(account["key"]) == 0:
        raise Exception("Invalid account: missing key {account}")

    if account["key"] in keys:
        raise Exception(
            f"Invalid account: duplicate key {account['key']} under parents with parent {parent}"
        )
    key = account["key"]

    keys.add(key)
    if parent is None:
        path = key
    else:
        path = parent.structural_path + "/" + key

    return path, key


def get_account_currency(
    account: Any,
    default_currency_mode: CurrencyMode,
    default_currency: Optional[Currency],
) -> tuple[CurrencyMode, Optional[Currency]]:
    if is_key_set(account, "currency") and is_key_set(account, "currencyMode"):
        if account["currencyMode"] != "single":
            raise Exception(
                "Invalid account: currency cannot be set when currencyMode is multi"
            )
        currency_mode = account.get("currencyMode", default_currency_mode)
        currency = get_currency(account.get("currency", default_currency))
        return CurrencyMode(currency_mode), currency
    elif is_key_set(account, "currency"):
        return CurrencyMode.single, get_currency(account["currency"])
    elif is_key_set(account, "currencyMode"):
        if account["currencyMode"] != "multi":
            raise Exception(
                "Invalid account: currencyMode must be multi when currency is not set"
            )
        return CurrencyMode(account["currencyMode"]), None
    else:
        return default_currency_mode, default_currency


def get_template(account: Any, parent: None | SchemaLedgerAccount) -> bool:
    template = account.get("template", False)
    if not isinstance(template, bool):
        raise Exception("Invalid account: template must be boolean {account}")

    return template


def parse_accounts(
    accounts: Any,
    default_currency_mode: CurrencyMode,
    default_currency: Optional[Currency] = None,
    parent: SchemaLedgerAccount | None = None,
) -> Dict[str, SchemaLedgerAccount]:
    structual_path_to_schema_account: Dict[str, SchemaLedgerAccount] = {}

    for account in accounts:
        keys: Set[str] = set()
        type = get_account_type(account, parent)
        path, key = get_path_and_key(account, parent, keys)
        template = get_template(account, parent)
        name = account.get("name", key)
        currency_mode, currency = get_account_currency(
            account, default_currency_mode, default_currency
        )

        assert path not in structual_path_to_schema_account

        structual_path_to_schema_account[path] = SchemaLedgerAccount(
            type=type,
            key=key,
            structural_path=path,
            template=template,
            name=name,
            currency_mode=currency_mode,
            currency=currency,
        )

        if "children" in account:
            children = account["children"]
            children_parent = structual_path_to_schema_account[path]
            structual_path_to_schema_account.update(
                parse_accounts(
                    children,
                    children_parent.currency_mode,
                    children_parent.currency,
                    children_parent,
                )
            )

    return structual_path_to_schema_account


def parse_line(
    line: Any, structual_path_to_schema_account: Dict[str, SchemaLedgerAccount]
) -> SchemaLedgerLine:
    if "account" not in line:
        raise Exception("Invalid entry: missing account {line}")
    if "amount" not in line:
        raise Exception("Invalid entry: missing amount {line}")
    if not isinstance(line["amount"], str):
        raise Exception("Invalid entry: amount must be string {line}")
    account, amount = line["account"], line["amount"]

    if not re.match(r"^[\{\}\d\w+-]+$", amount):
        raise Exception(
            "Invalid expression: must only contain +, -, digits, paramaterize variables, and curly braces"
        )

    if "path" not in account:
        raise Exception("Invalid entry: missing path {account}")
    if not isinstance(account["path"], str):
        raise Exception("Invalid entry: path must be string {account}")

    parameterized_path = account["path"]
    structural_path = convert_parameterized_path_to_structural_path(parameterized_path)

    instanceValueByPath = get_instance_value_by_path(parameterized_path)

    required_parameters: Set[str] = get_required_parameters(line)
    for path, instanceValue in instanceValueByPath.items():
        structural_path = convert_parameterized_path_to_structural_path(path)
        if structural_path not in structual_path_to_schema_account:
            raise Exception(f"Invalid entry: unknown path {structural_path}")
        if (
            not structual_path_to_schema_account[structural_path].template
            and instanceValue is not None
        ):
            raise Exception(
                f"Invalid entry: path {structural_path} is not a template and has a parameter in line {line}"
            )

        if (
            instanceValue is None
            and structual_path_to_schema_account[structural_path].template
        ):
            raise Exception(
                f"Invalid entry: structural_path {structural_path} is a template and missing parameter in line {line}"
            )

        # Confirm instanceValue follows format {{1234}}
        if instanceValue is not None and not re.match(r"^{{\w+}}$", instanceValue):
            raise Exception(
                f"Invalid entry: structural_path {structural_path} has invalid parameter format {instanceValue} in line {line}"
            )

    account = structual_path_to_schema_account[structural_path]

    return SchemaLedgerLine(
        amount=amount,
        parameterized_path=parameterized_path,
        required_parameters=required_parameters,
    )


def parse_entries(
    entries: Any, structual_path_to_schema_account: Dict[str, SchemaLedgerAccount]
) -> Dict[str, SchemaLedgerEntry]:
    type_to_entry = {}

    # For each entry type, validate
    for entry in entries:
        if "type" not in entry:
            raise Exception("Invalid entry: missing type {entry}")

        type: str = entry["type"]
        if type in type_to_entry:
            raise Exception(f"Invalid entry: duplicate type {type}")

        if "lines" not in entry:
            raise Exception("Invalid entry: missing lines {entry}")

        lines = []
        if not isinstance(entry["lines"], list):
            raise Exception("Invalid entry: lines must be list {entry}")

        for line in entry["lines"]:
            lines.append(parse_line(line, structual_path_to_schema_account))

        description = entry.get("description", None)

        required_parameters = get_required_parameters(entry)

        ledger_entry = SchemaLedgerEntry(
            type=type,
            lines=lines,
            required_parameters=required_parameters,
            description=description,
        )
        type_to_entry[type] = ledger_entry

    return type_to_entry
