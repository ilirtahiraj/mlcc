import os
import shutil
import pickle 
import numpy as np
from scipy.spatial.transform import Rotation as R
from createpcd import *
import random
import yaml

# Base directory where your scenes are located
base_dir = '/home/ilirtahiraj/code/mlcc'

# Source directory for point cloud files
pcd_source_dir = '/media/ilirtahiraj/OSshared/diss/dissertation/03_paper/03_SensorToVehicle/carla_town01_curve/scenario_1/'

with open("source/config.yaml", "r") as file:
    config_data = yaml.safe_load(file)

# Open the pickle file with data
with open(os.path.join(pcd_source_dir, 'output.pkl'), "rb") as openfile:
    data_storage = pickle.load(openfile)

T_f = data_storage["T_f"]

# Loop through scene directories from scene1 to scene3
for scene_num in range(1, 101):
    scene_dir = f"scene{scene_num}"
    scene_path = os.path.join(base_dir, scene_dir)
    
    # Ensure that the scene directory and subfolders exist
    for folder_name in ['4', '5', 'original_pose']:
        folder_path = os.path.join(scene_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)

    # Save every 10th pose to 4.json in original_pose folder
    pose_file_path = os.path.join(scene_path, "original_pose", "4.json")
    poses = []
    pcd_files_to_copy = []
    
    # Extract and process every 10th pointcloud pose
    for idx, (pcd_path, car_pose) in enumerate(data_storage["pointcloud_f"]):
        if idx % 5 == 0:  # Take every 10th pose
            lidar_pose = car_pose @ T_f
            lidar_rotation = R.from_matrix(lidar_pose[:3, :3])
            quaternion = lidar_rotation.as_quat()

            # Append pose as a flat list of values
            pose_line = f"{lidar_pose[0, 3]} {lidar_pose[1, 3]} {lidar_pose[2, 3]} {quaternion[3]} {quaternion[0]} {quaternion[1]} {quaternion[2]}"
            poses.append(pose_line)
    
    #poses.pop()

    #Create the pcd files with the calibration error


    transform_lidar_f = config_data.get("transform_lidar_f_sim", "")[0]
    transform_lidar_r = config_data.get("transform_lidar_r_sim", "")[0]

    random.seed(scene_num)

    r_error_f = [random.uniform(-3.0, 3.0) for _ in range(3)]
    t_error_f = [random.uniform(-0.1, 0.1) for _ in range(3)]
    errors_f = r_error_f + t_error_f

    r_error_r = [random.uniform(-3.0, 3.0) for _ in range(3)]
    t_error_r = [random.uniform(-0.1, 0.1) for _ in range(3)]
    errors_r = r_error_r + t_error_r

    for i in range(6):
        transform_lidar_f[i] += errors_f[i]
        transform_lidar_r[i] += errors_r[i]

    T_f_init = np.eye(4)
    T_f_init[:3, :3] = R.from_euler('xyz', transform_lidar_f[:3], degrees=True).as_matrix()
    T_f_init[:3, 3] = np.array(transform_lidar_f[3:])

    T_r_init = np.eye(4)
    T_r_init[:3, :3] = R.from_euler('xyz', transform_lidar_r[:3], degrees=True).as_matrix()
    T_r_init[:3, 3] = np.array(transform_lidar_r[3:])
    
    pcd_name = 1
    pcd_output_name = 0
    while pcd_name < 113:
        process_point_cloud("/media/ilirtahiraj/OSshared/diss/dissertation/03_paper/03_SensorToVehicle/carla_town01_curve/scenario_1/lidar_front/" + str(pcd_name) + ".pcd",
                            T_f_init,
                            os.path.join(scene_path, '4'),
                            str(pcd_output_name) + ".pcd"
        )

        #Use every 10th file
        pcd_name = pcd_name + 5
        pcd_output_name = pcd_output_name + 1

    pcd_name = 1
    pcd_output_name = 0
    while pcd_name < 113:
        process_point_cloud("/media/ilirtahiraj/OSshared/diss/dissertation/03_paper/03_SensorToVehicle/carla_town01_curve/scenario_1/lidar_rear/" + str(pcd_name) + ".pcd",
                            T_r_init,
                            os.path.join(scene_path, '5'),
                            str(pcd_output_name) + ".pcd"
        )

        #Use every 10th file
        pcd_name = pcd_name + 5
        pcd_output_name = pcd_output_name + 1

    # Save poses to 4.json
    with open(pose_file_path, 'w') as pose_file:
        pose_file.write("\n".join(poses))
    print(f"Saved every 10th pose to {pose_file_path}")


    # Create pose.json and ref.json next to the folders
    pose_json_path = os.path.join(scene_path, "pose.json")
    ref_json_path = os.path.join(scene_path, "ref.json")

    # Data for pose.json and ref.json as per your requirements
    pose_data = "0 0 0 1 0 -1.35558e-20 2.71051e-20"
    ref_data = "1.86026537 0.00273564 -0.16042542 -4.37113875e-08 1.03406510e-17 1.42944123e-16 1.00000000e+00"

    # Write single-line data to pose.json
    with open(pose_json_path, 'w') as pose_json_file:
        pose_json_file.write(pose_data)
    print(f"Saved pose data to {pose_json_path}")

    # Write single-line data to ref.json
    with open(ref_json_path, 'w') as ref_json_file:
        ref_json_file.write(ref_data)
    print(f"Saved ref data to {ref_json_path}")


    #for idx, (pcd_path, car_pose) in enumerate(data_storage["pointcloud_r"]):
    #    if idx % 10 == 0:  # Take every 10th pose

    #        # Add PCD file path for copying
    #        pcd_files_to_copy.append(os.path.join(pcd_source_dir, pcd_path))


    # Copy PCD files to folder '5' and rename them sequentially
    #destination_folder_5 = os.path.join(scene_path, '5')
    #for new_idx, pcd_file in enumerate(pcd_files_to_copy):
    #    if os.path.isfile(pcd_file):
    #        destination_file = os.path.join(destination_folder_5, f"{new_idx}.pcd")
    #        shutil.copy(pcd_file, destination_file)
    #        print(f"Copied and renamed {pcd_file} to {destination_file}")