#!/usr/bin/env python

# Define MongoEngine Model for Email set
from mongoengine import Document, StringField, DictField

class Message(Document):
    meta = {
            'db_alias': 'messages'
            }
    body = StringField()
    subFolder = StringField()
    filename = StringField()
    headers = DictField()



if __name__ == "__main__":
    from mongoengine.connection import connect
    db = connect("enron_email")
    print "Found %s messages" % (Message.objects().count())
    print "First message: \n\t%s" % (Message.objects()[0])


