cmake_minimum_required(VERSION 3.22)
project(set_moveit_coords)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(rclcpp REQUIRED)
find_package(lbr_description REQUIRED)

add_executable(set_moveit_coords src/set_moveit_coords.cpp)

ament_target_dependencies(set_moveit_coords
  geometry_msgs  
  moveit_ros_planning_interface
  rclcpp
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

install(TARGETS set_moveit_coords
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
