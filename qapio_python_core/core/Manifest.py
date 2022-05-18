import json
import os
import sys

INPUT_STREAMS = 'inputStreams'
OUTPUT_STREAMS = 'outputStreams'
GRAPH_ID = 'processId'


class Manifest:

    def __init__(self, raw):
        self.__raw = raw

    @property
    def graph_id(self):
        return self.__raw[GRAPH_ID]

    @property
    def input_streams(self):
        return self.__raw[INPUT_STREAMS]

    @property
    def output_streams(self):
        return self.__raw[OUTPUT_STREAMS]


def load_qapio_manifest():
    # Receive the manifest for the standard input
    # This is an instance of "PythonQapioManifest"
    # serialized to JSON.
    # Qapio provides the manifest through the standard
    # input, binary serialized.

    # The first bytes contain the length
    # of the manifest
    filename = sys.argv[ 1 ]

    manifest = json.loads(
        filename
    )

    #print("loaded python manifest", manifest)

    return Manifest(manifest)
