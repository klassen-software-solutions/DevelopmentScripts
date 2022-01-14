#!/usr/bin/env python3

# Subscribe to an MQTT message, which should be containing JSON, and pretty print it.

# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
#   Justification: Don't care about docstrings in this little utility.

import argparse
import json
import signal
import threading

import paho.mqtt.client as mqtt

# pylint: disable=consider-using-with
#   Justification: Cannot use with in this context

waiter = threading.Lock()
waiter.acquire()

def _signal_handler(_sig, _frame):
    waiter.release()


class MQTTListener():
    # pylint: disable=too-few-public-methods
    #   Justification: Really only need the one

    def __init__(self, host, port, topic):
        self._client = self._init_client()
        self._topic = topic
        self._client.connect_async(host, port)
        self._client.loop_start()

    def stop(self):
        self._client.loop_stop()

    def _init_client(self):
        client = mqtt.Client()
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        return client

    def _on_connect(self, client, _userdata, _flags, _rc):
        client.subscribe(self._topic)

    @staticmethod
    def _on_message(_client, _userdata, msg):
        try:
            payload = {}
            if len(msg.payload) > 0:
                payload = json.loads(msg.payload)
            print(json.dumps(payload, indent=2, sort_keys=True))
        except json.decoder.JSONDecodeError:
            print("Could not decode payload as JSON, ignoring message")


def _parse_command_line(args: list):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost', type=str, help='MQTT host')
    parser.add_argument('--port', default=1883, type=int, help='MQTT port')
    parser.add_argument('topic', type=str, help='Topic to subscribe')
    return parser.parse_args(args)

def run(args: list = None):
    options = _parse_command_line(args)
    print(f"Listening for '{options.topic}'...")
    listener = MQTTListener(options.host, options.port, options.topic)

    # Wait for a cntr-c
    try:
        signal.signal(signal.SIGTERM, _signal_handler)
        signal.signal(signal.SIGINT, _signal_handler)
        waiter.acquire()
    except KeyboardInterrupt:
        waiter.release()

    listener.stop()

run()
