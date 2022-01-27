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

app = Flask(__name__)

import json
import random
from dataclasses import dataclass
import mysql.connector

conn = mysql.connector.connect(
    **mysql_cred_localhost, database="meta")
cur = conn.cursor()



class Main:
    def __init__(self):
        """"""


t = Main()



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1236)
