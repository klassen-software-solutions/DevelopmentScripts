#!/usr/bin/env python3

"""Utility to pretty print an input"""

import argparse
import json
import sys

def pretty_print(input_stream, output_stream, error_stream=None) -> bool:
    """Pretty print the input stream onto the output stream

       This will attempt to recognize the input stream as JSON. If that fails the
       input will simply be echoed to the output as is.

       Returns True if the input was valid and False if it was not.

       Parameters
       ----------
       input_stream: The input stream
       output_stream: The output stream. If None then no output will be written.
       error_stream: The error stream. If there are validation errors they will be sent
            here. If None (the default) then the errors will not be written.
    """
    text = input_stream.read()
    try:
        json_obj = json.loads(text)
        if output_stream is not None:
            json.dump(json_obj, output_stream, indent=2, sort_keys=True)
            output_stream.write('\n')
        return True
    except json.JSONDecodeError as err:
        if output_stream is not None:
            output_stream.write(text)
        if error_stream is not None:
            print(f"Error: {err}", file=error_stream)
        return False

# MARK: Main Entry Point

def _parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Return an error code if the input is not valid")
    parser.add_argument(
        "--show-errors",
        action="store_true",
        help="If the validation fails, write the error to the standard error device"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Perform the validation only but writing nothing to the standard output device"
    )
    return parser.parse_args()

def _main():
    args = _parse_command_line()
    output_stream = None if args.quiet else sys.stdout
    error_stream = sys.stderr if args.show_errors else None
    ret = pretty_print(sys.stdin, output_stream, error_stream)
    if (args.validate or args.show_errors) and (not ret):
        sys.exit(1)

if __name__ == '__main__':
    _main()
