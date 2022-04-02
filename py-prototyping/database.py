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
from enum import Enum

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


class Tables(Enum):
    STORES = "foodp_stores"
    ABSTRACT_ITEMS = "foodp_abstract_items"
    CONCRETE_ITEMS = "foodp_concrete_items"
    PURCHASES = "foodp_purchases"


class MySQLDatabase(IDatabase):
    def __init__(self, tables: type(Tables), mysql_connector: mysql.connector.connection):
        super(MySQLDatabase).__init__()
        self.tables = tables
        self.conn = mysql_connector

    def create(self, table: Tables, entry: dict) -> int:
        placeholders = ', '.join(['%s'] * len(entry))
        columns = ', '.join(entry.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table, columns, placeholders)
        cur.execute(sql, list(entry.values()))
        conn.commit()
        return cur.lastrowid or -1

    # ~ Create

    def create_concrete_item(self, item: ConcreteProductItem) -> int:
        return self.create(self.tables.CONCRETE_ITEMS.value, item.__dict__)

    def create_abstract_item(self, item: AbstractProductItem) -> int:
        return self.create(self.tables.ABSTRACT_ITEMS.value, item.__dict__)

    def create_purchase(self, purchase: Purchase) -> int:
        return self.create(self.tables.PURCHASES.value, purchase.__dict__)

    def create_store(self, store: Store) -> int:
        return self.create(self.tables.STORES.value, store.__dict__)

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
        cur.execute("select * from foodp_purchases")
        return [Purchase(**item) for item in cur.fetchall()]
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


db = MySQLDatabase(Tables, conn)
# db.create_store(Store(name="Test", ID=99))
print(db.get_all_stores())
