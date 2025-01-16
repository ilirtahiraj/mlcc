import os
import numpy as np
import pickle
from scipy.spatial.transform import Rotation as R

# Function to create homogeneous calibration matrix
def create_homogeneous_matrix(tx, ty, tz, qw, qx, qy, qz):
    # Create rotation matrix from quaternion
    rotation_matrix = R.from_quat([qx, qy, qz, qw]).as_matrix()

    # Create homogeneous transformation matrix
    homogeneous_matrix = np.eye(4)
    homogeneous_matrix[:3, :3] = rotation_matrix
    homogeneous_matrix[:3, 3] = [tx, ty, tz]

    return homogeneous_matrix

# Main script to scan folders and process the space-separated files
calibration_matrices = []

for i in range(1, 101):
    folder_name = f"scene{i}"
    file_path = os.path.join(folder_name, "ref.json")

    # Check if the file exists
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            # Read space-separated values from the file
            values = list(map(float, file.readline().strip().split()))
            
            # Extract calibration parameters
            tx, ty, tz = values[:3]
            qw, qx, qy, qz = values[3:]

            # Generate the homogeneous calibration matrix
            calibration_matrix = create_homogeneous_matrix(tx, ty, tz, qw, qx, qy, qz)

            # Store the matrix in the dictionary
            calibration_matrices.append(calibration_matrix)

# Save the calibration matrices to a pickle file
with open("calibration_matrices_curve.pkl", "wb") as pickle_file:
    pickle.dump(calibration_matrices, pickle_file)

print("Calibration matrices saved to calibration_matrices.pkl")

# Load the pickle file and print the first calibration matrix
with open("calibration_matrices_curve.pkl", "rb") as pickle_file:
    loaded_matrices = pickle.load(pickle_file)

# # Print the first calibration matrix
# if loaded_matrices:
#     first_scene = list(loaded_matrices.keys())[0]  # Get the first scene key
#     print(f"First calibration matrix ({first_scene}):\n{loaded_matrices[first_scene]}")
# else:
#     print("No calibration matrices were loaded.")
