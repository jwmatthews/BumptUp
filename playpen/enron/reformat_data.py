#!/usr/bin/env python
import time
import dateutil.parser
from optparse import OptionParser


from models import OriginalMessage, Message
import base

def process_messages(limit):
    count = 0
    date_parser = dateutil.parser.parser()
    omsgs = OriginalMessage.objects()
    if limit:
        omsgs = omsgs.limit(limit)
    for raw_count, om in enumerate(omsgs):
        m = Message()
        m.body = om.body
        m.subFolder = om.subFolder
        m.filename = om.filename
        m.headers = om.headers
        m.subject = om.get_subject()
        m.date = date_parser.parse(om.get_date())
        m.to = [x for x in om.get_to() if "enron.com" in x]
        if not m.to:
            # Skip if none of the "To's" are to enron employees
            continue
        m.from_str = om.get_from()
        if "enron.com" not in m.from_str:
            # Skip if this email was not from an enron employee
            continue
        try:
            m.save()
        except Exception, e:
            print "Error trying to save: %s" % (m)
            print e
        count+=1
        if count % 5000 == 0:
            print "Processing %s raw messages, filtered to %s" % (raw_count, count)
    return count

if __name__ == "__main__":
    base.drop_database()
    base.init()
    parser = OptionParser(description="Generate a graph from email data")
    parser.add_option("--limit", action="store", help="Limit number of messages to parse", default=0)
    (opts, args) = parser.parse_args()
    limit = int(opts.limit)
    start = time.time()
    count = process_messages(limit=limit)
    end = time.time()
    print "%s objects saved in %s seconds" % (count, end-start)