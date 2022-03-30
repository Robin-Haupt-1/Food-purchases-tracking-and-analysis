from mine.utils.logging import Logging
from mine.imports import *
from fp_types import *


class FoodPCLI:
    log = Logging("Food Purchase Tracker CLI").log
    server = "http://10.28.4.2:1241"
    stores = [Store]
    purchases = [Purchase]
    abstract_items = [AbstractProductItem]
    concrete_items = [ConcreteProductItem]

    def sync(self):
        """update all internal representations of db"""
        self.stores=[Store(**store) for store in requests.get(self.server+"/stores/all").json()]


    def __init__(self):
        self.log("Started")
        self.sync()
        print(self.stores)


cli = FoodPCLI()
