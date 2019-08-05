

class ValueChaser:
    def __init__(self, chaser_speed, max_fall_speed=None):
        self.value = 0
        self.desired_value = 0;
        self.chaser_speed = chaser_speed
        self.max_fall_speed = max_fall_speed

    def update(self, new_desired_value):
        self.desired_value = new_desired_value
        chaser_value = (self.desired_value - self.value) / self.chaser_speed
        print("cv", chaser_value, self.value)
        if self.max_fall_speed is not None and chaser_value < self.value:
            print(self.value - chaser_value)
            diff = self.value - chaser_value
            rate_limited_diff = min(self.max_fall_speed, diff)
            chaser_value = self.value - rate_limited_diff
        self.value = chaser_value
        return self.value 


    def bump(self, desired_value_delta):
        self.desired_value += desired_value_delta


class WindowedRangeTransformer:
    def __init__(self, pull, transform_minimum=0, transform_maximum=1):
        self.min = transform_minimum
        self.max = transform_maximum
        self.pull = pull
        self.window_min = 0
        self.window_max = 0.1

    def transform(self, value):
        self.window_max = max(self.window_max, value)
        self.window_min = min(self.window_min, value)
        self.window_min = max(self.window_min, 0)
        zero_to_one_transform = (value - self.window_min) / (self.window_max - self.window_min)

        self.window_max -= self.pull
        self.window_min += self.pull
        return (zero_to_one_transform + self.min) * (self.max - self.min)


        