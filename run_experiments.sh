#!/bin/bash

# Define the range of scene numbers
START_SCENE=1
END_SCENE=1

# Docker container and image settings
DOCKER_IMAGE="mlcc:edgar"
CONTAINER_NAME="ros_mlcc_container"

# Path to the ROS package on the host
HOST_PATH_TO_MLCC="/home/ilirtahiraj/code/mlcc"
CONTAINER_PATH="/catkin_ws/src/mlcc"

# Three different launch files with respective timeouts
declare -A LAUNCH_TIMEOUTS=(
  ["pose_refine.launch"]=15
  ["extrinsic_refine.launch"]=75
  ["global.launch"]=90
)

# Function to run Docker with specified scene and launch file
run_docker() {
  local SCENE_NUMBER=$1
  local LAUNCH_FILE=$2
  local TIME_LIMIT=$3
  echo "Starting Docker for scene number: $SCENE_NUMBER using launch file: $LAUNCH_FILE with timeout: $TIME_LIMIT seconds"

  # Start Docker in the background
  docker run --rm -d \
    --name $CONTAINER_NAME \
    --network host \
    --privileged \
    -v /home/ilirtahiraj/code/mlcc:/dev_ws/catkin_ws/src/mlcc \
    $DOCKER_IMAGE \
    bash -c "source catkin_ws/devel/setup.bash && roslaunch mlcc $LAUNCH_FILE scene_number:=$SCENE_NUMBER"

  # Sleep for the specified time limit
  sleep $TIME_LIMIT

  # After the sleep, stop the container by sending a SIGINT (Ctrl+C) to the ROS process
  echo "Time limit reached, sending SIGINT to stop the container..."

  # Send SIGINT (Ctrl+C) to the roslaunch process (PID 1 in the container)
  docker exec $CONTAINER_NAME kill -2 1  # Sends SIGINT to process with PID 1

  # Wait for the container to stop
  docker wait $CONTAINER_NAME

  # Show logs from the container
  echo "Logs from the Docker container:"
  docker logs $CONTAINER_NAME

  # Ensure the container is stopped
  echo "Stopping any lingering containers..."
  docker stop $CONTAINER_NAME 2>/dev/null || true
  docker kill $CONTAINER_NAME 2>/dev/null || true

  echo "Docker container stopped successfully."
}

# Loop through each scene number
for SCENE_NUMBER in $(seq $START_SCENE $END_SCENE); do
  echo "Processing scene number: $SCENE_NUMBER"

  # Loop through each launch file for the current scene number
  for LAUNCH_FILE in "${!LAUNCH_TIMEOUTS[@]}"; do
    TIME_LIMIT=${LAUNCH_TIMEOUTS[$LAUNCH_FILE]}
    run_docker $SCENE_NUMBER $LAUNCH_FILE $TIME_LIMIT

    echo "Completed launch file: $LAUNCH_FILE for scene number: $SCENE_NUMBER"
  done

  echo "Completed all launch files for scene number: $SCENE_NUMBER"
done

echo "All scenes processed."