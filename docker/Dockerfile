FROM ros:noetic

ENV ROS_DISTRO=noetic
ENV DEBIAN_FRONTEND=noninteractive

# Base setup
RUN apt-get update && \
    apt-get install -y software-properties-common locales && \
    add-apt-repository universe

RUN locale-gen en_US en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

ENV LANG=en_US.UTF-8

# Create a non-root user
ARG USERNAME=local
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && apt-get update \
  && apt-get install -y sudo \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
  && chmod 0440 /etc/sudoers.d/$USERNAME \
  && rm -rf /var/lib/apt/lists/* \
  && echo "source /usr/share/bash-completion/completions/git" >> /home/$USERNAME/.bashrc


RUN apt-get update \
  && apt-get install --no-install-recommends -y software-properties-common gnupg ca-certificates ros-noetic-cv-bridge\
  && add-apt-repository ppa:apt-fast/stable \
  && apt-get update \
  && apt-get install --no-install-recommends -y apt-fast \
  && apt-fast clean \
  && rm -rf /var/lib/apt/lists/*

RUN echo debconf apt-fast/maxdownloads string 16 | debconf-set-selections && \
  echo debconf apt-fast/dlflag boolean true | debconf-set-selections && \
  echo debconf apt-fast/aptmanager string apt-get | debconf-set-selections


RUN apt-fast update \
  && apt-fast install -y --no-install-recommends \
  git wget nano vim libomp-dev build-essential python3-pip python-is-python3


RUN apt-fast install -y --no-install-recommends \
  ros-${ROS_DISTRO}-eigen-conversions \
  ros-${ROS_DISTRO}-pcl-ros \
  ros-${ROS_DISTRO}-rviz \
  ros-${ROS_DISTRO}-tf2-geometry-msgs \
  ros-${ROS_DISTRO}-tf2-sensor-msgs \
  ros-${ROS_DISTRO}-diagnostic-updater \
  ros-${ROS_DISTRO}-roslint \
  ros-${ROS_DISTRO}-topic-tools \
  ros-${ROS_DISTRO}-ros-numpy

RUN pip install pyrsistent==0.15 \
  && pip install open3d==0.10


RUN sudo apt-get install -y libceres-dev 
RUN sudo apt-get install -y libopencv-dev 

# Create and build the workspace
RUN mkdir -p /dev_ws/catkin_ws/src
WORKDIR /dev_ws/catkin_ws/src
RUN git clone https://github.com/ilirtahiraj/mlcc.git
WORKDIR /dev_ws/catkin_ws

RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && catkin_make -DCMAKE_BUILD_TYPE=Release"

# Configure workspace sourcing
RUN sed -i "6i source \"/dev_ws/catkin_ws/devel/setup.bash\"" /ros_entrypoint.sh

WORKDIR /dev_ws
ENV QT_DEBUG_PLUGINS=1
CMD ["bash"]
