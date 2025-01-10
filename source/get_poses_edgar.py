import pickle 
import numpy as np
from scipy.spatial.transform import Rotation as R
from visualize import transform_pcds

openfile = open('/media/ilirtahiraj/OSshared/diss/dissertation/03_paper/03_SensorToVehicle/carla_town01_lin/scenario_1/output.pkl', "rb")
data_storage = pickle.load(openfile)

T_f = data_storage["T_f"]
T_r = data_storage["T_r"]


rotation_f = R.from_matrix(T_f[:3, :3])
rotation_r = R.from_matrix(T_r[:3, :3])

# (qx, qy, qz, qw)

# S2S 

S2S = T_f @ np.linalg.inv(T_r)

rotation = R.from_matrix(S2S[:3,:3])
quaternion = rotation.as_quat()
euler = rotation.as_euler('xyz', degrees=False)

# Initial Extrinsics
print("Translation S2S (x, y, z): ", S2S[:3,3])
print("Quaternion S2S (qx, qy, qz, qw): ", quaternion) 
print("Euler S2S: ", euler) 

#transform_pcds('/media/ilirtahiraj/OSshared/diss/dissertation/03_paper/03_SensorToVehicle/carla_town01/scenario_1/')
pose = []
for pcd_path, car_pose in data_storage["pointcloud_f"]:
    car_rotation = R.from_matrix(car_pose[:3,:3])
    lidar_pose = car_pose @ T_f
    lidar_rotation = R.from_matrix(lidar_pose[:3,:3])
    quaternion = lidar_rotation.as_quat()

    #pose.append([car_pose[0,3], car_pose[1,3],car_pose[2,3], quaternion[3], quaternion[0], quaternion[1], quaternion[2]])
    pose.append([lidar_pose[0,3], lidar_pose[1,3], lidar_pose[2,3], quaternion[3], quaternion[0], quaternion[1], quaternion[2]])
# Save the poses to a text file
output_file = "poses_lin.txt"
with open(output_file, 'w') as f:
    for p in pose:
        # Convert each pose to a space-separated string
        f.write(" ".join(map(str, p)) + "\n")

print(f"Poses saved to {output_file}")