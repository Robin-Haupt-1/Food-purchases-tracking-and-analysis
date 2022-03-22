import requests
from mine.utils.strings import string_to_filename
from mine.utils.files import load_json
from mine.private import mysql_cred_localhost
import os
from mine.imports import *
import flask
from flask import Flask, request
import datetime
import pickle
from database import *

app = Flask(__name__)

import json
import random
from dataclasses import dataclass

db = MySQLDatabase(Tables, conn)


def make_response_from_list(response):
    if type(response) == list:
        response = [item.__dict__ for item in response]
    response = flask.make_response(json.dumps(response, indent=4))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/stores/all")
def get_all_stores():
    return make_response_from_list(db.get_all_stores())


@app.route("/items/concrete/all")
def get_all_concrete_items():
    return make_response_from_list(db.get_all_concrete_items())


@app.route("/items/abstract/all")
def get_all_abstract_items():
    return make_response_from_list(db.get_all_abstract_items())

@app.route("/purchases/all")
def get_all_purchases():
    return make_response_from_list(db.get_all_purchases())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1241)
