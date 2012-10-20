#!/usr/bin/env python

# Define MongoEngine Model for Email set
from mongoengine import Document, StringField, DictField

import base

def strip_formatting_chars(input, to_strip=None):
    if not to_strip:
        to_strip = ['\n', '\r', '\t']
    if not input:
        raise Exception("Unable to strip data from None")
    return ''.join(x for x in input if x not in to_strip)

class Message(Document):
    meta = {
        'collection': 'messages',
        'allow_inheritance': False  # False is needed to read existing data not created with mongoengine
    }
    body = StringField()
    subFolder = StringField()
    filename = StringField()
    headers = DictField()

    def __generic_get(self, keys=None):
        for k in keys:
            if self.headers.has_key(k):
                return self.headers[k]

    def get_from(self):
        keys = ["From"]
        return self.__generic_get(keys)

    def get_to(self):
        keys = ["To", "X-To"]
        t = self.__generic_get(keys)
        if not t:
            return "undisclosed-recipients"
        try:
            t = strip_formatting_chars(t)
        except Exception, e:
            print "Caught exception processing: %s" % (self)
            print "Full headers are: %s" % (self.headers)
            raise
        return t.split(",")

    def get_date(self):
        keys = ["Date"]
        return self.__generic_get(keys)

    def get_subject(self):
        keys = ["Subject"]
        return self.__generic_get(keys)

    def __str__(self):
        hdrs = {}
        desired_headers = ["To", "From", "Subject", "Date"]
        for key in desired_headers:
            if self.headers.has_key(key):
                hdrs[key] = self.headers[key]
        return "Message with headers: %s and a body of %s bytes" % (hdrs, len(self.body))



if __name__ == "__main__":
    base.init()
    msgs = Message.objects()
    print "Found %s messages" % (msgs.count())
    for x in range(0, 3):
        print "\t%s" % (msgs[x])


