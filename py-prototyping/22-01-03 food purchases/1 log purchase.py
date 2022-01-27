import os
from mine.imports import *
import flask
from flask import Flask, request
from mine.private import mysql_cred_localhost
import datetime
import pickle

app = Flask(__name__)
from mine.utils.logging import Logging
import json
import random
from dataclasses import dataclass
import mysql.connector

log = Logging("Meta Purchases").log

conn = mysql.connector.connect(**mysql_cred_localhost, database="meta")
cur = conn.cursor(dictionary=True)

ps = [{"store": "1", "items": [{"name": "Knollensellerie", "weight": 0.918, "cost": 0.91},
                               {"name": "Orangen", "weight": 1.494, "cost": 3.42},
                               {"name": "Paprika rot", "weight": 0.776, "cost": 1.47},
                               {"name": "Bananen", "weight": 0.746, "cost": 0.66},
                               {"name": "Bananen", "weight": 0.93, "cost": 0.83},
                               {"name": "Möhren 2000g", "amount": 1, "cost": 0.79},
                               {"name": "Knoblauchsäckchen", "amount": 1, "cost": 0.99},
                               {"name": "Grapefruit", "amount": 1, "cost": 0.59},
                               {"name": "Blaubeeren gefroren 500g", "amount": 1, "cost": 3.49},
                               {"name": "Früchtemüsli 1000g", "amount": 2, "cost": 3.18},
                               {"name": "Haselnüsse natur 200g", "amount": 1, "cost": 2.79},
                               {"name": "Arriba Edelcacao Schokolade 85% 125g", "amount": 2, "cost": 2.18},
                               {"name": "Datteln ohne Stein Schale 250g", "amount": 3, "cost": 4.47}
                               ], "date": "2022-01-03"},
      {"store": "11", "items": [{"name": "Ostmann Cayenne-Pfeffer gemahlen Beutel 40g", "amount": 1, "cost": 1.99},
                                ], "date": "2022-01-04"},
      {"store": "1", "items": [{"name": "Zwiebeln rot 1000g", "amount": 1, "cost": 1.59},
                               {"name": "Zwiebeln gelb 2000g", "amount": 1, "cost": 1.19},
                               {"name": "Möhren 2000g", "amount": 1, "cost": 0.79},
                               {"name": "Hefe 42g", "amount": 2, "cost": 0.18},
                               {"name": "Blutorangen 1500g", "amount": 1, "cost": 1.99},
                               ], "date": "2022-01-05"},
      {"store": "10", "items": [{"name": "Duru Iri Nohut 1000g", "amount": 1, "cost": 3.79},
                                {"name": "Dere Kidney Fasulye 1000g", "amount": 2, "cost": 6.98},
                                {"name": "Sere Seker Fasulye 1000g", "amount": 2, "cost": 5.38},
                                ], "date": "2022-01-05"},
      {"store": "3", "items": [{"name": "Ja Müsli Früchte 1000g", "amount": 1, "cost": 1.79},
                               {"name": "Ostmann Paprika rosenscharf 50g", "amount": 1, "cost": 1.99},
                               {"name": "REWE Bio Kokosmilch 400ml", "amount": 3, "cost": 5.07},
                               {"name": "REWE Beste Wahl Currypaste grün 110g", "amount": 1, "cost": 1.29},
                               ], "date": "2022-01-05"},
      {"store": "3", "items": [{"name": "Rote Bete", "weight": 0.234, "cost": 0.28}

                               ], "date": "2022-01-05"},  {"store": "5", "items": [{"name": "Enerbio Sojamilch 1000ml", "amount":2, "cost":1.98},
], "date": "2022-01-10"}]
"""
      
      {"store": "", "items": [{"name": "", "amount":, "cost":},
{"name": "", "amount":, "cost":},
{"name": "", "amount":, "cost":},
{"name": "", "amount":, "cost":},
{"name": "", "amount":, "cost":},
{"name": "", "amount":, "cost":},
{"name": "", "amount":, "cost":},
{"name": "", "weight":, "cost":},
{"name": "", "weight":, "cost":},
{"name": "", "weight":, "cost":},
{"name": "", "weight":, "cost":},
{"name": "", "weight":, "cost":},
{"name": "", "weight":, "cost":},
{"name": "", "weight":, "cost":},

], "date": ""}
"""

for p in ps:
    print(f'Total Cost: {sum([i["cost"] for i in p["items"]])}')


# 4 types of items: fixed weight, only amount / only weight

class LogPurchaseToMySQL:
    def __init__(self):
        """"""
        testing_purchase = {"store": "3", "items": [
            {"store specific": True, "metric": "amount", "measure": "g", "measurement": 110, "new": True,
             "name": "REWE Beste Wahl Currypaste grün", "amount": 1,
             "cost": 1.29},
            {"store specific": True, "metric": "weight", "new": True, "name": "Paprika rot", "weight": 0.776,
             "cost": 1.47},
            {"store specific": False, "metric": "weight", "new": True, "name": "Rote Bete", "weight": 0.234,
             "cost": 0.28},
            {"store specific": True, "metric": "amount", "measure": "ml", "measurement": 400, "new": True,
             "name": "REWE Bio Kokosmilch", "amount": 3, "cost": 5.07}, ],
                            "date": "2022-01-05"}
        self.add_purchase(testing_purchase)

    def add_purchase(self, purchase: dict):
        """integrate purchases from above array"""
        p = purchase
        print(p)

        for it in p["items"]:
            """Introduce new items to db"""
            if it["new"]:
                log("Adding new item " + it["name"])
                if it["metric"] == "weight":
                    cur.execute("insert into foodp_items (name,store,metric,measure,measurement) values (%s,%s)",
                                (it["name"], p["store"] if it["store specific"] else None))

                else:
                    cur.execute("insert into foodp_items (name,store) values (%s,%s)",
                                (it["name"], p["store"] if it["store specific"] else None))

            pass
        # cur.execute("sele")
        conn.commit()

    def get_item(self, name: str, store: int):
        cur.execute("select * from foodp_items where name='aaa'")

class db:
    def __init__(self):
        """"""

    def all_stores(self):
        cur.execute("select id, name from foodp_stores")
        return cur.fetchall()

    def all_items(self):
        cur.execute("select id, name, metric, measure, measurement from foodp_items")
        return cur.fetchall()

    def add_item(self,name,metric,measurement=None,measure=None):
        print(name,metric,measurement,measure)

        log("Adding new item " + name)
        cur.execute("insert into foodp_items (name,metric,measure,measurement) values (%s,%s,%s,%s)",
                        (name, metric,measure,measurement))
        print(name,metric,measurement,measure)
        conn.commit()



d=db()
print(d.all_stores())
@app.route("/stores/all")
def all_stores():
    response = flask.make_response(json.dumps(d.all_stores()))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/items/add")
def add_item():
    name = request.args.get("name")
    metric = request.args.get("metric")
    measure = request.args.get("measure")

    if metric == "amount":
        measurement = request.args.get("measurement")
    else:
        measurement=None

    print(name, metric, measurement, measure)

    d.add_item(name,metric,measurement,measure)
    response = flask.make_response("success")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/items/all")
def all_items():
    response = flask.make_response(json.dumps(d.all_items()))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#m = LogPurchaseToMySQL()
#m.get_item("aae", 3)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=1240)
