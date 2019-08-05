#! /usr/bin/env python3

import sys
import os
import threading

from PiGPIOPinOutputSource import PiGPIOPinOutputSource
from RhythmBasedStreamProcessor import RhythmBasedStreamProcessor
from Visualizer import Visualizer
from stream import Stream, FileStream
from CircleAnalyzerOutputSource import CircleAnalyzerOutputSource

def is_pi():
    return os.uname()[1] == 'raspberrypi'

if __name__ == '__main__':
    print("Starting Lightshow!")
    
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")

    visualizer = Visualizer()
    visualizer.add_stream_processor(RhythmBasedStreamProcessor())

    if is_pi():
        visualzer.add_input_source(Stream())
        visualizer.add_output_source(PiGPIOPinOutputSource())

    else: 
        if len(sys.argv) < 2:
            print("Not enough arguments. When using in dev mode, you must specify an input file!")
            sys.exit(1)
        visualizer.add_input_source(FileStream(sys.argv[1]))
        visualizer.add_output_source(CircleAnalyzerOutputSource())
    visualizer.run()
    print("Ending Lightshow!")
