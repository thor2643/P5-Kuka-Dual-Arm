# P5-Kuka-Dual-Arm
This is a fifth semester project, which proposes an integration of a Large Language Model to make automation more intuitive for operators.

## Contributors
This project was developed by group 565 on Aalborg University, Robot Technology at 5rd semester.

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

<section id="quick_start">
## Quick Start
1. Install ROS 2 development tools

    ```shell
    sudo apt install ros-dev-tools
    ```

2. Create a workspace, clone, and install dependencies

    ```shell
    source /opt/ros/humble/setup.bash
    export FRI_CLIENT_VERSION=1.15
    mkdir -p lbr-stack/src && cd lbr-stack
    vcs import src --input https://raw.githubusercontent.com/lbr-stack/lbr_fri_ros2_stack/humble/lbr_fri_ros2_stack/repos-fri-${FRI_CLIENT_VERSION}.yaml
    rosdep install --from-paths src -i -r -y
    ```
