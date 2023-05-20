import numpy as np
import pose
import config
import viewer_io


class GeometryBuilder:
    def __init__(self, params: config.Params):
        self.params = params
        self.point_cloud = []
        self.vertices = []
        self.camera_colors = []
        self.poses = []
        self.cam_idx = 1
        self.link_idx = 1

    def write_camera_trajectory_plot(self):
        # TODO implement params consistency check
        self.point_cloud.clear()
        self.vertices.clear()
        self.camera_colors.clear()
        self.cam_idx = 1
        self.link_idx = 1
        self.poses = viewer_io.TrajectoryLoader.load_poses_from_file_with_tum_format(self.params.input_path)

