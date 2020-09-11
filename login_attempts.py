#!/usr/bin/env python


import socket
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from splunklib.client import connect
import splunklib.results as results
import utils

def get_data(response):
    reader = results.ResultsReader(response)
    
    # Running through results dictionary and making key value pairs
    for result in reader:
        for key, value in result.items():
                print key + "=" + value, 
        print


def main():
    # Adding color to the --help output
    usage = "ugh. always asking for help. just run the python script. no arguments needed."
    opts = utils.parse(sys.argv[1:], {}, ".splunkrc", usage=usage)
    if len(opts.args) != 0:
        utils.error("Ummm...... no arguments are needed.", 2)

    # Search to run and get all the login attempts in the last week
    # Note: The exercise asked to only display failed attempts but the output had successful attempts as well
    search = """
             search index=_audit action="login attempt" earliest=-7d
             | eval src=coalesce(clientip, src),
                    timestamp=strftime(_time,"%m-%d-%Y %H:%M:%S")
             | rename info as status
             | table timestamp user status src
             """

    # Making the connection to Splunk
    try:
        service = connect(**opts.kwargs)
        socket.setdefaulttimeout(None)
        response = service.jobs.oneshot(search)

    # Sending the output to definition to print to console
        get_data(response)
    except:
        print("Something went wrong while trying to connect. Do better.")
    

if __name__ == "__main__":
    main()
