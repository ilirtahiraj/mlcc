import open3d as o3d
import numpy as np
import os

# Function to apply a transformation matrix to the point cloud
def transform_point_cloud(pcd, transformation_matrix):
    #print(transformation_matrix)
    pcd.paint_uniform_color([1, 0, 0])  # Red
    transformed_pcd = o3d.geometry.PointCloud()
    transformed_pcd.points = pcd.points
    #o3d.visualization.draw_geometries([pcd])
    transformed_pcd.paint_uniform_color([0, 0, 1])  # Blue
    transformed_pcd.transform(transformation_matrix)
    #o3d.visualization.draw_geometries([transformed_pcd])
    # Visualize the point clouds
    #o3d.visualization.draw_geometries([transformed_pcd, pcd])
    return transformed_pcd

# Function to save the transformed point cloud to a new directory
def save_pcd(pcd, output_dir, output_filename):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, output_filename)
    o3d.io.write_point_cloud(output_path, pcd)
    print(f"Transformed point cloud saved to: {output_path}")

# Callable function to read, transform, save, and visualize a point cloud
def process_point_cloud(input_pcd, transformation_matrix, output_directory, output_filename):
    point_cloud = o3d.io.read_point_cloud(input_pcd)
    transformed_point_cloud = transform_point_cloud(point_cloud, transformation_matrix)
    save_pcd(transformed_point_cloud, output_directory, output_filename)
