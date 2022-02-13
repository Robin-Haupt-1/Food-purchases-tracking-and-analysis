from mine.private import mysql_cred_localhost
import datetime
import pickle

from mine.utils.logging import Logging
import json
import random
from dataclasses import dataclass
import mysql.connector
from fp_types import *

log = Logging("FPT Database").log

conn = mysql.connector.connect(**mysql_cred_localhost, database="meta")
cur = conn.cursor(dictionary=True)


class IDatabase:
    def __init__(self):
        """"""

    # ~ Read

    def all_stores(self) -> [Store]:
        """Returns all stores"""

    def all_abstract_items(self) -> [AbstractProductItem]:
        """Returns all abstract items"""

    def all_concrete_items(self) -> [ConcreteProductItem]:
        """Returns all concrete items"""

    def all_purchases(self) -> [Purchase]:
        """Returns all purchases"""

    # ~ Add

    def add_concrete_item(self, item: ConcreteProductItem):
        """Add a concrete item"""

    def add_abstract_item(self, item: AbstractProductItem):
        """Add an abstract item"""

    def add_purchase(self, purchase: Purchase):
        """Add a purchase"""

    def add_store(self, store: Store):
        """Add a store"""


class MySQLDatabase(IDatabase):
    def __init__(self):
        super(MySQLDatabase).__init__()
        """"""

    # ~ Read

    def all_stores(self) -> [Store]:
        cur.execute("select * from foodp_stores")
        return [Store(**store) for store in cur.fetchall()]

    def all_abstract_items(self) -> [AbstractProductItem]:
        cur.execute("select * from foodp_abstract_items")
        return [AbstractProductItem(**item) for item in cur.fetchall()]

    def all_concrete_items(self) -> [ConcreteProductItem]:
        cur.execute("select * from foodp_concrete_items")
        return [ConcreteProductItem(**item) for item in cur.fetchall()]
        pass

    def all_purchases(self) -> [Purchase]:
        pass

    # ~ Add

    def add_concrete_item(self, item: ConcreteProductItem):
        pass

    def add_abstract_item(self, item: AbstractProductItem):
        pass

    def add_purchase(self, purchase: Purchase):
        pass

    def add_store(self, store: Store):
        pass

    def all_items(self):
        cur.execute("select id, name, metric, measure, measurement from foodp_items")
        return cur.fetchall()

    def add_item(self, name, metric, measurement=None, measure=None):
        print(name, metric, measurement, measure)

        log("Adding new item " + name)
        cur.execute("insert into foodp_items (name,metric,measure,measurement) values (%s,%s,%s,%s)",
                    (name, metric, measure, measurement))
        print(name, metric, measurement, measure)
        conn.commit()


d = MySQLDatabase()

print(d.all_concrete_items()[0].__dict__)
