#!/usr/bin/env python

# Base file responsible for setting up database connections
from mongoengine.connection import connect
DB = None

def init():
    global DB
    connect("enron", alias="enron")
    DB = connect("bumptup")

def drop_database():
    db = connect("bumptup")
    db.drop_database("bumptup")
