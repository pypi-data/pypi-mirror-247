from dataclasses import dataclass
from typing import Dict, List, Optional, Set

from strenum import StrEnum

"""
Schema types
"""


class CurrencyMode(StrEnum):
    multi = "multi"
    single = "single"

    def __repr__(self) -> str:
        return f"CurrencyMode.{self.value}"


# TODO: Support parameterization for accounts
@dataclass(frozen=True)
class SchemaLedgerAccount:
    # Accounting type: asset, liability, income, or expense
    # TODO: Try and use Literal["asset", "liability",..]
    type: str

    key: str
    template: bool

    # Human readable name. Defaults to key if not set.
    name: str

    # a/b/c instead of a/b:123/c or a/b:{{id}}/c
    structural_path: str

    currency_mode: CurrencyMode
    currency: Optional[tuple[str, Optional[str]]] = None


@dataclass(frozen=True)
class SchemaLedgerLine:
    """
    The key for the Ledger Line. Ledger Line keys are unique within a Ledge Entry.
    """

    key: str
    # a/b:{{id}}/c not a/b/c or a/b:123/c
    parameterized_path: str
    amount: str
    # Required parameters for this line.
    required_parameters: Set[str]


@dataclass(frozen=True)
class SchemaLedgerEntry:
    type: str
    lines: List[SchemaLedgerLine]

    # Required parameters for this entry.
    # In addition to the parameters  required for the entry,
    # this will include the parameters required for every line
    # that's part of this entry.
    required_parameters: Set[str]
    description: Optional[str] = None


@dataclass(frozen=True)
class Schema:
    # The schema key
    key: str
    # Structural path to account
    accounts: Dict[str, SchemaLedgerAccount]

    # Type to Entry
    entries: Dict[str, SchemaLedgerEntry]


"""
Data types
"""


@dataclass(frozen=True)
class LedgerAccount:
    # Accounting type: asset, liability, income, or expense
    type: str
    template: bool

    # Human readable name. Defaults to key if not set.
    name: str

    # a/b:123/c not a/b/c or a/b:{{id}}/c
    path: str

    currency_mode: CurrencyMode
    currency: Optional[tuple[str, Optional[str]]] = None


class LedgerLineSource(StrEnum):
    # If the line amount came from the entry directly
    ENTRY = "ENTRY"
    # If the line amount came from aggregating a child account
    AGGREGATED = "AGGREGATED"


@dataclass(frozen=True)
class BaseLedgerLine:
    account: LedgerAccount
    amount: int
    source: LedgerLineSource


@dataclass(frozen=True)
class LedgerLine(BaseLedgerLine):
    """
    The key for the Ledger Line. Ledger Line keys are unique within a Ledge Entry.
    """

    key: str


@dataclass(frozen=True)
class LedgerEntry:
    type: str
    lines: List[LedgerLine]
    aggregated_lines: List[BaseLedgerLine]
    description: Optional[str] = None


"""
Base classes for generated code
"""


@dataclass(frozen=True)
class BaseEntry:
    __LEDGER_ENTRY_TYPE__: str


@dataclass(frozen=True)
class BaseLedgerAccountFactory:
    __STRUCTURAL_PATH__: str
    __LEDGER_ACCOUNT_SCHEMA__: SchemaLedgerAccount

    @property
    def path(self) -> str:
        raise NotImplementedError()

    @property
    def account(self) -> LedgerAccount:
        return LedgerAccount(
            type=self.__LEDGER_ACCOUNT_SCHEMA__.type,
            template=self.__LEDGER_ACCOUNT_SCHEMA__.template,
            name=self.__LEDGER_ACCOUNT_SCHEMA__.name,
            path=self.path,
            currency=self.__LEDGER_ACCOUNT_SCHEMA__.currency,
            currency_mode=self.__LEDGER_ACCOUNT_SCHEMA__.currency_mode,
        )
