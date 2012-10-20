#!/usr/bin/env python

# Base file responsible for setting up database connections
from mongoengine.connection import connect
DB_NAME = "enron"
DB = None

def init(db_name=None):
    global DB
    if not db_name:
        db_name = DB_NAME
    DB = connect("enron")
    return DB
