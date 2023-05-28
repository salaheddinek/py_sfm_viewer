import numpy as np


class Pose:
    def __init__(self, timestamp=0.0, transformation=np.eye(4)):
        self.timestamp = timestamp
        self.transformation = transformation

    @staticmethod
    def pose_from_position_quaternion(timestamp, position, quaternion):
        res = Pose(timestamp)
        norm = np.linalg.norm(quaternion)
        qn = quaternion / norm
        # Extract the values from Q
        q0 = qn[0]
        q1 = qn[1]
        q2 = qn[2]
        q3 = qn[3]

        # First row of the rotation matrix
        r00 = 2 * (q0 * q0 + q1 * q1) - 1
        r01 = 2 * (q1 * q2 - q0 * q3)
        r02 = 2 * (q1 * q3 + q0 * q2)

        # Second row of the rotation matrix
        r10 = 2 * (q1 * q2 + q0 * q3)
        r11 = 2 * (q0 * q0 + q2 * q2) - 1
        r12 = 2 * (q2 * q3 - q0 * q1)

        # Third row of the rotation matrix
        r20 = 2 * (q1 * q3 - q0 * q2)
        r21 = 2 * (q2 * q3 + q0 * q1)
        r22 = 2 * (q0 * q0 + q3 * q3) - 1

        # 3x3 rotation matrix
        rot_matrix = np.array([[r00, r01, r02],
                               [r10, r11, r12],
                               [r20, r21, r22]])
        res.transformation[0:3, 0:3] = rot_matrix
        res.transformation[0:3, 3] = position
        return res


class TrajectoryStats:
    def __init__(self, poses_list):
        if len(poses_list) == 0:
            raise ValueError("poses list provided to trajectory stats is empty")
        for pose in poses_list:
            if not isinstance(pose, Pose):
                raise ValueError("the list contains non Pose elements")
        self.total_distance = 0
        self.total_time = poses_list[-1].timestamp - poses_list[0].timestamp
        self.num_poses = len(poses_list)
        previous_position = poses_list[0].transformation[0:3, 3]
        self.bounding_box_max = previous_position
        self.bounding_box_min = previous_position
        for i in range(1, len(poses_list)):
            cur_position = poses_list[i].transformation[0:3, 3]
            self.bounding_box_max = np.maximum(self.bounding_box_max, cur_position)
            self.bounding_box_min = np.minimum(self.bounding_box_min, cur_position)
            self.total_distance = np.linalg.norm(cur_position - previous_position)
            previous_position = cur_position

    def get_stats(self):
        msg = f"number of poses in trajectory: {self.num_poses}\n"
        msg += f"total timestamp difference: {self.total_time}\n"
        msg += f"total distance covered by the camera: {self.total_distance:g}\n"
        msg += f"trajectory bounding box:\n"
        msg += f"  * max=[x:{self.bounding_box_max[0]:0.6f}, y:{self.bounding_box_max[1]:0.6f}, " \
               f"z:{self.bounding_box_max[2]:0.6f}]\n"
        msg += f"  * min=[x:{self.bounding_box_min[0]:0.6f}, " \
               f"y:{self.bounding_box_min[1]:0.6f},  z:{self.bounding_box_min[2]:0.6f}]\n"
        return msg

    def print_stats(self):
        print(self.get_stats())
