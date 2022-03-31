from dataclasses import dataclass
import datetime
from typing import Union


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
    date: Union[datetime.date, str]
    storeID: int
    cost: int  # in cents

    concreteItemID: int = None
    abstractItemID: int = None
    measurement: int = None  # in ml/g
    amount: int = None
    ID: int = None

    def __post_init__(self):
        if type(self.date)==datetime.date:
            self.date = self.date.strftime("%Y-%m-%d")

        if not (self.measurement or self.amount):
            raise Exception("Please specify measurement or amount!")

        if not (self.concreteItemID or self.abstractItemID):
            raise Exception("Please supply ID of item!")

        if self.concreteItemID and not self.amount:
            raise Exception("Please specify amount of concrete item purchased")

        if self.abstractItemID and not self.measurement:
            raise Exception("Please specify measurement of abstract item purchased")


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

    def __post_init__(self):
        if self.store_specific and not self.storeID:
            raise Exception("Please specify ID of store this item is specific for!")
