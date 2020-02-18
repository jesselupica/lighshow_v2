from __future__ import division

from collections import deque
import numpy as np
import math
import time
import random
from stream import Stream, STREAM_RATE, CHUNK_SIZE
from Color import Color
from StreamProcessorBase import StreamProcessorBase
from Transforms import WindowedRangeTransformer, ValueChaser

HUE_SHIFT_MULTIPLIER = 2

SAT_CHASER_MULTIPLIER = 0.015

VALUE_AVG_AMOUNT = 7
VALUE_PULL_RATE_S = 0.002 # Hold this value

HIT_INTENSITY = 0.0

HISTORY_DURATION_S = 2  

SLEEP_MAX = 3000

MAX_VALUE_FALL_SPEED_S = 0.2

MIN_HIT_MULTIPLIER = 1.5142857

MIN_BRIGHTNESS = 0 # out of 255
delay = 0.42857


def val_for_chunk(rate, chunk_size, stream_rate):
    return rate * chunk_size / stream_rate

# Enum
class LightModes:
    VisualizeMusic = 'VISUALIZE_MUSIC'
    StaticColor = 'STATIC_COLOR'
    Fade = 'FADE'
    Asleep = 'ASLEEP'
    Off = 'OFF'
    CustomStaticColor = 'CUSTOM_STATIC_COLOR'

class StreamAnalyzer:
    def __init__(self, history_duration_s):
        max_len = int(history_duration_s * STREAM_RATE / CHUNK_SIZE)
        self.energy_history = deque([], maxlen=max_len)
        self.sleep_history = deque([], maxlen=5*max_len)
        self.curr_intensity = 0
        self.last_hit = time.time()
        self.is_hit = None
        self.hit_mag = None

    def analyze(self, block):
        rl_sum = 0 
        for r, l in zip(block[::2], block[1::2]):
            rl_sum += abs(r) + abs(l)
        self.energy_history.append(rl_sum)
        self.sleep_history.append(rl_sum)
        self.curr_intensity = rl_sum

        avg = sum(self.energy_history)/len(self.energy_history)
        # var = np.var(np.array(self.energy_history))
        time_since_last_hit = time.time() - self.last_hit
        rest_interval_complete = time_since_last_hit > delay
        is_loud = self.curr_intensity > MIN_HIT_MULTIPLIER * avg
        self.is_hit = is_loud and rest_interval_complete

        if self.is_hit:
            self.last_hit = time.time()
            self.hit_mag = self.curr_intensity / avg

    def get_intensity(self):
        max_intensity = max(self.energy_history)
        if max_intensity is 0:
            return 0
        return self.curr_intensity / max_intensity

    def should_sleep(self):
        return max(self.sleep_history) < SLEEP_MAX


class RhythmBasedStreamProcessor(StreamProcessorBase):    
    def __init__(self):
        self.desired_hue = 0
        self.desired_sat = 1
        
        self.light_intensity_chaser = ValueChaser(VALUE_AVG_AMOUNT, MAX_VALUE_FALL_SPEED_S * CHUNK_SIZE / STREAM_RATE)
        self.light_intensity_transformer = WindowedRangeTransformer(VALUE_PULL_RATE_S * CHUNK_SIZE / STREAM_RATE)
        self.stream_analyzer = StreamAnalyzer(HISTORY_DURATION_S)
        self.mode_override = None
        self.color = Color()

    def preprocess(self, input_stream):
        self.stream_analyzer.analyze(input_stream)

    def process(self, input_stream):
        if self.mode_override is not None:
            return self.mode_override.get_values()
        hue, saturation, value = self.color.get_hsv()
        intensity = self.stream_analyzer.get_intensity()
        
        hue_diff = self.desired_hue - self.color.hue()
        if abs(hue_diff) > 0.5:
            hue_diff = -1 * np.sign(hue_diff) * (1 - abs(hue_diff))
        hue += hue_diff * 0.1 * intensity

        sat_diff = self.desired_sat - saturation
        saturation += sat_diff * SAT_CHASER_MULTIPLIER

        if self.stream_analyzer.is_hit:
            mag = self.stream_analyzer.hit_mag
            desired_color = (random.uniform(0, 1), 1)
            self.desired_hue = desired_color[0]
            self.desired_sat = desired_color[1]
            self.light_intensity_chaser.bump(HIT_INTENSITY)

        # bounds check
        self.desired_hue %= 1.0

        value = self.light_intensity_transformer.transform(self.light_intensity_chaser.update(intensity))
        h, s, v = self.bounds_check(hue, saturation, value)

        self.color.set_hsv(h, s, v)
        return self.color.get_rgb()

    def bounds_check(self, hue, saturation, value):
       hue %= 1.0
       saturation = min(saturation, 1)
       saturation = max(saturation, 0)
       value = min(value, 1)
       value = max(value, 0)
       return hue, saturation, value

