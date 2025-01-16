import matplotlib.pyplot as plt

# Path to the pose file
file_path = '/home/ilirtahiraj/code/mlcc/scene1/original_pose/4.json'
file_path = '/home/ilirtahiraj/code/mlcc/scene1/pose.json'

# Read the file
with open(file_path, 'r') as f:
    lines = f.readlines()

# Lists to store x and y values
x_vals = []
y_vals = []

# Process each line
for line in lines:
    # Split each line by spaces and convert to float
    values = line.split()
    
    # Ensure the line has enough values (at least two)
    if len(values) > 1:
        # Append the first value to x_vals and the second to y_vals
        x_vals.append(float(values[0]))
        y_vals.append(float(values[1]))

# Create a figure and subplots (1 row, 3 columns)
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# Plot the original x-y plot
axs[0].plot(x_vals, y_vals, marker='o', linestyle='-', color='b')
axs[0].set_title('X-Y Plot')
axs[0].set_xlabel('X values')
axs[0].set_ylabel('Y values')
axs[0].grid(True)

# Plot the x values
axs[1].plot(x_vals, marker='o', linestyle='-', color='g')
axs[1].set_title('X Values')
axs[1].set_xlabel('Index')
axs[1].set_ylabel('X values')
axs[1].grid(True)

# Plot the y values
axs[2].plot(y_vals, marker='o', linestyle='-', color='r')
axs[2].set_title('Y Values')
axs[2].set_xlabel('Index')
axs[2].set_ylabel('Y values')
axs[2].grid(True)

# Adjust layout to prevent overlap
plt.tight_layout()

# Display the plots
plt.show()
