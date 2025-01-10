import numpy as np
from scipy.spatial.transform import Rotation as R

# Input values directly in the code
# Example: -4.02441 0.000908054 -0.549468 0.0001181 -0.173634 -0.000173306 0.98481
gt = "1.86026537  0.00273564 -0.16042542  -4.37113875e-08 1.03406510e-17  1.42944123e-16  1.00000000e+00"
input_data = "1.67611 0.103503 -0.299748 -0.0136674 -0.0293597 0.0226272 0.999219"
gt_data = list(map(float, gt.split()))
data = list(map(float, input_data.split()))

# Assign values
tx, ty, tz, qw, qx, qy, qz = data
gtx, gty, gtz, gtqw, gtqx, gtqy, gtqz = gt_data

# Create a Rotation object from the quaternion
rotation = R.from_quat([qx, qy, qz, qw])
gt_rotation = R.from_quat([gtqx, gtqy, gtqz, gtqw])

# Convert to Euler angles
euler_angles = rotation.as_euler('xyz', degrees=False)
gt_euler_angles = gt_rotation.as_euler('xyz', degrees=False)

# Output Euler angles
roll, pitch, yaw = np.rad2deg(euler_angles)
gt_roll, gt_pitch, gt_yaw = np.rad2deg(gt_euler_angles)
print(f"Translation Error:\nX: {tx-gtx}\nY: {ty-gty}\nZ: {tz-gtz}")
#print(f"Euler angle erros (in degree):\nRoll: {roll- gt_roll}\nPitch: {gt_pitch- pitch}\nYaw: {360 - np.abs(gt_yaw-yaw)}")
print(f"Euler angle erros (in degree):\nRoll: {roll- gt_roll}\nPitch: {gt_pitch- pitch}\nYaw: {gt_yaw-yaw}")
