import numpy as np


class Color:
    def __init__(self, r: int = 255, g: int = 0, b: int = 0):
        for channel in [r, g, b]:
            if channel > 255 or channel < 0:
                raise ValueError("color values should between [0, 255]")
        self.r = int(round(r, 0))
        self.g = int(round(g, 0))
        self.b = int(round(b, 0))

    def to_str(self, add_rgb=False):
        if add_rgb:
            return f"rgb({self.r},{self.g},{self.b})"
        return f"{self.r},{self.g},{self.b}"

    @staticmethod
    def parse_from_str(in_c: str):
        c_str = in_c.lower().strip(" #()")
        if c_str.startswith("rgb"):
            c_str = c_str[3:].strip(" ()")
        if c_str.startswith("rgba"):
            c_str = c_str[4:].strip(" ()")
        res = []
        if len(c_str) == 6 and "," not in c_str:
            res = [int(c_str[i:i + 2], 16) for i in (0, 2, 4)]
        else:
            c_str = c_str.replace(",", " ")
            for word in c_str.split(" "):
                if word.isnumeric():
                    if 0 <= int(word) <= 255:
                        res += [int(word)]
        if len(res) < 3:
            raise ValueError(
                f'ERROR: the color [{in_c}] could not parsed as color, please use HEX or "R,G,B" color format')
        return Color(res[0], res[1], res[2])


class ColorGradient:
    def __init__(self, descriptor: str):
        self.gradient_desc = []
        desc = descriptor.strip(" .,")
        raw_entries = desc.split(",")
        entries, cur_entry = [], ""
        # merge splits on the form of rgb(r, g, b)
        for entry in raw_entries:
            if cur_entry == "":
                if "(" in entry and ")" not in entry:
                    cur_entry = entry
                else:
                    entries.append(entry)
            else:
                cur_entry += "," + entry
                if ")" in entry:
                    entries.append(cur_entry)
                    cur_entry = ""
        # merge ended

        desc_example = f". Provided descriptor: '{descriptor}'. " \
                       f"An example of a good gradient descriptor: '#cc33ff 0%, #00ff99 30%, #ffcc00 100%'"
        if len(entries) < 2:
            raise ValueError("wrong format of color gradient descriptor, "
                             "it must contain at least 2 colors" + desc_example)
        for i, entry in enumerate(entries):
            words = list(filter(None, entry.strip().split(" ")))
            if len(words) != 2:
                raise ValueError(f"wrong format of color gradient descriptor, "
                                 f"error at entry num [{i + 1}]" + desc_example)
            try:
                color = Color.parse_from_str(words[0])
                percentage = float(words[1].strip("%")) / 100
            except ValueError:
                raise ValueError(f"wrong format of color gradient descriptor, "
                                 f"error at entry num [{i + 1}]" + desc_example)
            if i == 0:
                if percentage != 0:
                    raise ValueError("percentage of the first color must be equal to 0" + desc_example)
            else:
                if percentage <= self.gradient_desc[-1][1]:
                    raise ValueError("color percentages must be of an increasing order" + desc_example)
                if i == len(entries) - 1 and percentage != 1:
                    raise ValueError("percentage of the last color must be equal to 100" + desc_example)
            self.gradient_desc.append((color, percentage))

    def generate_colors(self, num_of_colors: int):
        if num_of_colors <= 0:
            raise ValueError("number of colors to be generated must be strictly positive")
        steps = np.linspace(0.0, 1.0, num=num_of_colors)
        x, fx_r, fx_g, fx_b = [], [], [], []
        for entry in self.gradient_desc:
            x.append(entry[1])
            fx_r.append(entry[0].r)
            fx_g.append(entry[0].g)
            fx_b.append(entry[0].b)

        steps_r = np.interp(steps, x, fx_r)
        steps_g = np.interp(steps, x, fx_g)
        steps_b = np.interp(steps, x, fx_b)
        res = []
        for i in range(num_of_colors):
            res.append(Color(steps_r[i], steps_g[i], steps_b[i]))
        return res
