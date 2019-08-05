import colorsys

### Abstraction for colors in different color spaces 
class Color:
    def __init__(self):
        self.hsv_tuple = (0, 0, 0)

    def set_rgb(self, r, g, b):
        self.hsv_tuple = colorsys.rgb_to_hsv(r,g,b)

    def set_hsv(self, h, s, v):
        self.hsv_tuple = (h,s,v)

    def get_hsv(self):
        return self.hsv_tuple

    def get_rgb(self):
        return colorsys.hsv_to_rgb(*self.hsv_tuple)

    # concise getters 
    def hue(self):
        return self.hsv_tuple[0]

    def sat(self):
        return self.hsv_tuple[1]

    def val(self):
        return self.hsv_tuple[2]
