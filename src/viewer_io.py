import pathlib
import numpy as np
import pose


class TrajectoryLoader:
    @staticmethod
    def load_poses_from_file_with_tum_format(file_path_str):
        poses = []
        file_path = pathlib.Path(file_path_str)
        if not file_path.is_file():
            raise IOError(f"trajectory file could not be found at: {file_path_str}")
        with file_path.open("r") as file_obj:
            lines = file_obj.readlines()
        line_error_msg = "line [{}] of file [{}] is not in the format [timestamp tx ty tz qx qy qz qw]"
        for i, line in enumerate(lines):
            line = line.strip(" \n")
            if line.startswith("#"):
                continue

            words = line.split(" ")
            if len(words) == 0:
                continue
            if len(words) != 8:
                raise IOError(line_error_msg.format(i + 1, file_path.name))
            try:
                timestamp = float(words[0])
                position = np.array([float(words[1]), float(words[2]), float(words[3])])
                quaternion = np.array([float(words[4]), float(words[5]), float(words[6]), float(words[7])])
            except ValueError:
                raise IOError(line_error_msg.format(i + 1, file_path.name))

            new_pose = pose.Pose.pose_from_position_quaternion(timestamp, position, quaternion)
            poses.append(new_pose)
        return poses
