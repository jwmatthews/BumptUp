#!/usr/bin/env python

# Define MongoEngine Model for Email set
from mongoengine import Document, StringField, DictField

class Message(Document):
    meta = {
        'collection': 'messages',
        'allow_inheritance': False  # Needed to read existing data not created with mongoengine
    }
    body = StringField()
    subFolder = StringField()
    filename = StringField()
    headers = DictField()

    def __str__(self):
        hdrs = {}
        desired_headers = ["To", "From", "Subject", "Date"]
        for key in desired_headers:
            if self.headers.has_key(key):
                hdrs[key] = self.headers[key]
        return "Message with headers: %s and a body of %s bytes" % (hdrs, len(self.body))



if __name__ == "__main__":
    from mongoengine.connection import connect
    db = connect("enron")
    msgs = Message.objects()
    print "Found %s messages" % (msgs.count())
    for x in range(0, 3):
        print "\t%s" % (msgs[x])


