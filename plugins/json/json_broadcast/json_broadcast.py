#!/usr/bin/env python
#
#   Copyright (c) 2016 In-Q-Tel, Inc, All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
JSON Parser Plugin
Breaks a CSV file down into a series of messages, one for each row.
Created on 28 October 2016
@author: Peter Bronez
"""

import pika
import sys
import json


def get_path():
    """Get the path to the input file provided by Vent"""
    path = None
    try:
        path = sys.argv[1]
    except:
        print("no path provided, quitting.")
    return path


def connections():
    """Handle connection setup to rabbitmq service"""
    channel = None
    connection = None
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='rabbitmq'))
        channel = connection.channel()

        channel.exchange_declare(exchange='topic_recs', type='topic')
    except:
        print("unable to connect to rabbitmq, quitting.")
    return channel, connection


def run_tool(path):
    """Tool entry point"""

    routing_key = "json_broadcast" + path.replace("/", ".")

    with open(path) as jsonfile:
        print("Parsing JSON file...")

        # This pure Python implementation could be replaced with a more robust parser
        reader = json.load(jsonfile)

        # File must be formatted as a list of JSON objects to be valid
        if type(reader) != list:
            raise TypeError('JSON file is not formatted as a list.')

        channel, connection = connections()

        for item in reader:
            message = json.dumps(item)
            channel.basic_publish(exchange='topic_recs', routing_key=routing_key, body=message)
            print(" [x] Sent {1}:{2}".format(routing_key, message))

if __name__ == '__main__':
    path = get_path()
    if path:
        run_tool(path)
