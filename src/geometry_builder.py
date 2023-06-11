import numpy as np
import pose
import config
import viewer_io
import color
import math


class PointRGB:
    def __init__(self, point=np.zeros(3), in_color = color.Color()):
        self.point = point
        self.color = in_color


class GeometryBuilder:
    def __init__(self, params: config.Params):
        self.params = params
        self.point_cloud = []
        self.vertices = []
        self.camera_colors = []
        self.poses = []
        self.cam_idx = 1
        self.link_idx = 1
        self.cone_size_used = params.configuration["camera_cone_size"]

    def write_camera_trajectory_plot(self):
        self.params.check_configuration_consistency(self.params.configuration)

        # init
        self.point_cloud.clear()
        self.vertices.clear()
        self.camera_colors.clear()
        self.cam_idx = 1
        self.link_idx = 1
        self.cone_size_used = self.params.configuration["camera_cone_size"]  # could change is auto_cone is set to true

        # load poses from file
        if len(self.poses) == 0:
            self.poses = viewer_io.TrajectoryLoader.load_poses_from_file_with_tum_format(self.params.input_path)

        if len(self.poses) < 1:
            raise ValueError("number of poses must be superior to 1")

        self._apply_rotation_correction_to_poses()

        stats = pose.TrajectoryStats(self.poses)

        # estimate camera cone size if needed
        if self.params.configuration["automatic_cone_size"]:
            self._estimate_camera_cone_size(stats)

        # build colors
        gradient_builder = color.ColorGradient(self.params.get_colormap())
        self.camera_colors = gradient_builder.generate_colors(len(self.poses))

        cam_indices = self._subsample_camera_indices()
        vm = self.params.configuration["view_mode"]

        # build camera cones
        if vm == config.ViewMode.JUST_CONES or vm == config.ViewMode.CONES_AND_LINKS:
            for index in cam_indices:
                self._make_camera_cone(index)

        # build links between cones
        if vm == config.ViewMode.JUST_LINKS or vm == config.ViewMode.CONES_AND_LINKS:
            for index in range(1, len(self.poses)):
                self._make_link(index)

        # save plot as .ply file
        viewer_io.PlotSaver.mesh_ply_saver(self.params.output_path, self.point_cloud, self.vertices)

        # stats.print_stats()
        res_dict = {
            "num_cones_plotted": len(cam_indices),
            "used_cone_size": self.cone_size_used,
            "trajectory_stats": stats,
        }
        return res_dict

    def _subsample_camera_indices(self):
        import copy
        length = len(self.poses)
        indices = [0]
        previous_timestamp = self.poses[0].timestamp
        previous_index = 0
        previous_position = self.poses[0].transformation[0:3, 3]
        subsample_method = self.params.configuration["camera_subsample_mode"]
        factor = self.params.configuration["camera_subsample_factor"]
        for i in range(1, length):
            cur_pose = copy.deepcopy(self.poses[i])
            if subsample_method == config.CameraSubsampleMode.TIMESTAMP_BASED:
                if cur_pose.timestamp - previous_timestamp >= factor:
                    indices.append(i)
                    previous_timestamp = cur_pose.timestamp
            elif subsample_method == config.CameraSubsampleMode.COUNT_BASED:
                if i - previous_index >= factor:
                    indices.append(i)
                    previous_index = i
            elif subsample_method == config.CameraSubsampleMode.DISTANCE_BASED:
                if np.linalg.norm(cur_pose.transformation[0:3, 3] - previous_position) >= factor:
                    indices.append(i)
                    previous_position = cur_pose.transformation[0:3, 3]
            elif subsample_method == config.CameraSubsampleMode.CONE_SIZE_BASED:
                if np.linalg.norm(cur_pose.transformation[0:3, 3] - previous_position) >= factor * self.cone_size_used:
                    indices.append(i)
                    previous_position = cur_pose.transformation[0:3, 3]
        if indices[-1] != length - 1:
            indices.append(length - 1)
        return indices

    def _estimate_camera_cone_size(self, traj_stats):
        max_scene_distance = np.linalg.norm(traj_stats.bounding_box_max - traj_stats.bounding_box_min)
        self.cone_size_used = max_scene_distance * self.params.configuration["auto_cone_size_factor"]

    def _apply_rotation_correction_to_poses(self):
        rot_angles = self.params.configuration["camera_rotation"]
        if rot_angles[0] == 0 and rot_angles[1] == 0 and rot_angles[2] == 0:
            return
        c1 = np.cos(rot_angles[0] * np.pi / 180.0)
        s1 = np.sin(rot_angles[0] * np.pi / 180.0)
        c2 = np.cos(rot_angles[1] * np.pi / 180.0)
        s2 = np.sin(rot_angles[1] * np.pi / 180.0)
        c3 = np.cos(rot_angles[2] * np.pi / 180.0)
        s3 = np.sin(rot_angles[2] * np.pi / 180.0)
        # apply rotation angle in the order x -> y -> z
        rot_mat = np.array([[c2*c3, -c2*s3, s2],
                            [c1*s3+c3*s1*s2, c1*c3-s1*s2*s3, -c2*s1],
                            [s1*s3-c1*c3*s2, c3*s1+c1*s2*s3, c1*c2]])

        for i, cam_pose in enumerate(self.poses):
            new_pose = cam_pose
            new_pose.transformation[0:3, 0:3] = new_pose.transformation[0:3, 0:3].dot(rot_mat)
            self.poses[i] = new_pose

    def _make_camera_cone(self, camera_index):
        cam_color = self.camera_colors[camera_index]
        trans = self.poses[camera_index].transformation
        c_size = self.cone_size_used
        cam_resize = np.array([c_size, c_size, c_size, 1.0])
        num_points = len(self.point_cloud)
        points = np.array([[0, 0, 0, 1], [0.75, 0.5, 1, 1], [-0.75, 0.5, 1, 1], [-0.75, -0.5, 1, 1], [0.75, -0.5, 1, 1],
                           [-0.2, -0.5, 1, 1] , [0.2, -0.5, 1, 1], [0, -0.7, 1, 1], [0, 0, 0.5, 1]]).transpose()
        points = points * cam_resize[:, np.newaxis]
        points = trans.dot(points)
        for i in range(9):
            self.point_cloud.append(PointRGB(points[0:3, i], cam_color))

        triangles = np.array([[0, 2, 1], [0, 1, 4], [0, 4, 3],
                              [0, 3, 2], [2, 3, 4], [1, 2, 4],
                              [6, 5, 7], [7, 5, 8], [6, 7, 8]]) + (num_points * np.ones((9, 3), dtype=np.int64))
        for i in range(9):
            self.vertices.append(triangles[i, :])

    @staticmethod
    def _get_rotation_between_two_cam_centers(cam1, cam2):
        a_n = cam1 - cam2
        a_n = a_n / np.linalg.norm(a_n)
        b_n = np.array([0, 0, 1])
        new_b_n = b_n - a_n * (a_n[0] * b_n[0] + a_n[1] * b_n[1] + a_n[2] * b_n[2])
        new_b_n = new_b_n / np.linalg.norm(new_b_n)

        dot = a_n[0] * b_n[0] + a_n[1] * b_n[1] + a_n[2] * b_n[2]
        len_sq1 = a_n[0] * a_n[0] + a_n[1] * a_n[1] + a_n[2] * a_n[2]
        len_sq2 = b_n[0] * b_n[0] + b_n[1] * b_n[1] + b_n[2] * b_n[2]
        angle = math.acos(dot / math.sqrt(len_sq1 * len_sq2))
        rot = np.eye(3)
        if angle != 0.0:
            axis = np.cross(new_b_n, a_n)
            axis = axis / np.linalg.norm(axis)

            # rotation matrix from axis angle
            ca = math.cos(angle)
            sa = math.sin(angle)
            c = 1 - ca

            # Depack the axis.
            x, y, z = axis

            # Multiplications (to remove duplicate calculations).
            xs = x * sa
            ys = y * sa
            zs = z * sa
            x_c = x * c
            y_c = y * c
            z_c = z * c
            xy_c = x * y_c
            yz_c = y * z_c
            zx_c = z * x_c

            # Update the rotation matrix.
            rot[0, 0] = x * x_c + ca
            rot[0, 1] = xy_c - zs
            rot[0, 2] = zx_c + ys
            rot[1, 0] = xy_c + zs
            rot[1, 1] = y * y_c + ca
            rot[1, 2] = yz_c - xs
            rot[2, 0] = zx_c - ys
            rot[2, 1] = yz_c + xs
            rot[2, 2] = z * z_c + ca
        return rot

    def _make_link(self, camera_index):
        p = 0.7071067   # p = sqrt(2) / 2
        n = -p
        pp = 0.5773502
        nn = -pp
        p20 = pp + 20  # pp = sqrt(3) / 3
        points = [[0, 0, -1],
                  [nn, nn, nn], [pp, nn, nn], [pp, pp, nn], [nn, pp, nn],
                  [0, -1, 0], [n, n, 0], [-1, 0, 0], [n, p, 0],
                  [0, 1, 0], [p, p, 0], [1, 0, 0], [p, n, 0],

                  [0, -1, 20], [n, n, 20], [-1, 0, 20], [n, p, 20],
                  [0, 1, 20], [p, p, 20], [1, 0, 20], [p, n, 20],
                  [nn, nn, p20], [pp, nn, p20], [pp, pp, p20], [nn, pp, p20],
                  [0, 0, 21]]

        triangles = [[0, 2, 1], [0, 3, 2], [0, 4, 3], [0, 1, 4],

                     [1, 5, 6], [1, 2, 5], [5, 2, 12],
                     [2, 11, 12], [2, 3, 11], [11, 3, 10],
                     [3, 9, 10], [3, 4, 9], [9, 4, 8],
                     [4, 7, 8], [4, 1, 7], [7, 1, 6],

                     [5, 13, 6], [13, 14, 6], [6, 14, 7], [14, 15, 7],
                     [7, 15, 8], [15, 16, 8], [8, 16, 9], [16, 17, 9],
                     [9, 17, 10], [17, 18, 10], [10, 18, 11], [18, 19, 11],
                     [11, 19, 12], [19, 20, 12], [12, 20, 13], [13, 5, 12],

                     [19, 22, 20], [19, 23, 22], [18, 23, 19],
                     [17, 23, 18], [17, 24, 23], [16, 24, 17],
                     [15, 24, 16], [15, 21, 24], [14, 21, 15],
                     [13, 21, 14], [13, 22, 21], [20, 22, 13],

                     [25, 24, 21], [25, 21, 22], [25, 22, 23], [25, 23, 24]]

        num_points = 26
        zero = np.array([0, 0, 0, 1])
        cam1 = self.poses[camera_index - 1].transformation.dot(zero)
        cam2 = self.poses[camera_index].transformation.dot(zero)

        rot = self._get_rotation_between_two_cam_centers(cam2[:-1], cam1[:-1])
        r = self.params.configuration["links_size_ratio"] * self.cone_size_used
        point_cloud_size = len(self.point_cloud)
        for i in range(num_points):
            cam = cam1
            v_color = self.camera_colors[camera_index - 1]
            bias = 0
            if i >= num_points / 2:
                cam = cam2
                v_color = self.camera_colors[camera_index]
                bias = 20
            p_ = np.array([points[i][0], points[i][1], points[i][2] - bias])
            pp_ = rot.dot(p_)
            point = r * pp_ + cam[:-1]
            self.point_cloud.append(PointRGB(point, v_color))

        for tri in triangles:
            self.vertices.append(np.array([tri[0] + point_cloud_size,
                                           tri[1] + point_cloud_size,
                                           tri[2] + point_cloud_size]))
