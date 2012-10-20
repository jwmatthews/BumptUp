#!/usr/bin/env python

# TODO:
# - Add support for CCs
# - Revisit 'undisclosed recipients'

import networkx
from optparse import OptionParser

from models import Message

import base

def generate_graph(msgs):
    graph = networkx.MultiDiGraph()
    for m in msgs:
        source_addr = m.get_from()
        for target_addr in m.get_to():
            graph.add_edge(source_addr, target_addr, subject=m.get_subject(), date=m.get_date())
    return graph

def print_graph(graph):
    # print edges with message subject
    for (u,v,d) in graph.edges_iter(data=True):
        print("From: %s To: %s Subject: %s, Date: %s" % (u,v,d["subject"], d["date"]))

def display_graph(graph, num_iterations=0):
    try:
        from matplotlib import pyplot
    except:
        print "Unable to import matplotlib.pyplot"
        return
    pos = networkx.spring_layout(graph, iterations=num_iterations)
    networkx.draw(graph,pos,node_size=0,alpha=0.4,edge_color='r',font_size=8)
    pyplot.savefig("enron_email.png")
    pyplot.show()

def write_graph(graph):
    pass


if __name__ == "__main__":
    parser = OptionParser(description="Generate a graph from email data")
    parser.add_option("--limit", action="store", help="Limit number of messages to parse", default=50)
    (opts, args) = parser.parse_args()
    limit = int(opts.limit)
    # Build a graph in networkX of all of the email data in the database
    base.init()
    msgs = Message.objects().limit(limit)
    graph = generate_graph(msgs)
    display_graph(graph)
    print_graph(graph)
    write_graph(graph)
