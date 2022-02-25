from dataclasses import dataclass
import datetime


@dataclass
class Store:
    """Represents a store."""
    name: str
    ID: int = None


@dataclass
class Purchase:
    """Represents a purchase of a single item.
    if its a concrete item, has amount, but no measurement (this can be calculated from concrete item measurement * amount)
    if its an abstract item (fresh cherries weighed at checkout) has measurement but no amount
    """
    date: datetime.date
    storeID: int
    cost: int  # in cents

    concreteItemID: int = None
    abstractItemID: int = None
    measurement: int = None  # in ml/g
    amount: int = None
    ID: int = None


@dataclass
class AbstractProductItem:
    """
    Represents an abstract product.

    Metric: g/ml
    """
    name: str
    metric: str
    ID: int = None


@dataclass
class ConcreteProductItem:
    """
    Represents a concrete product.

    Measurement: weight/volume of product unit in g/ml
    """
    abstractItemID: int
    name: str
    brand: str
    measurement: int
    store_specific: bool
    storeID: int = None
    ID: int = None
