

class Color:
    def __init__(self, r: int = 255, g: int = 0, b: int = 0):
        for channel in [r, g, b]:
            if channel > 255 or channel < 0:
                raise ValueError("color values should between [0, 255]")
        self.r = r
        self.g = g
        self.b = b

    def to_str(self, add_rgb=False):
        if add_rgb:
            return f"rgb({self.r} {self.g} {self.b})"
        return f"{self.r} {self.g} {self.b}"

    @staticmethod
    def parse_from_str(in_c: str):
        c_str = in_c.lower().strip(" #()")
        if c_str.startswith("rgb"):
            c_str = c_str[3:].strip(" ()")
        if c_str.startswith("rgba"):
            c_str = c_str[4:].strip(" ()")
        res = []
        if len(c_str) == 6:
            res = [int(c_str[i:i + 2], 16) for i in (0, 2, 4)]
        else:
            c_str = c_str.replace(",", " ")
            for word in c_str.split(" "):
                if word.isnumeric():
                    if 0 <= int(word) <= 255:
                        res += [int(word)]
        if len(res) < 3:
            raise ValueError(
                f'ERROR: the color {in_c} could not parsed as color, please use HEX or "R,G,B" color format')
        return Color(res[0], res[1], res[2])