#!/usr/local/bin/python3
import sys
import pyaudio
import traceback
import wave

from stream import Stream

arg_prompt = '''
Please specify mode: record | playback
For playback specify a file to playback
e.g. 
python streamTester.py record
python streamTester.py playback test.wav
'''

WAVE_OUTPUT_FILENAME = "songs/low_quality.wav"

def record():
    stream = Stream()    
    try:
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(1)
        waveFile.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        waveFile.setframerate(44100)

        while True:
            raw_data = stream.get_chunk()
            waveFile.writeframes(raw_data)

    except KeyboardInterrupt:
        print("Shutting down!")
        waveFile.close()

        sys.exit(0)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
            

def playback(filename):
    pass

if __name__ == '__main__':
    if len(sys.argv) not in range(2,4):
        print(arg_prompt)
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "record":
        record()
    elif mode == "playback":
        playback(sys.argv[2])
    else:
        print("Bad argument: ", mode)
        print(arg_prompt)
        sys.exit(1)