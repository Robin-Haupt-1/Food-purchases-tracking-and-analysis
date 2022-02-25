from mine.private import mysql_cred_localhost
import datetime
import pickle

from mine.utils.logging import Logging
import json
import random
from dataclasses import dataclass
import mysql.connector
from fp_types import *
import datetime

log = Logging("FPT Database").log

conn = mysql.connector.connect(**mysql_cred_localhost, database="meta")
cur = conn.cursor(dictionary=True)


class IDatabase:
    def __init__(self):
        """"""

    # ~ Create

    def create_concrete_item(self, item: ConcreteProductItem):
        pass

    def create_abstract_item(self, item: AbstractProductItem):
        pass

    def create_purchase(self, purchase: Purchase):
        pass

    def create_store(self, store: Store):
        pass

    # ~ Read

    def get_all_stores(self) -> [Store]:
        pass

    def get_all_abstract_items(self) -> [AbstractProductItem]:
        pass

    def get_all_concrete_items(self) -> [ConcreteProductItem]:
        pass

    def get_all_purchases(self) -> [Purchase]:
        pass

    # ~ Update

    def update_concrete_item(self, item: ConcreteProductItem):
        pass

    def update_abstract_item(self, item: AbstractProductItem):
        pass

    def update_purchase(self, purchase: Purchase):
        pass

    def update_store(self, store: Store):
        pass

    # ~ Delete

    def delete_concrete_item(self, item: ConcreteProductItem):
        pass

    def delete_abstract_item(self, item: AbstractProductItem):
        pass

    def delete_purchase(self, purchase: Purchase):
        pass

    def delete_store(self, store: Store):
        pass


class MySQLDatabase(IDatabase):
    def __init__(self):
        super(MySQLDatabase).__init__()
        """"""

    # ~ Create

    def create_concrete_item(self, item: ConcreteProductItem):
        pass

    def create_abstract_item(self, item: AbstractProductItem):
        pass

    def create_purchase(self, purchase: Purchase):
        pass

    def create_store(self, store: Store):
        storeDict = store.__dict__
        placeholders = ', '.join(['%s'] * len(storeDict))
        columns = ', '.join(storeDict.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("foodp_stores", columns, placeholders)
        cur.execute(sql, list(storeDict.values()))
        # cur.execute("insert into foodp_stores (name,ID) value (%s,%s)", (store.name, store.ID))
        conn.commit()
        pass

    # ~ Read

    def get_all_stores(self) -> [Store]:
        cur.execute("select * from foodp_stores")
        return [Store(**store) for store in cur.fetchall()]

    def get_all_abstract_items(self) -> [AbstractProductItem]:
        cur.execute("select * from foodp_abstract_items")
        return [AbstractProductItem(**item) for item in cur.fetchall()]

    def get_all_concrete_items(self) -> [ConcreteProductItem]:
        cur.execute("select * from foodp_concrete_items")
        return [ConcreteProductItem(**item) for item in cur.fetchall()]
        pass

    def get_all_purchases(self) -> [Purchase]:
        pass

    # ~ Update

    def update_concrete_item(self, item: ConcreteProductItem):
        pass

    def update_abstract_item(self, item: AbstractProductItem):
        pass

    def update_purchase(self, purchase: Purchase):
        pass

    def update_store(self, store: Store):
        pass

    # ~ Delete

    def delete_concrete_item(self, item: ConcreteProductItem):
        pass

    def delete_abstract_item(self, item: AbstractProductItem):
        pass

    def delete_purchase(self, purchase: Purchase):
        pass

    def delete_store(self, store: Store):
        pass


db = MySQLDatabase()
db.create_store(Store(name="Test", ID=59))

