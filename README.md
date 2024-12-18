# P5-Kuka-Dual-Arm
This project, developed during our fifth semester at AAU, explores the integration of a large language model (LLM) to make automation more intuitive for operators. The GitHub contains all the code produced throughout the project period, from September 1st to December 20th, and allows for the use of an LLM to control two Kuka LBR iiwa 7 R800 robots.

The LLM is capable of the following:
- Detecting LEGO bricks using a RealSense D435i camera, with either traditional computer vision or YOLO-World.
- Planning and executing trajectories to any point defined by Cartesian coordinates and roll-pitch-yaw parameters [𝑥,𝑦,𝑧,𝑟,z,𝑦].
- Performing pick-and-place tasks using the attached grippers. NOTE: The code is built for a RobotIQ 3-F Gripper and a RobotIQ 2-F 85 Gripper.
- Informing operators about its capabilities.
- Providing insights into errors encountered during operation.

## Quick Start
This quick-start guide assumes a clean installation of Ubuntu 22.04 LTS (Jammy Jellyfish) along with ROS 2 Humble. If either is not yet set up, you can refer to the following resources:
- [Ubuntu 22.04 LTS](https://medium.com/@maheshdeshmukh22/how-to-install-ubuntu-22-04-lts-on-virtualbox-in-windows-11-6c259ce8ef60)
- [ROS2 - Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)

If your system crashes or you need to switch terminals at any point, ensure you re-run the following command:

    source /opt/ros/humble/setup.bash
    
Before starting the installation of this project, we recommend grabbing a snack and a beverage. The process will take at least 30 minutes.

1. Install ROS 2 development tools

    ```shell
    sudo apt install ros-dev-tools
    ```

2. Create a workspace, clone, and install dependencies

    ```shell
    cd ~
    source /opt/ros/humble/setup.bash
    git clone https://github.com/thor2643/P5-Kuka-Dual-Arm.git
    cd P5-Kuka-Dual-Arm/p5_ws
    sudo rosdep init
    rosdep update
    rosdep install --from-paths src -i -r -y
    ```

3. Installing colcon mixin and pip (Needed for Moveit2)

    ```shell
    sudo apt install python3-colcon-common-extensions
    sudo apt install python3-colcon-mixin
    sudo apt install python3-pip
    sudo apt-get install portaudio19-dev python-all-dev
    colcon mixin add default https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml
    colcon mixin update default
    sudo apt install python3-vcstool
    ```

4. Installing python libraries

    ```shell
    cd ~/P5-Kuka-Dual-Arm
    pip install -r requirements.txt
    ```

5. Adding an API key for Janise

   ```shell
    cd ~/P5-Kuka-Dual-Arm/p5_ws/src/robutler/janise
    nano API_KEY.json
    # Added your API Key for GPT following the format
    # {
    #     "API_KEY": "Insert your API Key here"
    # }
    # Remember to write the file, ctrl + s then ctrl + x
    ```

6. Colcon build - Re-run if any packages timeout during compile

    ```shell
    cd ~/P5-Kuka-Dual-Arm/p5_ws
    export MAKEFLAGS="-j3"
    colcon build --mixin release
    ```
 
8. NOTE: If you are running on our setup, remember to set your IP to 172.31.1.148 and Netmask to 255.255.255.0, also ensure that you are correctly connected to the setup (2 USB's 1 Ethernet). ([Static IP configuration](https://linuxconfig.org/how-to-configure-static-ip-address-on-ubuntu-22-04-jammy-jellyfish-desktop-server))
   
9. Running the system

    ```shell
    cd ~/P5-Kuka-Dual-Arm/p5_ws
    source install/setup.bash
    ros2 launch robutler_bringup robutler.launch.py
    ```
    
10. Recommendations - *Don't do this, if you run multiple ROS Distros*

    ```shell
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
    echo "source ~/P5-Kuka-Dual-Arm/p5_ws/install/setup.bash" >> ~/.bashrc
    ```

## Contributors
This project was developed by group 565 at Aalborg University, during the 5th semester of Robot Technology. Every member of the group can be found listed below, alongside their GitHub pages:

<section id="sec_contributors">
<table>
  <tr> 
    <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/Gustav-Bay"><img src="https://avatars.githubusercontent.com/u/120191982?v=4" width="100px;" alt=""/><br/><sub><b>Gustav Bay Baastrup</b></sub></a></br><a href="gttps://github.com/Gustav-Bay" title="">🤖</a></td>
    <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/thor2643"><img src="https://avatars.githubusercontent.com/u/66319719?v=4" width="100px;" alt=""/><br/><sub><b>Thor Iversen</b></sub></a></br><a href="gttps://github.com/thor2643" title="">👨‍🌾</a></td>
    <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/xdKazer"><img src="https://avatars.githubusercontent.com/u/116707938?v=4" width="100px;" alt=""/><br/><sub><b>Kasper Lauritsen</b></sub></a></br><a href="gttps://github.com/xdKazer" title="">🎥</a></td>
    <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/silasjensen2001"><img src="https://avatars.githubusercontent.com/u/54105795?v=4" width="100px;" alt=""/><br/><sub><b>Silas Jensen</b></sub></a></br><a href="gttps://github.com/silasjensen2001" title="">😎</a></td>
    <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/DaMalle"><img src="https://avatars.githubusercontent.com/u/58878411?v=4" width="100px;" alt=""/><br/><sub><b>Marcus Friis</b></sub></a></br><a href="gttps://github.com/DaMalle" title="">🤠</a></td>
    <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/signeskuldbol"><img src="https://avatars.githubusercontent.com/u/117270262?v=4" width="100px;" alt=""/><br/><sub><b>Signe Møller-Skuldbøl</b></sub></a></br><a href="gttps://github.com/signeskuldbol" title="">🌸</a></td>
  </tr>
</table>
