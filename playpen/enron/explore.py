#!/usr/bin/env python
from optparse import OptionParser
from models import Message
import base
import graph

def display_froms():
    email_authors = Message.objects().distinct(field="from_str")

    for x in email_authors[:25]:
        print x
    print "%s unique email authors" % (len(email_authors))

def display_from(email_addr):
    emails = Message.objects(from_str=email_addr).all()
    count = emails.count()
    print "%s emails found authored by '%s'" % (count, email_addr)
    g = graph.generate_graph(emails)
    graph.display_graph(g)

if __name__ == "__main__":
    base.init()
    parser = OptionParser(description="Explore the data")
    parser.add_option("--email", action="store", help="Generate graph focused on this email address", default=None)
    (opts, args) = parser.parse_args()
    if opts.email:
        display_from(opts.email)
    else:
        display_froms()