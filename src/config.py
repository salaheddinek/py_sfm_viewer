import enum
import json
import pathlib
import color
import _version
import appdirs
import copy


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
    def get_view_modes_help_message():
        msg_dict = {
            ViewMode.CONES_AND_LINKS: "display both of camera cones and the links between those cones",
            ViewMode.JUST_CONES: "display camera cones and hide links",
            ViewMode.JUST_LINKS: "display camera links and hide cones"
        }
        msg = "available view modes:\n\n"
        for v_mode in ViewMode:
            msg += f"{v_mode.value} => {v_mode.name}: {msg_dict[v_mode]}.\n"
        return msg


class CameraSubsampleMode(enum.Enum):
    CONE_SIZE_BASED = 0
    COUNT_BASED = 1
    DISTANCE_BASED = 2
    TIMESTAMP_BASED = 3

    @staticmethod
    def get_subsample_modes_listing():
        msg = ""
        for s_mode in CameraSubsampleMode:
            msg += f"{s_mode.value}:{s_mode.name} , "
        return msg + "-1:show_modes_help"

    @staticmethod
    def get_subsample_modes_help_message():
        msg_dict = {
            CameraSubsampleMode.CONE_SIZE_BASED: "the minimum distance of two plotted camera cones is equal to "
                                                 "subsampling factor multiplied by the camera size "
                                                 "(min_dist = factor * cone_size), this is the recommended subsampling"
                                                 " mode to use with a factor of 2.5",
            CameraSubsampleMode.COUNT_BASED: "in this case, if the subsampling factor is 4 then a cone is display for "
                                             "each 4 poses provided. If set to 1, then all cones are plotted",
            CameraSubsampleMode.DISTANCE_BASED: "the frequency of plotting a camera cone is based on how far those "
                                                "cones are, the minimum distance of two plotted camera cones is equal "
                                                "to the subsampling factor",
            CameraSubsampleMode.TIMESTAMP_BASED: "a camera cone is plotted when the time since the previous one"
                                                 " is bigger then the subsampling factor, "
                                                 "this uses the timestamps provided in the input text file",
        }
        msg = "available camera subsampling modes:\n\n"
        for s_mode in CameraSubsampleMode:
            msg += f"{s_mode.value} => {s_mode.name}: {msg_dict[s_mode]}.\n"
        return msg


HELP_INFO = {
    "cone_size": "the camera cone size determines the height of the cones plotted.\n"
                 "if this parameters is too big then only one cone will be shown.\n"
                 "alternatively, if it is too small, then the plotted camera links will be too small to see.\n"
                 "if unsure of the camera cone size then check automatic cone size estimation which works in most"
                 " cases.",
    
    "subsample_factor": "plotting all camera cones of a trajectory, "
                        "can make it hard to see the real path of the camera. "
                        "so, hiding some cones (subsampling) is mandatory for a good trajectory plot.\n\n"
                        "this factor determines how frequent a camera cone is plotted, "
                        "and its behavior is linked to camera subsampling mode (refer to subsample_mode for more info)",
    
    "subsample_mode": CameraSubsampleMode.get_subsample_modes_help_message(),
    
    "view_mode": ViewMode.get_view_modes_help_message(),

    "input_path": "input path must be '.txt' file that contains the trajectory in the TUM format:\n\n"
                  "each line is in the form of <b>[timestamp tx ty tz qx qy qz qw]</b>; where [tx ty tz] represents"
                  " the position of the frame, and [qc qy qz qw] represent its orientation in the form "
                  "of a quaternion.\n\nmore info can be found in the following link:\n\n"
                  "<a href='https://cvg.cit.tum.de/data/datasets/rgbd-dataset/file_formats'>"
                  "https://cvg.cit.tum.de/data/datasets/rgbd-dataset/file_formats</a>",

    "rotation_angles": "the euler angles (degrees) are turned into a rotation matrix (in the order 'xyz'); "
                       "then all camera poses rotations are multiplied with this rotation matrix from the right:\n"
                       "pose[0:3, 0:3] = pose[0:3, 0:3] * rot_matrix(euler_angles)\n"
                       "this can be used to correct the orientation of camera cones without alternating the course"
                       " of the trajectory",
    "links_size": "camera links size ratio is used to calculate the size of the links between camera cones:\n"
                  "link_size = camera_size * link_size_ratio",
    "auto_cone_size": "auto cone size factor is used to calculate the camera cones,"
                      " in the case of automatic estimation of cone size is set to True: \n"
                      "cone_size = auto_cone_size_factor * length_of_trajectory_bounding_box",
}


