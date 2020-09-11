#!/usr/bin/env python


import socket
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from splunklib.client import connect
import splunklib.results as results
import utils

def get_data(response):
    reader = results.ResultsReader(response)
    for result in reader:
        for key, value in result.items():
                print key + "=" + value, 
        print


def main():
    usage = "ugh. always asking for help. just run the python script. no arguments needed."
    opts = utils.parse(sys.argv[1:], {}, ".splunkrc", usage=usage)
    if len(opts.args) != 0:
        utils.error("Ummm...... no arguments are needed.", 2)

    search = """
             search index=_audit action="login attempt" earliest=-7d
             | eval src=coalesce(clientip, src),
                    timestamp=strftime(_time,"%m-%d-%Y %H:%M:%S")
             | rename info as status
             | table timestamp user status src
             """

    try: 
        service = connect(**opts.kwargs)

        socket.setdefaulttimeout(None)
        response = service.jobs.oneshot(search)

        get_data(response)

    except ImportError:
        from splunklib.ordereddict import OrderedDict    

if __name__ == "__main__":
    main()
