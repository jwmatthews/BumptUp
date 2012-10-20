#!/usr/bin/env python

# Info:
# - First attempt created an edge between "To" and "From" for all messages
#   this generated on the order of ~360k nodes, and a graph with ~1200 weakly connected components
#   Visualizing the data through Gephi was not helpful, there was too much data.  Want to refine what we look at.
#
#TODO:
#   - Filter on time, so we look at a weekly snapshot
#   - Filter so we are only looking at @enron email addresses
#   - Create a network per, "From" and analyze.
#     - Count highest edge weights
#     
# Future Improvements:
# - Add support for CCs
# - Revisit 'undisclosed recipients'
# - We are currently storing 'subject' on each edge, this might not make sense
# - How we handle time?

import networkx
import time
from optparse import OptionParser

from models import Message

import base

def generate_graph(msgs):
    graph = networkx.MultiDiGraph()
    for index, m in enumerate(msgs):
        if index % 5000 == 0:
            print "Processed %s messages"  % (index)
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

def write_graph(graph, filename):
    networkx.write_gexf(graph, filename, prettyprint=True)


if __name__ == "__main__":
    # Build a graph in networkX of all of the email data in the database
    base.init()
    #
    # Get Command Line Options
    #
    parser = OptionParser(description="Generate a graph from email data")
    parser.add_option("--limit", action="store", help="Limit number of messages to parse", default=0)
    parser.add_option("--display", action="store_true", help="Display a png graph, only useful for small number of messages")
    parser.add_option("--dump", action="store_true", help="Dump a textual listing of each edge ('message') to console")
    parser.add_option("--name", action="store", help="Output filename for graph in gexf format",
        default="enron_email_graph.gexf")
    (opts, args) = parser.parse_args()
    #
    # Fetch messages
    #
    start = time.time()
    msgs = Message.objects()
    limit = int(opts.limit)
    if limit > 1:
        msgs = msgs.limit(limit)
    graph = generate_graph(msgs)
    b_time = time.time()

    print "Finished generating graph for %s messages in %s seconds" % (len(msgs), b_time-start)
    if opts.display and limit < 500:
        display_graph(graph)
    if opts.dump:
        print_graph(graph)

    c_time = time.time()
    write_graph(graph, opts.name)
    end = time.time()
    print "Finished writing graph in GEXF format in %s seconds" % (end - c_time)
    print "All processing took %s seconds" % (end - start)
