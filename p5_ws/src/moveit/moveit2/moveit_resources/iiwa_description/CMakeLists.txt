cmake_minimum_required(VERSION 3.5)
project(iiwa_description)
find_package(ament_cmake REQUIRED)

ament_package()

install(DIRECTORY meshes urdf DESTINATION share/${PROJECT_NAME})
