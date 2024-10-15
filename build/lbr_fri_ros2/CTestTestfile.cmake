# CMake generated Testfile for 
# Source directory: /home/gustav/P5-Kuka-Dual-Arm/p5_ws/src/lbr_fri_ros2_stack/lbr_fri_ros2
# Build directory: /home/gustav/P5-Kuka-Dual-Arm/build/lbr_fri_ros2
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test([=[test_command_interfaces]=] "/usr/bin/python3" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/gustav/P5-Kuka-Dual-Arm/build/lbr_fri_ros2/test_results/lbr_fri_ros2/test_command_interfaces.gtest.xml" "--package-name" "lbr_fri_ros2" "--output-file" "/home/gustav/P5-Kuka-Dual-Arm/build/lbr_fri_ros2/ament_cmake_gtest/test_command_interfaces.txt" "--command" "/home/gustav/P5-Kuka-Dual-Arm/build/lbr_fri_ros2/test_command_interfaces" "--gtest_output=xml:/home/gustav/P5-Kuka-Dual-Arm/build/lbr_fri_ros2/test_results/lbr_fri_ros2/test_command_interfaces.gtest.xml")
set_tests_properties([=[test_command_interfaces]=] PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/gustav/P5-Kuka-Dual-Arm/build/lbr_fri_ros2/test_command_interfaces" TIMEOUT "60" WORKING_DIRECTORY "/home/gustav/P5-Kuka-Dual-Arm/build/lbr_fri_ros2" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/gustav/P5-Kuka-Dual-Arm/p5_ws/src/lbr_fri_ros2_stack/lbr_fri_ros2/CMakeLists.txt;87;ament_add_gtest;/home/gustav/P5-Kuka-Dual-Arm/p5_ws/src/lbr_fri_ros2_stack/lbr_fri_ros2/CMakeLists.txt;0;")
subdirs("gtest")
