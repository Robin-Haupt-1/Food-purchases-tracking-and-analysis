from dataclasses import dataclass
import datetime

@dataclass
class Store:
    """Represents a store."""
    name:str
    ID:int=None

@dataclass
class Purchase:
    """Represents a purchase of a single item.
    """
    date:datetime.date
    storeID:int
    abstractItemID:int
    itemID:int=None
    ID:int=None


@dataclass
class AbstractProductItem:
    """
    Represents an abstract product.

    Metric: g/ml
    """
    name: str
    metric: str
    ID:int = None


@dataclass
class ConcreteProductItem:
    """
    Represents a concrete product.

    Measurement: weight/volume of product unit in g/ml
    """
    abstractItemID:int
    name: str
    brand: str
    measurement: int
    store_specific:bool
    storeID:int=None
    ID:int = None




