import numpy as np


class Pose:
    def __init__(self, timestamp=0.0, transformation=np.eye(4)):
        self.timestamp = timestamp
        self.transformation = transformation

    @staticmethod
    def pose_from_position_quaternion(timestamp, position, quaternion):
        res = Pose(timestamp)
        # Extract the values from Q
        q0 = quaternion[0]
        q1 = quaternion[1]
        q2 = quaternion[2]
        q3 = quaternion[3]

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