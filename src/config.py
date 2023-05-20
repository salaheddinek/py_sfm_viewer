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
                                             "each 4 poses provided",
            CameraSubsampleMode.TIMESTAMP_BASED: "a camera cone is plotted when the time since the previous one"
                                                 " is bigger then the subsampling factor"
        }
        print("available camera subsampling modes:")
        for s_mode in CameraSubsampleMode:
            print(f"{s_mode.value} => {s_mode.name}: {msg_dict[s_mode]}.")


DEFAULT_PARAMS = {
    "first_camera_color": "rgb(255, 0, 0)",
    "last_camera_color": "rgb(0, 0, 255)",
    "view_mode": ViewMode.CONES_AND_LINKS,
    "camera_cone_size": 0.12,
    "camera_subsample_mode": CameraSubsampleMode.DISTANCE_BASED,
    "camera_subsample_factor": 0.05,
    "available_colormaps": {   # taken from https://webgradients.com/
        "Ripe_Malinka": "#f093fb 0%, #f5576c 100%",
        "Itmeo_Branding": "#2af598 0%, #009efd 100%",
        "Burning_Spring": "#4fb576 0%, #44c489 30%, #28a9ae 46%, #28a2b7 59%, #4c7788 71%, #6c4f63 86%, #432c39 100%",
    },
    "colormap_index": -1,
    "links_size_ratio": 0.05,
    "version": _version.__version__,
}

class Params:
    def __init__(self, input_path="", output_path=""):
        self.input_path = input_path
        self.output_path = output_path
        self.configuration = {
            "first_camera_color": "rgb(255, 0, 0)",
            "last_camera_color": "rgb(0, 0, 255)",
            "view_mode": ViewMode.CONES_AND_LINKS,
            "camera_cone_size": 0.12,
            "camera_subsample_mode": CameraSubsampleMode.DISTANCE_BASED,
            "camera_subsample_factor": 0.05,
            "available_colormaps": {  # taken from https://webgradients.com/
                "Ripe_Malinka": "#f093fb 0%, #f5576c 100%",
                "Itmeo_Branding": "#2af598 0%, #009efd 100%",
                "Burning_Spring": "#4fb576 0%, #44c489 30%, #28a9ae 46%, #28a2b7 59%, #4c7788 71%, #6c4f63 86%, #432c39 100%",
            },
            "colormap_index": -1,
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


    def load_from_config_file_if_possible(self):
        pass
def get_params():
    # save_path = pathlib.Path("/home/buser/xx.json")
    # with save_path.open("w") as file:
    #     json.dump(DEFAULT_PARAMS, file)
    return DEFAULT_PARAMS


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