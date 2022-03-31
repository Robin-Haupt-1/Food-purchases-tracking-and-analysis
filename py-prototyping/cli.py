from mine.utils.logging import Logging
from mine.imports import *
from fp_types import *
import traceback


class FoodPCLI:
    log = Logging("Food Purchase Tracker CLI").log
    server = "http://10.28.4.2:1241"
    stores = [Store]
    abstract_items = [AbstractProductItem]
    concrete_items = [ConcreteProductItem]

    def sync(self):
        """update all internal representations of db"""
        self.stores = [Store(**store) for store in requests.get(self.server + "/stores/all").json()]
        self.concrete_items = [ConcreteProductItem(**store) for store in requests.get(self.server + "/items/concrete/all").json()]
        self.abstract_items = [AbstractProductItem(**store) for store in requests.get(self.server + "/items/abstract/all").json()]

    def __init__(self):
        self.log("Started")
        self.sync()
        selected_store: Store = None
        while True:
            if selected_store:
                if input(f"Keep store {colored(selected_store.name, 'yellow')}? y/n") == "y":
                    print("keeping!")
                else:
                    selected_store = None
            while selected_store is None:
                try:
                    self.log("Enter store")

                    for store in self.stores:
                        self.log(f'{store.ID}: {store.name}', start="\t", color="yellow")

                    store = int(input("Store:"))
                    for s in self.stores:
                        if s.ID == store:
                            selected_store = s
                except Exception as e:
                    print(traceback.print_exc())

            self.log("Selected " + colored(selected_store.name, "green"))

            continue
            while True:
                cost: int = None  # in cents
                concrete_item: ConcreteProductItem = None
                abstract_Item: AbstractProductItem = None
                measurement: int = None  # in ml/g
                amount: int = None

                self.sync()
                # start entering purchase procedure


cli = FoodPCLI()
