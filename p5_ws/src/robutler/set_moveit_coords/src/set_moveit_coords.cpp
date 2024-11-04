#include "geometry_msgs/msg/pose.hpp"
#include "moveit/move_group_interface/move_group_interface.h"
#include "rclcpp/rclcpp.hpp"

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);

  // Configure node
  auto node_ptr = rclcpp::Node::make_shared("set_moveit_coords");
  node_ptr->declare_parameter("robot_name", "iiwa7_table");
  auto robot_name = node_ptr->get_parameter("robot_name").as_string();

  // Create MoveGroupInterface (lives inside robot_name namespace)
  auto move_group_interface = moveit::planning_interface::MoveGroupInterface(
      node_ptr, moveit::planning_interface::MoveGroupInterface::Options("right_arm", "robot_description",
                                                                        robot_name));
                                                                        
  // Set a target pose
  geometry_msgs::msg::Pose target_pose;
  target_pose.orientation.w = 1.0;
  target_pose.position.x = 0;
  target_pose.position.y = 0.5;
  target_pose.position.z = 1.8;
  move_group_interface.setPoseTarget(target_pose);

  // Create a plan to that target pose
  moveit::planning_interface::MoveGroupInterface::Plan plan;
  auto error_code = move_group_interface.plan(plan);
  // RCLCPP_INFO(node_ptr->get_logger(), "\nThe plan is now executed\n");

  if (error_code == moveit::core::MoveItErrorCode::SUCCESS) {
    // Execute the plannode_ptr->get_logger()->info("The plan is now executed");
    RCLCPP_INFO(node_ptr->get_logger(), "\nThe plan is now executed\n");
    move_group_interface.execute(plan);
    RCLCPP_INFO(node_ptr->get_logger(), "\nThe plan has been executed\n");
  } else {
    RCLCPP_ERROR(node_ptr->get_logger(), "Failed to plan to target pose");
  }

  rclcpp::shutdown();
  return 0;
}
