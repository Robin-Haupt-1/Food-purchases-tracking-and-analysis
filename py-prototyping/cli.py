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

    def reset_ids(self):
        self.items = []


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

    def save_item_or_purchase(self, item: Union[ConcreteProductItem, AbstractProductItem, Purchase]) -> Union[None, int]:
        new_id = None
        try:
            if type(item) == Purchase:
                x = requests.post(self.server + "/purchases/add",
                                  data=json.dumps(item.__dict__),
                                  headers={'Content-Type': 'application/json'})
                reply = json.loads(x.text)
                if reply["status"] == "success":
                    self.log("Successfully created purchase!", color="green")
                    new_id = reply["id"] if "id" in reply else None

            if type(item) == ConcreteProductItem:
                x = requests.post(self.server + "/items/concrete/add",
                                  data=json.dumps(item.__dict__),
                                  headers={'Content-Type': 'application/json'})

                reply = json.loads(x.text)
                if reply["status"] == "success":
                    self.log("Successfully created concrete product item!", color="green")
                    new_id = reply["id"] if "id" in reply else None
            if type(item) == AbstractProductItem:
                x = requests.post(self.server + "/items/abstract/add",
                                  data=json.dumps(item.__dict__),
                                  headers={'Content-Type': 'application/json'})

                reply = json.loads(x.text)
                if reply["status"] == "success":
                    self.log("Successfully created concrete abstract item!", color="green")
                    new_id = reply["id"] if "id" in reply else None

        except Exception:
            traceback.print_exc()
        return new_id

    def get_abstract_item(self, id: int):
        for i in self.abstract_items:
            if i.ID == id:
                return i

    def __init__(self):
        self.sync()
        self.create_concrete_item()
        # self.enter_purchase()

    def input_select_store(self) -> Store:
        selected_store = None
        try:
            self.log("Enter store")

            for store in self.stores:
                self.log(f'{store.ID}: {store.name}', start="\t", color="yellow")

            store = int(input("Store: "))
            for s in self.stores:
                if s.ID == store:
                    selected_store = s
            if selected_store:
                self.log("Selected " + colored(selected_store.name, "green"))
                return selected_store
        except Exception as e:
            print(traceback.print_exc())

    def enter_purchase(self):
        selected_store: Union[Store, None] = None
        date: [datetime.date, None] = None
        while True:
            selected_store = self.input_select_store()

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

                self.log('Search for item (input "n" to create a new one, - to update date and store)')
                _input = input("Search: ").strip()
                selected_item: Union[AbstractProductItem, ConcreteProductItem, None] = None
                measurement: Union[None, int] = None  # in ml/g
                amount: Union[None, int] = None
                cost: Union[None, int] = None

                while selected_item is None:

                    if _input == "n":
                        # create new item
                        self.create_concrete_item()
                        self.sync()
                        continue

                    elif _input == "-":
                        date = None
                        selected_store = None
                        break

                    concrete_item: Union[ConcreteProductItem, None] = None
                    abstract_Item: Union[AbstractProductItem, None] = None

                    self.log("Abstract items:")
                    self.log("---------------")
                    for i in self.abstract_items:
                        if _input.lower() in i.name.lower():
                            self.log(f'{temp_item_id_helper.get_id(i)}: {str(i)}', color="yellow")
                    self.log("")

                    self.log("Concrete items:")
                    self.log("---------------")
                    for i in self.concrete_items:
                        if _input.lower() in i.name.lower():
                            a = self.get_abstract_item(i.abstractItemID)
                            self.log(f'{temp_item_id_helper.get_id(i)}: {str(i)} ({i.measurement} {a.metric})', color="yellow")

                    _input = input("ID or new search phrase: ").strip()

                    try:
                        _id = int(_input)
                        selected_item = temp_item_id_helper.get_item(_id)
                        self.log(f'Selected: {colored(str(selected_item), "green")}')

                    except Exception as e:
                        pass
                    temp_item_id_helper.reset_ids()

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
                self.save_item_or_purchase(new_purchase)
            self.sync()

    def create_concrete_item(self):
        abstract_item: Union[AbstractProductItem, None] = None
        store_specific: Union[bool, None] = None
        store: Union[Store, None] = None
        measurement: Union[int, None] = None
        name: Union[str, None] = None
        brand: Union[str, None] = None

        self.log("Create abstract item? y (n)")
        _input = input("").strip()
        if _input == "y":
            abstract_item = self.create_abstract_item()

        if not abstract_item:
            self.log('Search for abstract item')
            _input = input("Search: ").strip()
        else:
            self.log(f'Selected: {colored(str(abstract_item), "green")}')

        while abstract_item is None:

            self.log("Abstract items:")
            self.log("---------------")
            for i in self.abstract_items:
                if _input.lower() in i.name.lower():
                    self.log(f'{temp_item_id_helper.get_id(i)}: {str(i)}', color="yellow")
            self.log("")

            _input = input("ID or new search phrase: ").strip()

            try:
                _id = int(_input)
                abstract_item = temp_item_id_helper.get_item(_id)
                self.log(f'Selected: {colored(str(abstract_item), "green")}')

            except Exception as e:
                pass

            temp_item_id_helper.reset_ids()

        while store_specific is None:
            self.log("Is store specific item? y (n)")
            _input = input("").strip()
            if _input == "y":
                store_specific = True
                store = self.input_select_store()
            else:
                store_specific = False

        while measurement is None:
            try:
                self.log(f"Input measurement (in {abstract_item.metric})")
                measurement = int(input("Measurement: ").strip())
            except Exception:
                pass

        while name is None:
            try:
                self.log(f"Input name")
                name = input("Name: ").strip()
            except Exception:
                pass

        while brand is None:
            try:
                self.log(f"Input brand")
                brand = input("Brand: ").strip()
            except Exception:
                pass
        new_concrete_item = ConcreteProductItem(abstractItemID=abstract_item.ID, name=name, brand=brand, measurement=measurement,
                                                store_specific=store_specific, storeID=store.ID if store else None)
        self.save_item_or_purchase(new_concrete_item)

    def create_abstract_item(self) -> AbstractProductItem:
        pass


cli = FoodPCLI()
