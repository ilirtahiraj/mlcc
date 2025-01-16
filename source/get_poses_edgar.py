import os
import pickle 
import numpy as np
from scipy.spatial.transform import Rotation as R
import json

# Base directory where your scenes are located
base_dir = '/home/ilirtahiraj/code/mlcc'

# Open the pickle file with data
openfile = open('/media/ilirtahiraj/OSshared/diss/dissertation/03_paper/03_SensorToVehicle/carla_town01_lin/scenario_1/output.pkl', "rb")
data_storage = pickle.load(openfile)

T_f = data_storage["T_f"]
T_r = data_storage["T_r"]

# Rotation matrices
rotation_f = R.from_matrix(T_f[:3, :3])
rotation_r = R.from_matrix(T_r[:3, :3])

# (qx, qy, qz, qw)
S2S = T_f @ np.linalg.inv(T_r)
rotation = R.from_matrix(S2S[:3, :3])
quaternion = rotation.as_quat()
euler = rotation.as_euler('xyz', degrees=False)

# Initial Extrinsics
print("Translation S2S (x, y, z): ", S2S[:3, 3])
print("Quaternion S2S (qx, qy, qz, qw): ", quaternion)
print("Euler S2S: ", euler)

# Loop through scene directories from scene4 to scene6
for scene_num in range(4, 7):  # From scene4 to scene6 (scene4, scene5, scene6)
    scene_dir = f"scene{scene_num}"
    scene_path = os.path.join(base_dir, scene_dir)
    
    # Ensure that the scene directory exists
    if not os.path.exists(scene_path):
        os.makedirs(scene_path)  # Create the scene folder if it doesn't exist
        print(f"Created directory: {scene_path}")
    
    # Create two new empty folders named '4' and '5' inside each scene folder
    for folder_name in ['4', '5']:
        folder_path = os.path.join(scene_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created empty folder: {folder_path}")

    # Create the 'original_pose' folder next to '4' and '5'
    original_pose_folder = os.path.join(scene_path, "original_pose")
    if not os.path.exists(original_pose_folder):
        os.makedirs(original_pose_folder)
        print(f"Created 'original_pose' folder: {original_pose_folder}")

    # Create an empty file named '4.json' inside 'original_pose'
    json_file_path = os.path.join(original_pose_folder, "4.json")
    pose = []
    for pcd_path, car_pose in data_storage["pointcloud_f"]:
        car_rotation = R.from_matrix(car_pose[:3, :3])
        lidar_pose = car_pose @ T_f
        lidar_rotation = R.from_matrix(lidar_pose[:3, :3])
        quaternion = lidar_rotation.as_quat()

        # Append pose in the format: [x, y, z, qx, qy, qz, qw]
        pose.append([
            lidar_pose[0, 3], lidar_pose[1, 3], lidar_pose[2, 3], 
            quaternion[3], quaternion[0], quaternion[1], quaternion[2]
        ])

    # Save the poses in the 4.json file as a JSON array of values
    if not os.path.exists(json_file_path):
        with open(json_file_path, 'w') as json_file:
            json.dump(pose, json_file)  # Write pose data as a JSON array
        print(f"Saved poses to {json_file_path}")
