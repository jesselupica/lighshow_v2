from Color import Color 

class StreamProcessorBase(object):
    def __init__(self, history_duration_s, stream_rate, stream_chunk_size):
        self.color = Color()
        self.stream = None
        self.mode_override = None

    def add_input_stream(self, stream):
        self.stream = stream
        
    def process(self, raw_input):
        raise NotImplemented()

    def preprocess(self, raw_input):
        pass

    def should_sleep(self):
        return max(self.sleep_history) < SLEEP_MAX


    # def get_state(self):
    #     interface_fade_speed = (self.fade_speed - self.fade_speed_range[0]) / (self.fade_speed_range[1] - self.fade_speed_range[0]) 
    #     return {'hue': self.hue, 'saturation': self.saturation, 
    #             'value':self.value, 'mode': self.mode, 
    #             'is_asleep':self.mode == LightModes.Asleep, 'fade_speed' : interface_fade_speed}