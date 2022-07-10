import datetime
from typing import Optional
from mine.utils._logging import Logging
from mine.imports import *
from fp_types import *
import traceback


class TempItemId:
    items: [Union[ConcreteProductItem, AbstractProductItem, str, int]] = []

    def get_id(self, item: Union[ConcreteProductItem, AbstractProductItem, str, int]) -> int:
        if item not in self.items:
            self.items.append(item)
        return self.items.index(item) + 1

    def get_item(self, id: int) -> Union[ConcreteProductItem, AbstractProductItem, str]:
        return self.items[id - 1]

    def reset_ids(self):
        self.items = []


temp_item_id_helper = TempItemId()


class FoodPCLI:
    log = Logging("Food Purchase Tracker").log
    server = "http://localhost:1249"
    stores = [Store]
    abstract_items = [AbstractProductItem]
    concrete_items = [ConcreteProductItem]

    def __init__(self):
        self.sync()
        self.enter_purchase()

    def sync(self):
        """update all internal representations of db"""
        self.stores = [Store(**store) for store in requests.get(self.server + "/stores/all").json()]
        self.purchases = [Purchase(**purchase) for purchase in requests.get(self.server + "/purchases/all").json()]
        self.concrete_items = [ConcreteProductItem(**store) for store in requests.get(self.server + "/items/concrete/all").json()]
        self.concrete_items = sorted(self.concrete_items, key=lambda i: self.no_of_purchases(i), reverse=True)
        self.abstract_items = [AbstractProductItem(**store) for store in requests.get(self.server + "/items/abstract/all").json()]
        self.abstract_items = sorted(self.abstract_items, key=lambda i: self.no_of_purchases(i), reverse=True)

    def no_of_purchases(self, item: Union[AbstractProductItem, ConcreteProductItem]):
        def match_item(p: Purchase):
            if type(item) == AbstractProductItem:
                # also count it if a concrete item belonging to given abstract item was purchased
                return (p.abstractItemID or self.get_instance(p.concreteItemID, ConcreteProductItem).abstractItemID ) == item.ID

            if type(item) == ConcreteProductItem:
                return p.concreteItemID == item.ID

        return len([p for p in self.purchases if match_item(p)])

    def save_item_or_purchase(self, item: Union[ConcreteProductItem, AbstractProductItem, Purchase]) -> Optional[int]:
        """Send information to the server to be stored to db"""
        new_id = None
        try:
            # TODO DRY this up
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
                    self.log("Successfully created abstract product item!", color="green")
                    new_id = reply["id"] if "id" in reply else None

        except Exception:
            traceback.print_exc()
        self.sync()
        return new_id

    def get_instance(self, id, _type: type(Union[AbstractProductItem, ConcreteProductItem, Store])) -> Union[AbstractProductItem, ConcreteProductItem, Store]:
        """Get instance of items or stores from cached representation of db"""
        list_to_search = {ConcreteProductItem: self.concrete_items, AbstractProductItem: self.abstract_items, Store: self.stores}[_type]
        for i in list_to_search:
            if i.ID == id:
                return i
        self.log(f'No instance of type {_type.__name__} found for id {id}', color="red")

    def input_select_store(self) -> Store:
        """routine for selecting and returning store from other routines"""
        selected_store = None
        try:
            self.log("Select store:")
            self.log("-------------")

            for store in self.stores:
                # self.log(f'{temp_item_id_helper.get_id(store.ID)}: {store.name}', start="\t", color="yellow")
                self.log("{:<5} {:<10}".format(temp_item_id_helper.get_id(store.ID), store.name), color="yellow")  # start="\t",

            store = int(input("Store: "))
            for s in self.stores:
                if s.ID == temp_item_id_helper.get_item(store):
                    selected_store = s
            if selected_store:
                self.log("Selected " + colored(selected_store.name, "green"))
                temp_item_id_helper.reset_ids()
                return selected_store
        except Exception as e:
            pass

    def enter_purchase(self):
        selected_store: Optional[Store] = None
        date: Optional[datetime.date] = None
        while True:
            while selected_store is None:
                selected_store = self.input_select_store()

            while date is None:
                try:
                    self.log('Enter date in YYMMDD format (press Enter for today, n for today-n days)')

                    datestr = input("Date (YYMMDD): ").strip()
                    # datestr = ""
                    if datestr == "":
                        date = datetime.datetime.now().date()
                    else:
                        try:
                            date = datetime.datetime.strptime(datestr, "%y%m%d").date()
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

                self.log('Search for item (input "n" to create a new concrete, "na" new abstract item, - to update date and store, -d to update date, -s to update store)')
                _input = input("Search: ").strip()
                selected_item: Optional[AbstractProductItem, ConcreteProductItem] = None
                measurement: Optional[int] = None  # in ml/g
                amount: Optional[int] = None
                cost: Optional[int] = None
                do_break = False
                item_search_phrase = None
                while selected_item is None:

                    if _input == "n":
                        # create new item
                        selected_item = self.create_concrete_item(selected_store, item_search_phrase)
                        continue

                    if _input == "na":
                        # create new item
                        selected_item = self.create_abstract_item()
                        continue

                    elif _input == "-":
                        date = None
                        selected_store = None
                        do_break = True
                        break

                    elif _input == "-d":
                        date = None
                        do_break = True
                        break

                    elif _input == "-s":
                        selected_store = None
                        do_break = True
                        break

                    item_search_phrase = _input

                    # print all items to choose from
                    self.log("Abstract items:")
                    self.log("---------------")
                    for i in self.abstract_items:
                        if _input.lower() in i.name.lower():
                            self.log(f'{temp_item_id_helper.get_id(i)}: {str(i)}', color="yellow")
                    self.log("")

                    self.log("Concrete items:")
                    self.log("---------------")
                    for i in self.concrete_items:
                        if (not i.store_specific or i.store_specific and i.storeID == selected_store.ID) and _input.lower() in i.name.lower():
                            a = self.get_instance(i.abstractItemID, AbstractProductItem)
                            self.log(f'{temp_item_id_helper.get_id(i)}: {str(i)} ({i.measurement} {a.metric}) / {a.name}', color="yellow")

                    self.log("")
                    self.log("Other store's items:")
                    self.log("---------------")
                    for i in self.concrete_items:
                        if (i.store_specific and not i.storeID == selected_store.ID) and _input.lower() in i.name.lower():
                            a = self.get_instance(i.abstractItemID, AbstractProductItem)
                            self.log(f'{temp_item_id_helper.get_id(i)}: {str(i)} ({i.measurement} {a.metric}) / {a.name}', color="yellow")
                    _input = input("ID or new search phrase: (Enter=1) ").strip()

                    if _input == "":
                        _input = 1
                    try:
                        _id = int(_input)
                        selected_item = temp_item_id_helper.get_item(_id)
                    except Exception as e:
                        pass
                    temp_item_id_helper.reset_ids()
                if do_break:
                    break
                self.log(f'Selected: {colored(str(selected_item), "green")}')
                if type(selected_item) == ConcreteProductItem:
                    while amount is None:
                        try:
                            self.log("Input amount (1)")
                            _input = input("Amount: ").strip()
                            if _input == "":
                                amount = 1
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
                        cost = int(input("Cost: ").strip())
                        if amount > 1:
                            cost = int(cost / amount)
                    except Exception:
                        pass
                for i in range(amount if amount else 1):
                    new_purchase = Purchase(date, selected_store.ID, cost, concreteItemID=selected_item.ID if type(selected_item) == ConcreteProductItem else None,
                                            abstractItemID=selected_item.ID if type(selected_item) == AbstractProductItem else None, measurement=measurement)
                    self.save_item_or_purchase(new_purchase)

    def create_concrete_item(self, purchase_store, item_search_phrase) -> ConcreteProductItem:
        abstract_item: Optional[AbstractProductItem] = None
        store_specific: Optional[bool] = None
        store: Optional[Store] = None
        measurement: Optional[int] = None
        name: Optional[str] = None
        brand: Optional[str] = None

        self.log("Create abstract item? y/n (n)")
        _input = input("").strip()
        if _input == "y":
            abstract_item = self.create_abstract_item()

        if item_search_phrase:
            _input = item_search_phrase
            item_search_phrase = None
        else:
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
            self.log("Is store specific item? y/n (n)")
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
                self.log(f"Input name (Enter = {abstract_item.name})")
                name = input("Name: ").strip()
                if name == "":
                    name = abstract_item.name

            except Exception:
                pass

        while brand is None:
            all_brands = sorted(list(set([item.brand for item in self.concrete_items if (not item.store_specific or (store and item.storeID == store.ID))])), key=lambda x: x.lower())
            self.log('Select brand or type name:')
            self.log("Brands:")
            self.log("---------------")
            for b in all_brands:
                self.log(f'{temp_item_id_helper.get_id(b)}: {b}', color="yellow")
            self.log("")
            _input = input("ID/Name: ").strip()
            try:
                id = int(_input)
                brand = temp_item_id_helper.get_item(id)
            except Exception:
                brand = _input

            if _input == "-":
                brand = "Ohne Marke"
            self.log(f'Selected {colored(brand, color="green")}')
            temp_item_id_helper.reset_ids()

        new_concrete_item = ConcreteProductItem(abstractItemID=abstract_item.ID, name=name, brand=brand, measurement=measurement,
                                                store_specific=store_specific, storeID=store.ID if store else None)
        id = self.save_item_or_purchase(new_concrete_item)
        new_item = self.get_instance(id, ConcreteProductItem)
        return new_item

    def create_abstract_item(self) -> Optional[AbstractProductItem]:
        metric: Optional[str] = None
        name: Optional[str] = None

        while name is None:
            try:
                self.log(f"Input name")
                name = input("Name: ").strip()
            except Exception:
                pass

        while metric is None:
            try:
                self.log(f"Input metric (g/ml) (g)")
                _input = input("Metric: ").strip()
                if _input == "":
                    metric = "g"
                if _input in ["g", "ml"]:
                    metric = _input

            except Exception:
                pass

        new_abstract_item = AbstractProductItem(name=name, metric=metric)
        id = self.save_item_or_purchase(new_abstract_item)
        self.sync()
        created_item = None
        for i in self.abstract_items:
            if i.ID == id:
                created_item = i
        return created_item


cli = FoodPCLI()
