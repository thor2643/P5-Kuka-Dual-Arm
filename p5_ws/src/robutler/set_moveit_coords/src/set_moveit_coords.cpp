#include "moveit/move_group_interface/move_group_interface.h"
#include <moveit_visual_tools/moveit_visual_tools.h>
//#include <graph_msgs/msg/geometry_graph.hpp>
#include "rclcpp/rclcpp.hpp"
#include <thread>



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

  //move_group_interface.setEndEffectorLink("3f_palm_finger_2_joint");
  move_group_interface.setPlannerId("RRTstar");


  // Spin rviz
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(node_ptr);
  auto spinner = std::thread([&executor]() { executor.spin(); });
  
  // --- Constraint the planner so the end effector link (3f_tool0) is always inside a box ---
  // Link to this code: https://moveit.picknik.ai/main/doc/how_to_guides/using_ompl_constrained_planning/ompl_constrained_planning.html
  moveit_msgs::msg::PositionConstraint box_constraint;
  box_constraint.header.frame_id = move_group_interface.getPoseReferenceFrame(); // This is the link world, as set in the xacro.
  box_constraint.link_name = move_group_interface.getEndEffectorLink(); // Find the end effector link for right_arm, which is 3f_tool0

  // Create the box and set its dimensions
  shape_msgs::msg::SolidPrimitive box;
  box.type = shape_msgs::msg::SolidPrimitive::BOX;  
  box.dimensions = { 1, 0.667, 1.5 };
  box_constraint.constraint_region.primitives.emplace_back(box);

  // Set position of the box 
  geometry_msgs::msg::Pose box_pose; // 
  box_pose.position.x = 0.465;
  box_pose.position.y = 0.2995;
  box_pose.position.z = 1.5595;
  box_pose.orientation.w = 1; 
  box_constraint.constraint_region.primitive_poses.emplace_back(box_pose); // The box position is at it's center
  box_constraint.weight = 1.0;

  // We create a generic Constraints message and add our box_constraint to the position_constraints.
  moveit_msgs::msg::Constraints box_constraints;
  box_constraints.position_constraints.emplace_back(box_constraint);

   // Visualize the box constraint
  auto moveit_visual_tools = moveit_visual_tools::MoveItVisualTools{ node_ptr, "world", rviz_visual_tools::RVIZ_MARKER_TOPIC, move_group_interface.getRobotModel()};
  Eigen::Vector3d box_point_1(box_pose.position.x - box.dimensions[0] / 2, box_pose.position.y - box.dimensions[1] / 2,
                              box_pose.position.z - box.dimensions[2] / 2);
  Eigen::Vector3d box_point_2(box_pose.position.x + box.dimensions[0] / 2, box_pose.position.y + box.dimensions[1] / 2,
                              box_pose.position.z + box.dimensions[2] / 2);

  //moveit_visual_tools.publishCuboid(box_point_1, box_point_2, rviz_visual_tools::TRANSLUCENT_DARK);
  moveit_visual_tools.trigger();

  // --- Set a target pose right_arm, placing 3f_tool0 here --- 
  geometry_msgs::msg::Pose target_pose;
  target_pose.orientation.w = 1.0;
  target_pose.position.x = 0;
  target_pose.position.y = 0.5;
  target_pose.position.z = 1.5;
  move_group_interface.setPoseTarget(target_pose);
  
  // -- Create a plan to that target pose -- 
  moveit::planning_interface::MoveGroupInterface::Plan plan;
  
  // Print the planner parameters
  std::map<std::string, std::string> planer_params = move_group_interface.getPlannerParams("right_arm", "RRTstar");
  for (const auto &param : planer_params)
    {
        RCLCPP_INFO(node_ptr->get_logger(), "Parameter: %s, Value: %s", param.first.c_str(), param.second.c_str());
    }

  //move_group_interface.setPathConstraints(box_constraints); // Apply the box constraint to the planner
  //move_group_interface.setPlanningTime(10.0); // The box constraint adds calculation time to the planner
  auto error_code = move_group_interface.plan(plan);

  if (error_code == moveit::core::MoveItErrorCode::SUCCESS) {
    // Execute the plannode_ptr->get_logger()->info("The plan is now executed");
    RCLCPP_INFO(node_ptr->get_logger(), "\nThe plan is now executed\n");
    //move_group_interface.execute(plan);
    RCLCPP_INFO(node_ptr->get_logger(), "\nThe plan has been executed\n");
  } else {
    RCLCPP_ERROR(node_ptr->get_logger(), "Failed to plan to target pose");
  }

  // Shutdown ROS
  rclcpp::shutdown();  // <--- This will cause the spin function in the thread to return
  spinner.join();  // <--- Join the thread before exiting
  return 0;
}
