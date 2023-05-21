import pathlib
import numpy as np
import pose
import copy


class TrajectoryLoader:
    @staticmethod
    def load_poses_from_file_with_tum_format(file_path_str):
        file_path = pathlib.Path(file_path_str)
        if not file_path.is_file():
            raise IOError(f"trajectory file could not be found at: {file_path_str}")
        with file_path.open("r") as file_obj:
            lines = file_obj.readlines()
        line_error_msg = "line [{}] of file [{}] is not in the format [timestamp tx ty tz qx qy qz qw]"
        poses = []
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
            poses.append(copy.deepcopy(new_pose))
        return poses


class PlotSaver:
    @staticmethod
    def mesh_ply_saver(in_path, points, vertices):
        out_path = pathlib.Path(in_path)
        with out_path.open("w") as file_obj:
            file_obj.write("ply\n")
            file_obj.write("format ascii 1.0\n")
            file_obj.write("comment Slam Viewer generated\n")
            file_obj.write(f"element vertex {len(points)}\n")
            file_obj.write("property float x\n")
            file_obj.write("property float y\n")
            file_obj.write("property float z\n")
            file_obj.write("property uchar red\n")
            file_obj.write("property uchar green\n")
            file_obj.write("property uchar blue\n")
            file_obj.write(f"element face {len(vertices)}\n")
            file_obj.write("property list uchar int vertex_indices\n")
            file_obj.write("end_header\n")
            for xyz_rgb in points:
                file_obj.write(f"{xyz_rgb.point[0]:0.6f} {xyz_rgb.point[1]:0.6f} {xyz_rgb.point[2]:0.6f} "
                               f"{xyz_rgb.color.r} {xyz_rgb.color.g} {xyz_rgb.color.b}\n")
            for ver in vertices:
                file_obj.write(f"3 {ver[0]} {ver[1]} {ver[2]}\n")
