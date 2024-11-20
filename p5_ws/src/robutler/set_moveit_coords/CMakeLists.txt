cmake_minimum_required(VERSION 3.22)
project(set_moveit_coords)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# find dependencies
find_package(rclcpp REQUIRED)
find_package(ament_cmake REQUIRED)
find_package(project_interfaces REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(moveit_visual_tools REQUIRED)
find_package(graph_msgs REQUIRED)

add_executable(set_moveit_coords src/set_moveit_coords.cpp)
add_executable(robot_controller_service src/robot_controller_service.cpp)

ament_target_dependencies(set_moveit_coords
  geometry_msgs  
  moveit_ros_planning_interface
  moveit_visual_tools
  rclcpp
)

ament_target_dependencies(robot_controller_service
  geometry_msgs  
  moveit_ros_planning_interface
  project_interfaces
  rclcpp
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

install(TARGETS robot_controller_service
  DESTINATION lib/${PROJECT_NAME}
)

install(TARGETS set_moveit_coords 
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
