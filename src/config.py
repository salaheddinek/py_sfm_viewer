import enum
import json
import pathlib
import color
import _version


class ViewMode(enum.Enum):
    CONES_AND_LINKS = 0
    JUST_CONES = 1
    JUST_LINKS = 2

    @staticmethod
    def get_view_modes_listing():
        msg = ""
        for v_mode in ViewMode:
            msg += f"{v_mode.value}:{v_mode.name} , "
        return msg + "-1:show_modes_help"

    @staticmethod
    def print_view_modes_help_message():
        msg_dict = {
            ViewMode.CONES_AND_LINKS: "display both of camera cones and the links between those cones",
            ViewMode.JUST_CONES: "display camera cones and hide links",
            ViewMode.JUST_LINKS: "display camera links and hide cones"
        }
        print("available view modes:")
        for v_mode in ViewMode:
            print(f"{v_mode.value} => {v_mode.name}: {msg_dict[v_mode]}.")


class CameraSubsampleMode(enum.Enum):
    DISTANCE_BASED = 0
    COUNT_BASED = 1
    TIMESTAMP_BASED = 2

    @staticmethod
    def get_subsample_modes_listing():
        msg = ""
        for s_mode in CameraSubsampleMode:
            msg += f"{s_mode.value}:{s_mode.name} , "
        return msg + "-1:show_modes_help"

    @staticmethod
    def print_subsample_modes_help_message():
        msg_dict = {
            CameraSubsampleMode.DISTANCE_BASED: "the frequency of plotting a camera cone is based on how far those "
                                                "cones are, subsampling factor refers to this distance in this case",
            CameraSubsampleMode.COUNT_BASED: "in this case, if the subsampling factor is 4 then a cone is display for "
                                             "each 4 poses provided. If set to 1, then all cones are plotted",
            CameraSubsampleMode.TIMESTAMP_BASED: "a camera cone is plotted when the time since the previous one"
                                                 " is bigger then the subsampling factor"
        }
        print("available camera subsampling modes:")
        for s_mode in CameraSubsampleMode:
            print(f"{s_mode.value} => {s_mode.name}: {msg_dict[s_mode]}.")


class Params:
    def __init__(self, input_path="", output_path=""):
        self.input_path = input_path
        self.output_path = output_path
        self.configuration = {
            "view_mode": ViewMode.CONES_AND_LINKS,
            "camera_cone_size": 0.012,
            "camera_subsample_mode": CameraSubsampleMode.COUNT_BASED,
            "camera_subsample_factor": 40.0,
            "available_colormaps": {  # taken from https://webgradients.com/
                "ripe_malinka": "#f093fb 0%, #f5576c 100%",
                "gagarin_view": "#69EACB 0%, #EACCF8 48%, #6654F1 100%",
                "sweet_period": "#3f51b1 0%, #5a55ae 13%, #7b5fac 25%, #8f6aae 38%, #a86aa4 50%, "
                                "#cc6b8e 62%, #f18271 75%, #f3a469 87%, #f7c978 100%",
                "red_salvation": "#f43b47 0%, #453a94 100%",
                "purple_division": "#7028e4 0%, #e5b2ca 100%",
                "aqua_splash": "#13547a 0%, #80d0c7 100%",
                "fruit_blend": "#f9d423 0%, #ff4e50 100%",
                "palo_alto": "#16a085 0%, #f4d03f 100%",
            },
            "colormap_used": "custom",
            "first_camera_color": "rgb(255,0,0)",
            "last_camera_color": "rgb(0,0,255)",
            "display_ascii_art": True,
            "links_size_ratio": 0.05,
            "version": _version.__version__,
        }

    def process_output_path(self):
        in_path = pathlib.Path(self.input_path)
        if self.output_path.strip() == "":
            out_path = in_path.parent / (in_path.stem + "_plot.ply")
            self.output_path = str(out_path)
        else:
            out_path = pathlib.Path(self.output_path)
            if out_path.suffix.lower() != ".ply":
                self.output_path = self.output_path.strip() + ".ply"

    def print_info(self):
        cfg = self.configuration
        print(f"input path: {self.input_path}")
        print(f"output path: {self.output_path}")
        print(f"camera view mode: [{cfg['view_mode'].name}] | camera cone size: [{cfg['camera_cone_size']}]")
        print(f"camera subsample mode: [{cfg['camera_subsample_mode'].name}] | "
              f"subsample factor: [{cfg['camera_subsample_factor']}]")
        print(f"used colormap : [{cfg['colormap_used'].upper()}]")
        if cfg["colormap_used"] == "custom":
            print(f"camera color:  first={cfg['first_camera_color']}  =>  last={cfg['last_camera_color']}")

    def update_used_colormap(self, cmap_choice):
        choice = cmap_choice.strip().lower().replace(" ", "_")
        if choice == "custom" or choice in self.configuration["available_colormaps"]:
            self.configuration["colormap_used"] = choice
        else:
            raise ValueError(f"unrecognized colormap [{choice}], available colormaps: [{self.available_color_maps()}]")

    def get_colormap(self):
        choice = self.configuration["colormap_used"]
        if choice == "custom":
            return f"{self.configuration['first_camera_color']} 0%, {self.configuration['last_camera_color']} 100%"
        else:
            return self.configuration["available_colormaps"][choice]

    def load_from_config_file_if_possible(self):
        pass

    def available_color_maps(self):
        msg = "custom, ".upper()
        for c_map in self.configuration["available_colormaps"]:
            msg += c_map.upper() + ", "
        return msg[:-2]


class DataConsistency:
    @staticmethod
    def check_view_mode(in_data):
        if not isinstance(in_data, int):
            raise TypeError(f"Camera_view_mode should be integer, {in_data} is {type(in_data)}")
        else:
            possible_values = [v_mode.value for v_mode in ViewMode]
            if in_data not in possible_values:
                raise ValueError(f"invalid Camera_view_mode value, possible values: {possible_values}")

    @staticmethod
    def check_subsample_mode(in_data):
        if not isinstance(in_data, int):
            raise TypeError(f"Camera_subsample_mode should be integer, {in_data} is {type(in_data)}")
        else:
            possible_values = [s_mode.value for s_mode in CameraSubsampleMode]
            if in_data not in possible_values:
                raise ValueError(f"invalid Camera_subsample_mode value, possible values: {possible_values}")

    @staticmethod
    def check_positive_float(var_name, var_value):
        if not isinstance(var_value, (int, float)):
            raise TypeError(f"{var_name} should be float, {var_value} is {type(var_value)}")
        else:
            if var_value <= 0:
                raise ValueError(f"{var_name} should be strictly positive, given value: {var_value}")
    @staticmethod
    def check_color(in_c):
        if not isinstance(in_c, str):
            raise TypeError(f"expect str type when color parsing, {in_c} is a {type(in_c)}")
        else:
            color.Color.parse_from_str(in_c)
