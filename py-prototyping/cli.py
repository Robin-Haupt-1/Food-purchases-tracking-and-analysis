from mine.utils.logging import Logging
from mine.imports import *
from fp_types import *
import traceback


class TempItemId:
    items: [Union[ConcreteProductItem, AbstractProductItem]] = []

    def get_id(self, item: Union[ConcreteProductItem, AbstractProductItem]) -> int:
        if item not in self.items:
            self.items.append(item)
        return self.items.index(item) + 1

    def get_item(self, id: int) -> Union[ConcreteProductItem, AbstractProductItem]:
        return self.items[id - 1]


temp_item_id_helper = TempItemId()


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

    def save_purchase(self, purchase: Purchase):
        try:
            x = requests.post(self.server + "/purchases/add",
                              data=json.dumps(purchase.__dict__),
                              headers={'Content-Type': 'application/json'})

            if json.loads(x.text)["status"] == "success":
                self.log("Successfully created purchase!", color="green")
        except Exception:
            traceback.print_exc()

    def get_abstract_item(self, id: int):
        for i in self.abstract_items:
            if i.ID == id:
                return i

    def __init__(self):
        self.log("Started")
        self.sync()
        selected_store: Union[Store, None] = None
        date: [datetime.date, None] = None
        while True:
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
                    self.log('Enter date in YYYY-MM-DD format (press Enter for today)')

                    datestr = input("Date (YYYYMMDD): ").strip()
                    # datestr = ""
                    if datestr == "":
                        date = datetime.datetime.now().date()
                    else:
                        try:
                            date = datetime.datetime.strptime(datestr, "%Y%m%d")
                        except Exception as e:
                            print("Error!")
                except Exception as e:
                    print(traceback.print_exc())

            self.log("Selected " + colored(date.strftime('%Y-%m-%d'), "green"))
            while selected_store is not None and date is not None:

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

                    cost: Union[int, None] = None  # in cents
                    concrete_item: Union[ConcreteProductItem, None] = None
                    abstract_Item: Union[AbstractProductItem, None] = None

                    measurement: Union[None, int] = None  # in ml/g
                    amount: Union[None, int] = None

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
                        self.log(f'Selected: {colored(str(selected_item), "green")}')

                    except Exception as e:
                        pass

                if type(selected_item) == ConcreteProductItem:

                    while amount is None:
                        try:
                            self.log("Input amount")
                            amount = int(input("Amount: ").strip())
                        except Exception:
                            pass

                if type(selected_item) == AbstractProductItem:
                    while measurement is None:
                        try:
                            self.log(f"Input measurement (in {selected_item.metric})")
                            measurement = int(input("Measurement: ").strip())
                        except Exception:
                            pass

                while cost is None:
                    try:
                        self.log(f"Input cost (in Eurocent)")
                        cost = int(input("Measurement: ").strip())
                    except Exception:
                        pass
                new_purchase = Purchase(date, selected_store.ID, cost, concreteItemID=selected_item.ID if type(selected_item) == ConcreteProductItem else None,
                                        abstractItemID=selected_item.ID if type(selected_item) == AbstractProductItem else None, measurement=measurement, amount=amount)
            self.sync()


cli = FoodPCLI()
