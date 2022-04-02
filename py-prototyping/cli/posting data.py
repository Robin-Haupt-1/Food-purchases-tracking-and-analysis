from mine.utils.logging import Logging
from mine.imports import *
import traceback

import requests

ob = {
    "abstractItemID": 5,
    "name": "uiaui",
    "brand": "None",
    "measurement": 500,
    "store_specific": True,
    "storeID": 6
}

ob1 = {
    "name": "test",
    "metric": "ntia",
    "ID": 555
}

purchase_object = {"date": "2022-04-01",
                   "storeID": 1,
                   "cost": 123,
                   "abstractItemID": 2,
                   "measurement": 500
                   }

x = requests.post('http://10.28.4.2:1241/purchases/add',
                  data=json.dumps(purchase_object),
                  headers={'Content-Type': 'application/json'})

print(x.text)
