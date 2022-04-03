from mine.utils.logging import Logging
from mine.imports import *
from fp_types import *
import traceback


class TempItemId:
    items: [Union[ConcreteProductItem, AbstractProductItem, str]] = []

    def get_id(self, item: Union[ConcreteProductItem, AbstractProductItem, str]) -> int:
        if item not in self.items:
            self.items.append(item)
        return self.items.index(item) + 1

    def get_item(self, id: int) -> Union[ConcreteProductItem, AbstractProductItem, str]:
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
        self.sync()
        return new_id

    def get_instance(self, id, _type: type(Union[AbstractProductItem, ConcreteProductItem, Store])) -> Union[AbstractProductItem, ConcreteProductItem, Store]:
        list_to_search = {ConcreteProductItem: self.concrete_items, AbstractProductItem: self.abstract_items, Store: self.stores}[_type]
        for i in list_to_search:
            if i.ID == id:
                return i
        self.log(f'No instance of type {_type.__name__} found for id {id}', color="red")

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
                    self.log('Enter date in YYYY-MM-DD format (press Enter for today, n for today-n days)')

                    datestr = input("Date (YYYYMMDD): ").strip()
                    # datestr = ""
                    if datestr == "":
                        date = datetime.datetime.now().date()
                    else:
                        try:
                            date = datetime.datetime.strptime(datestr, "%Y%m%d")
                        except Exception as e:
                            try:
                                past = int(datestr)
                                if past >= 0:
                                    date = (datetime.datetime.now() - datetime.timedelta(days=past)).date()

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
                        selected_item = self.create_concrete_item(selected_store)
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
                            a = self.get_instance(i.abstractItemID, AbstractProductItem)
                            self.log(f'{temp_item_id_helper.get_id(i)}: {str(i)} ({i.measurement} {a.metric})', color="yellow")

                    _input = input("ID or new search phrase: ").strip()

                    try:
                        _id = int(_input)
                        selected_item = temp_item_id_helper.get_item(_id)


                    except Exception as e:
                        pass
                    temp_item_id_helper.reset_ids()
                self.log(f'Selected: {colored(str(selected_item), "green")}')
                if type(selected_item) == ConcreteProductItem:

                    while amount is None:
                        try:
                            self.log("Input amount (1)")
                            _input=input("Amount: ").strip()
                            if _input=="":
                                amount=1
                            else:
                                amount = int(_input)

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
                        if amount>1:
                            cost=int(cost/amount)
                    except Exception:
                        pass
                for i in range(amount if amount else 1):
                    new_purchase = Purchase(date, selected_store.ID, cost, concreteItemID=selected_item.ID if type(selected_item) == ConcreteProductItem else None,
                                            abstractItemID=selected_item.ID if type(selected_item) == AbstractProductItem else None, measurement=measurement)
                    self.save_item_or_purchase(new_purchase)

    def create_concrete_item(self) -> ConcreteProductItem:
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
                if purchase_store:
                    store = purchase_store
                    self.log("Selected " + colored(store.name, "green"))
                else:
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
        id = self.save_item_or_purchase(new_concrete_item)
        new_item = self.get_instance(id, ConcreteProductItem)
        return new_item

    def create_abstract_item(self) -> Union[AbstractProductItem, None]:
        metric: Union[str, None] = None
        name: Union[str, None] = None

        while name is None:
            try:
                self.log(f"Input name")
                name = input("Name: ").strip()
            except Exception:
                pass

        while metric is None:
            try:
                self.log(f"Input metric (g/ml) (g)")
                _input = input("Measurement: ").strip()
                if _input == "":
                    metric = "g"
                if _input in ["g", "ml"]:
                    metric = _input

            except Exception:
                pass

        new_abstract_item = AbstractProductItem(name=name, metric=metric)
        id = self.save_item_or_purchase(new_abstract_item)
        self.sync()
        print(self.abstract_items)
        created_item = None
        for i in self.abstract_items:
            if i.ID == id:
                created_item = i
        return created_item


cli = FoodPCLI()
