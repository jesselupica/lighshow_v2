#! /usr/bin/env python3

import sys
import os
import threading
import importlib
import argparse

from PiGPIOPinOutputSource import PiGPIOPinOutputSource
from StreamProcessorBase import StreamProcessorBase
from Visualizer import Visualizer
from stream import Stream, FileStream
from CircleAnalyzerOutputSource import CircleAnalyzerOutputSource

parser = argparse.ArgumentParser(description='Lightshow is a music visualization program for Raspberry Pi')

#parser.add_argument('song', help="The song to play if you are in dev mode", type=str, optional=True)
parser.add_argument('-p', '--stream-processor', help="The stream processor to use to visualize the music", type=str, default="RhythmBasedStreamProcessor")

def is_pi():
    return os.uname()[1] == 'raspberrypi'

def get_stream_processor(processor_name):
    module = importlib.import_module(processor_name)
    class_ = getattr(module, processor_name)
    assert issubclass(class_, StreamProcessorBase), (
        "Manually specified stream processors must be a subclass of"
        " StreamProcessorBase and must be defined in the file lightshow_v2/src/<processor_name>.py"
        )
    return class_()

if __name__ == '__main__':
    args = parser.parse_args()
    print("Starting Lightshow!")
    
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")

    visualizer = Visualizer()
    stream_processor = get_stream_processor(args.stream_processor)

    visualizer.add_stream_processor(stream_processor)

    if is_pi():
        visualizer.add_input_source(Stream())
        visualizer.add_output_source(PiGPIOPinOutputSource())

    else: 
        # if len(sys.argv) < 2:
        #     print("Not enough arguments. When using in dev mode, you must specify an input file!")
        #     sys.exit(1)
        visualizer.add_input_source(Stream())
        visualizer.add_output_source(CircleAnalyzerOutputSource())
    visualizer.run()
    print("Ending Lightshow!")
