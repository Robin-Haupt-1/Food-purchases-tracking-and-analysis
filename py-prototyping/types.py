from dataclasses import dataclass

 
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
    abstractItemId:int
    name: str
    brand: str
    measurement: int
    ID:int = None




