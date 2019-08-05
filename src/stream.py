from sys import byteorder
from array import array
import wave
import pyaudio

STREAM_RATE = 44100
CHUNK_SIZE = 1024

class Stream(object):
    def __init__(self):
        p = pyaudio.PyAudio()
        self.input_stream = p.open(format=pyaudio.paInt16, channels=1, rate=STREAM_RATE,
                            input=True,
                            frames_per_buffer=CHUNK_SIZE)

    def get_chunk(self):
        try:
            sound_data = array('h', self.input_stream.read(CHUNK_SIZE))
            if byteorder == 'big':
              	 sound_data.byteswap()
            return sound_data
        except IOError as e:
            return None
	    

class FileStream(Stream):
    def __init__(self, file_name, rate=STREAM_RATE, chunk_size=CHUNK_SIZE):
        self.CHUNK_SIZE = chunk_size
        self.RATE = rate
        p = pyaudio.PyAudio()
        self.wf = wave.open(file_name, mode='rb')
        self.output_stream = p.open(format =
                p.get_format_from_width(self.wf.getsampwidth()),
                channels = self.wf.getnchannels(),
                rate = self.wf.getframerate(),
                output = True) 

    def get_chunk(self):
        try:
            data = self.wf.readframes(self.CHUNK_SIZE)
            sound_data = array('h', data)
            self.output_stream.write(data)
            return sound_data
        except IOError as e:
           return None
