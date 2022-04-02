from mine.utils.logging import Logging
from mine.imports import *
from fp_types import *
import traceback


class TempItemId:
    items: [Union[ConcreteProductItem, AbstractProductItem]] = []

    def get_id(self, item: Union[ConcreteProductItem, AbstractProductItem]):
        if not item in self.items:
            self.items.append(item)
        return self.items.index(item)

    def get_item(self, id: int):
        return self.items[id]


temp_item_id_helper=TempItemId()

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

    def get_abstract_item(self, id: int):
        for i in self.abstract_items:
            if i.ID == id:
                return i

    def __init__(self):
        self.log("Started")
        self.sync()
        selected_store: Store = None
        date: datetime.date = None
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

                    store = int(input("Store: "))
                    for s in self.stores:
                        if s.ID == store:
                            selected_store = s
                except Exception as e:
                    print(traceback.print_exc())

            self.log("Selected " + colored(selected_store.name, "green"))
            while date is None:
                try:
                    self.log('Enter date ("t" for today)')

                    #datestr = input("Date (YYYYMMDD): ").strip()
                    datestr="t"
                    if datestr == "t":
                        date = datetime.datetime.now().date()
                    else:
                        try:
                            date = datetime.datetime.strptime(datestr, "%Y%m%d")
                        except Exception as e:
                            print("Error!")
                except Exception as e:
                    print(traceback.print_exc())

            self.log("Selected " + colored(date.strftime('%Y-%m-%d'), "green"))

            while True:
                self.log('Search for item (input "n" to create a new one, - to update date and store')
                _input = input("Search: ").strip()
                selected_item: Union[AbstractProductItem, ConcreteProductItem, None] = None
                while selected_item is None:
                    if _input == "n":
                        # create new item
                        self.sync()
                        continue
                        pass
                    elif _input == "-":
                        date = None
                        selected_store = None
                        break

                    cost: int = None  # in cents
                    concrete_item: ConcreteProductItem = None
                    abstract_Item: AbstractProductItem = None

                    measurement: int = None  # in ml/g
                    amount: int = None

                    self.log("Abstract items:")
                    self.log("---------------")
                    for i in self.abstract_items:
                        if _input in i.name:
                            self.log(f'{temp_item_id_helper.get_id(i)}: {str(i)})', color="yellow")
                    self.log("")

                    self.log("Concrete items:")
                    self.log("---------------")
                    for i in self.concrete_items:
                        if _input in i.name:
                            a = self.get_abstract_item(i.abstractItemID)
                            self.log(f'{temp_item_id_helper.get_id(i)}: {str(i)} ({i.measurement} {a.metric})', color="yellow")

                    _input = input("ID or new search phrase: ").strip()

                    try:
                        _id = int(_input)
                        selected_item = temp_item_id_helper.get_item(_id)

                    except Exception as e:
                        pass

                    self.sync()


cli = FoodPCLI()
