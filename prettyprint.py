#!/usr/bin/env python3

"""Utility to pretty print an input."""

import sys
import json

def pretty_print(input_stream, output_stream):
    """Pretty print the input stream onto the output stream.

       This will attempt to recognize the input stream as JSON. If that fails the
       input will simply be echoed to the output as is.
    """
    text = input_stream.read()
    try:
        json.dump(json.loads(text), output_stream, indent=2, sort_keys=True)
        output_stream.write('\n')
    except json.JSONDecodeError:
        output_stream.write(text)

if __name__ == '__main__':
    pretty_print(sys.stdin, sys.stdout)