class DataConsistency:
    @staticmethod
    def check_view_mode(in_data):
        try:
            ViewMode(in_data)
        except ValueError as err:
            raise ValueError(f"{err}, possible values: {[v_mode.value for v_mode in ViewMode]}")

    @staticmethod
    def check_subsample_mode(in_data):
        try:
            CameraSubsampleMode(in_data)
        except ValueError as err:
            raise ValueError(f"{err}, possible values: {[v_mode.value for v_mode in CameraSubsampleMode]}")

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

    @staticmethod
    def check_color_gradient(in_c):
        if not isinstance(in_c, str):
            raise TypeError(f"expect str type when color gradient parsing, {in_c} is a {type(in_c)}")
        else:
            color.ColorGradient(in_c)

    @staticmethod
    def check_rotation_angles(in_data):
        if not isinstance(in_data, list):
            raise TypeError(f"expect a list of 3 floats for rotation angles 'xyz', {in_data} is a {type(in_data)}")
        elif len(in_data) != 3:
            raise ValueError(f"expect a list of 3 floats for rotation angles 'xyz', "
                             f"length of provided list is {len(in_data)}")


class Params:
    def __init__(self, input_path="", output_path=""):
        self.input_path = input_path
        self.output_path = output_path
        self.configuration = {
            "view_mode": ViewMode.CONES_AND_LINKS,
            "camera_cone_size": 0.012,
            "automatic_cone_size": True,
            "camera_subsample_mode": CameraSubsampleMode.CONE_SIZE_BASED,
            "camera_subsample_factor": 2.5,
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
            "colormap_used": "aqua_splash",
            "first_camera_color": "rgb(255,0,0)",
            "last_camera_color": "rgb(0,0,255)",
            "camera_rotation": [0.0, 0.0, 0.0],
            "display_ascii_art": True,
            "links_size_ratio": 0.05,
            "auto_cone_size_factor": 0.03,
            "use_gui": True,
            "version": _version.__version__,
        }

    def process_output_path(self):
        in_path = pathlib.Path(self.input_path)
        if self.output_path.strip() == "":
            if self.input_path.strip() == "":
                self.output_path = "trajectory_plot.ply"
            else:
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
        if cfg["automatic_cone_size"]:
            print(f"camera view mode: [{cfg['view_mode'].name}] | automatic cone size estimation: [True]")
        else:
            print(f"camera view mode: [{cfg['view_mode'].name}] | camera cone size: [{cfg['camera_cone_size']}]")
        print(f"camera subsample mode: [{cfg['camera_subsample_mode'].name}] | "
              f"subsample factor: [{cfg['camera_subsample_factor']}]")
        print(f"used colormap : [{cfg['colormap_used'].upper()}]")
        if cfg["colormap_used"] == "custom":
            print(f"camera color:  first={cfg['first_camera_color']}  =>  last={cfg['last_camera_color']}")
        rot = cfg["camera_rotation"]
        if rot[0] != 0 or rot[1] != 0 or rot[2] != 0:
            print(f"camera rotation correction angles (deg): [x:{rot[0]:g}, y:{rot[1]:g}, z:{rot[2]:g}]")

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
        config_path = self.get_config_file_path()
        if not config_path.is_file():
            return
        with config_path.open("r") as file_obj:
            try:
                new_config = json.load(file_obj)
                self.check_configuration_consistency(new_config)
            except ValueError as err:
                print(f"{str(err)}, loading config from disk aborted")
                self.delete_config_file_if_exists()
                return
        new_config["colormap_used"] = new_config["colormap_used"].strip().lower().replace(" ", "_")
        colormaps = new_config["available_colormaps"]
        new_colormaps = {}
        for key, value in colormaps.items():
            new_colormaps[key.strip().lower().replace(" ", "_")] = value
        new_config["available_colormaps"] = colormaps
        new_config["view_mode"] = ViewMode(new_config["view_mode"])
        new_config["camera_subsample_mode"] = CameraSubsampleMode(new_config["camera_subsample_mode"])
        new_config["version"] = _version.__version__
        self.configuration = new_config

    def save_to_config_file(self):
        config_path = self.get_config_file_path()
        config_dir_path = config_path.parent
        config_dir_path.mkdir(parents=True, exist_ok=True)
        try:
            self.check_configuration_consistency(self.configuration)
        except ValueError as err:
            print(f"{str(err)}, saving config to disk aborted")
            return
        save_config = copy.deepcopy(self.configuration)
        save_config["view_mode"] = save_config["view_mode"].value
        save_config["camera_subsample_mode"] = save_config["camera_subsample_mode"].value
        with config_path.open("w") as file_obj:
            json.dump(save_config, file_obj, indent=4)

    @staticmethod
    def get_config_file_path():
        app_dir = appdirs.user_config_dir(_version.__package__)
        return pathlib.Path(app_dir) / "config.json"

    @staticmethod
    def delete_config_file_if_exists():
        try:
            Params.get_config_file_path().unlink(missing_ok=True)
        except OSError as err:
            print(f"Warning: could not delete old config file, err: {err}")

    def available_color_maps(self):
        msg = "custom, ".upper()
        for c_map in self.configuration["available_colormaps"]:
            msg += c_map.upper() + ", "
        return msg[:-2]

    @staticmethod
    def check_configuration_consistency(config_dict:dict):
        default_config = Params().configuration
        err_msg = "bad configuration dict,"
        for key in config_dict:
            if key not in default_config:
                raise ValueError(f"{err_msg} {key} is not a valid key")

        for key in default_config:
            if key not in config_dict:
                raise ValueError(f"{err_msg} missing {key}")
        try:
            DataConsistency.check_subsample_mode(config_dict["camera_subsample_mode"])
            DataConsistency.check_view_mode(config_dict["view_mode"])
            DataConsistency.check_positive_float("camera_cone_size", config_dict["camera_cone_size"])
            DataConsistency.check_positive_float("camera_subsample_factor", config_dict["camera_subsample_factor"])
            DataConsistency.check_positive_float("links_size_ratio", config_dict["links_size_ratio"])
            DataConsistency.check_positive_float("auto_cone_size_factor", config_dict["auto_cone_size_factor"])
            DataConsistency.check_color(config_dict["first_camera_color"])
            DataConsistency.check_color(config_dict["last_camera_color"])
            DataConsistency.check_rotation_angles(config_dict["camera_rotation"])
        except ValueError as err:
            raise ValueError(err_msg + " " + str(err))
        except TypeError as err:
            raise TypeError(err_msg + " " + str(err))

        if not isinstance(config_dict["display_ascii_art"], bool):
            raise ValueError(err_msg + " 'display_ascii_art' is not a bool type")
        if not isinstance(config_dict["use_gui"], bool):
            raise ValueError(err_msg + " 'use_gui' is not a bool type")
        if not isinstance(config_dict["automatic_cone_size"], bool):
            raise ValueError(err_msg + " 'automatic_cone_size' is not a bool type")
        if not isinstance(config_dict["available_colormaps"], dict):
            raise ValueError(err_msg + " 'available_colormaps' is not a dict type")
        for colormap_key in config_dict["available_colormaps"]:
            if not isinstance(colormap_key, str):
                raise ValueError(f"{err_msg} {colormap_key} is not a valid colormap key type, str is needed")
            try:
                DataConsistency.check_color_gradient(config_dict["available_colormaps"][colormap_key])
            except ValueError as err:
                raise ValueError(err_msg + " " + str(err))
            except TypeError as err:
                raise TypeError(err_msg + " " + str(err))

        if config_dict["colormap_used"] != "custom" and \
                config_dict["colormap_used"] not in config_dict["available_colormaps"]:
            raise ValueError(f"{err_msg} {config_dict['colormap_used']} is not a valid colormap choice")
