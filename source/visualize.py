import open3d as o3d
import pickle
from scipy.spatial.transform import Rotation 
import numpy as np 


def transform_pcds(input):
    
    data_storage_filepath = input + 'output.pkl'

    openfile = open(data_storage_filepath, "rb")
    data_storage = pickle.load(openfile)
    openfile.close()

    T_f = data_storage["T_f"]
    T_r = data_storage["T_r"]

    T_sts = T_f @ np.linalg.inv(T_r)

    print(T_sts)
    print(Rotation.from_matrix(T_sts[:3, :3]).as_euler("xyz"))

    vis = o3d.visualization.Visualizer()
    vis.create_window(
            window_name='Carla Lidar',
            width=960,
            height=540,
            left=480,
            top=270)
    vis.get_render_option().background_color = [0.05, 0.05, 0.05]
    vis.get_render_option().point_size = 1
    vis.get_render_option().show_coordinate_frame = True

    for pcd_path, car_pose in data_storage["pointcloud_f"]:
        filepath_f = input + pcd_path
        pcd_f = o3d.io.read_point_cloud(filepath_f)

        T_glob = car_pose @ T_f
        pcd_f.transform(T_glob)

        vis.add_geometry(pcd_f)
        vis.poll_events()
        vis.update_renderer()

    for pcd_path, car_pose in data_storage["pointcloud_r"]:
        filepath_r = input + pcd_path
        pcd_r = o3d.io.read_point_cloud(filepath_r)

        T_glob = car_pose @ T_r
        pcd_r.transform(T_glob)

        vis.add_geometry(pcd_r)
        vis.poll_events()
        vis.update_renderer()

    vis.run()