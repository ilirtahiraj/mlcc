import pickle 
import numpy as np
from scipy.spatial.transform import Rotation as R

openfile = open('/media/ilirtahiraj/OSshared/diss/dissertation/03_paper/03_SensorToVehicle/carla_town01/scenario_1/output.pkl', "rb")
data_storage = pickle.load(openfile)

T_f = data_storage["T_f"]
T_r = data_storage["T_r"]


rotation_f = R.from_matrix(T_f[:3, :3])
rotation_r = R.from_matrix(T_r[:3, :3])

# Convert to quaternion (qx, qy, qz, qw)
quaternion_f = rotation_f.as_quat()
quaternion_r = rotation_r.as_quat()

# S2S 
S2S = np.linalg.inv(T_f).dot(T_r)
rotation = R.from_matrix(S2S[:3, :3])
rotation.as_euler('zxy', degrees=True)
quaternion = rotation.as_quat()

# Initial Extrinsics
print("Translation Front: ", T_f[:3,3])
print("Quaternion Front: ", quaternion_f) 
print("Translation Rear: ", T_r[:3,3])
print("Quaternion Rear: ", quaternion_r) 
print("Translation S2S: ", S2S[:3,3])
print("Quaternion S2S: ", quaternion_r) 


for pcd_path, car_pose in data_storage["pointcloud_f"]:
    # TODO
    pass

for pcd_path, car_pose in data_storage["pointcloud_r"]:
    # TODO
    pass