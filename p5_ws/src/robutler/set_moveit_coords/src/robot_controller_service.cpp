#include "geometry_msgs/msg/pose.hpp"
#include "moveit/move_group_interface/move_group_interface.h"
#include "rclcpp/rclcpp.hpp"
#include "project_interfaces/srv/plan_move_command.hpp"
#include "project_interfaces/srv/execute_move_command.hpp"
#//include <moveit_visual_tools/moveit_visual_tools.h>
#include <string>


class RobotControllerService : public rclcpp::Node{
public:
  RobotControllerService() : Node("robot_controller_service") {
    this->declare_parameter<std::string>("model", "default_model");
    std::string model;
    this->get_parameter("model", model);

    RCLCPP_INFO(this->get_logger(), "Creating MoveGroupInterface for right arm");
    moveit::planning_interface::MoveGroupInterface::Options options_right("right_arm", "robot_description", "");   
    move_group_interface_right = std::make_shared<moveit::planning_interface::MoveGroupInterface>(std::make_shared<rclcpp::Node>(this->get_name()), options_right);  

    RCLCPP_INFO(this->get_logger(), "Creating MoveGroupInterface for left arm");
    moveit::planning_interface::MoveGroupInterface::Options options_left("left_arm", "robot_description", "");
    move_group_interface_left = std::make_shared<moveit::planning_interface::MoveGroupInterface>(std::make_shared<rclcpp::Node>(this->get_name()), options_left);
       
    // Pass the options and the shared pointer of the current node
    planner_service = this->create_service<project_interfaces::srv::PlanMoveCommand>(
        "plan_move_command", std::bind(&RobotControllerService::handle_planner_service, this, std::placeholders::_1, std::placeholders::_2));

    execute_service = this->create_service<project_interfaces::srv::ExecuteMoveCommand>(
        "execute_move_command", std::bind(&RobotControllerService::handle_execute_service, this, std::placeholders::_1, std::placeholders::_2));
  }

private:
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface_right;
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface_left;
  rclcpp::Service<project_interfaces::srv::PlanMoveCommand>::SharedPtr planner_service;
  rclcpp::Service<project_interfaces::srv::ExecuteMoveCommand>::SharedPtr execute_service;
  moveit::planning_interface::MoveGroupInterface::Plan plan_right;
  moveit::planning_interface::MoveGroupInterface::Plan plan_left;

  bool plan_available_right = false;
  bool plan_available_left = false;

  // Callback to plan the trajectory to the target pose
  void handle_planner_service(const std::shared_ptr<project_interfaces::srv::PlanMoveCommand::Request> request,
                      const std::shared_ptr<project_interfaces::srv::PlanMoveCommand::Response> response) {

    RCLCPP_INFO(this->get_logger(), "Received request to plan a trajectory");

    std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface;
    moveit::planning_interface::MoveGroupInterface::Plan *plan;
    bool *plan_available;
    
    // Joint names
    std::string right_array[7] = {"right_A1", "right_A2", "right_A3", "right_A4", "right_A5", "right_A6", "right_A7"};
    std::string left_array[7] = {"left_A1", "left_A2", "left_A3", "left_A4", "left_A5", "left_A6", "left_A7"};
    // Pointer to point to the chosen array
    std::string (*linkArray)[7] = nullptr;

    // Check if the request is for the right or left arm
    if (request->arm == "right") {
      RCLCPP_INFO(this->get_logger(), "Planning for right arm");
      move_group_interface = move_group_interface_right;
      plan = &plan_right;
      plan_available = &plan_available_right;
      linkArray = &right_array;
    } else if (request->arm == "left") {
      RCLCPP_INFO(this->get_logger(), "Planning for left arm");
      move_group_interface = move_group_interface_left;
      plan = &plan_left;
      plan_available = &plan_available_left;
      linkArray = &left_array;
    } else {
      RCLCPP_ERROR(this->get_logger(), "Invalid arm specified");
      response->log = "Invalid arm specified";
      response->success = false;
      return;
    }

    // --- Constraint the planner so the end effector link (3f_tool0) is always inside a box ---
    // Link to this code: https://moveit.picknik.ai/main/doc/how_to_guides/using_ompl_constrained_planning/ompl_constrained_planning.html
    moveit_msgs::msg::PositionConstraint box_constraint;
    box_constraint.header.frame_id = move_group_interface->getPoseReferenceFrame(); // This is the link world, as set in the xacro.
    box_constraint.link_name = move_group_interface->getEndEffectorLink(); // Find the end effector link for planner group, which is 3f_tool0 for right arm, and (2f_tool0?) for left arm

    // Create the box and set its dimensions
    shape_msgs::msg::SolidPrimitive box;
    box.type = shape_msgs::msg::SolidPrimitive::BOX;  
    box.dimensions = { 1, 0.667, 1.2 };
    box_constraint.constraint_region.primitives.emplace_back(box);

    // Set position of the box 
    geometry_msgs::msg::Pose box_pose; 
    box_pose.position.x = 0.465;
    box_pose.position.y = 0.2995;
    box_pose.position.z = 1.40945;
    box_pose.orientation.w = 1; 
    box_constraint.constraint_region.primitive_poses.emplace_back(box_pose); // The box position is at it's center
    box_constraint.weight = 1.0;

    // We make a generic constraint, and add box_constraint to the position_constraints.
    moveit_msgs::msg::Constraints constraints;
    constraints.position_constraints.emplace_back(box_constraint);

    // Visualize the box constraint
    /*
    auto moveit_visual_tools = moveit_visual_tools::MoveItVisualTools{ node_ptr, "world", rviz_visual_tools::RVIZ_MARKER_TOPIC, move_group_interface.getRobotModel()};
    Eigen::Vector3d box_point_1(box_pose.position.x - box.dimensions[0] / 2, box_pose.position.y - box.dimensions[1] / 2,
                                box_pose.position.z - box.dimensions[2] / 2);
    Eigen::Vector3d box_point_2(box_pose.position.x + box.dimensions[0] / 2, box_pose.position.y + box.dimensions[1] / 2,
                                box_pose.position.z + box.dimensions[2] / 2);
    moveit_visual_tools.publishCuboid(box_point_1, box_point_2, rviz_visual_tools::TRANSLUCENT_DARK);
    moveit_visual_tools.trigger();
    */

    // --- Set joint constraints ---    
    moveit_msgs::msg::JointConstraint joint_constraint1;
    joint_constraint1.joint_name = (*linkArray)[0]; // The first joint
    joint_constraint1.position = 0.0;       // Center of the allowed range
    joint_constraint1.tolerance_above = 1.57;  // +90 degrees in radians
    joint_constraint1.tolerance_below = 1.57;  // -90 degrees in radians
    joint_constraint1.weight = 1.0;         // Weight of the constraint
    // We add joint constraints to the generic constraints
    constraints.joint_constraints.push_back(joint_constraint1);
    
    /*
    moveit_msgs::msg::JointConstraint joint_constraint2;
    joint_constraint2.joint_name = (*linkArray)[2]; // The second joint
    joint_constraint2.position = 0.0;    // Center of the allowed range
    joint_constraint2.tolerance_above = 2.0943951;  // +120 degrees in radians
    joint_constraint2.tolerance_below = 0.174532925; // -10 degrees in radians
    joint_constraint2.weight = 1.0;         // Weight of the constraint
    constraints.joint_constraints.push_back(joint_constraint2);
    */
    
        
    /*
    moveit_msgs::msg::JointConstraint joint_constraint4;
    joint_constraint4.joint_name = "A4"; // The fourth joint
    joint_constraint4.position = 0.0;       // Center of the allowed range
    joint_constraint4.tolerance_above = 0.87;  // +50 degrees in radians
    joint_constraint4.tolerance_below = 0.87;  // -50 degrees in radians
    joint_constraint4.weight = 1.0;         // Weight of the constraint
    constraints.joint_constraints.push_back(joint_constraint4);
    */

    moveit_msgs::msg::JointConstraint joint_constraint5;
    joint_constraint5.joint_name = (*linkArray)[4]; // The fifth joint
    joint_constraint5.position = 0.0;       // Center of the allowed range
    joint_constraint5.tolerance_above = 1.57;  // +90 degrees in radians
    joint_constraint5.tolerance_below = 1.57;  // -90 degrees in radians
    joint_constraint5.weight = 1.0;         // Weight of the constraint
    constraints.joint_constraints.push_back(joint_constraint5);
    
    /*
    moveit_msgs::msg::JointConstraint joint_constraint6;
    joint_constraint6.joint_name = "A6"; // The sixth joint
    joint_constraint6.position = 0.0;       // Center of the allowed range
    joint_constraint6.tolerance_above = 1.57;  // +90 degrees in radians
    joint_constraint6.tolerance_below = 1.57;  // -90 degrees in radians
    joint_constraint6.weight = 1.0;         // Weight of the constraint
    constraints.joint_constraints.push_back(joint_constraint6);
    */

    geometry_msgs::msg::Pose target_pose;
    target_pose.orientation.x = request->orientation.x; //0.707; //request->orientation.x;
    target_pose.orientation.y = request->orientation.y; //0.707; //request->orientation.y;
    target_pose.orientation.z = request->orientation.z; //0; //request->orientation.z;
    target_pose.orientation.w = request->orientation.w; //0; //request->orientation.w;
    target_pose.position.x = request->position.x; // Example usage of request data
    target_pose.position.y = request->position.y;
    target_pose.position.z = request->position.z;

    // Applying planner configurations and constraints
    //move_group_interface.setEndEffectorLink("3f_tool"); // Do not set this, depends on the arm
    move_group_interface->setPlanningTime(59);
    move_group_interface->setPlannerId("TRRT"); // Other options in ompl_planning.yaml
    move_group_interface->setStartStateToCurrentState(); // Ensure that the planner has the current state of the robot
    move_group_interface->setPathConstraints(constraints);
    move_group_interface->setMaxVelocityScalingFactor(0.10); // Set the maximum velocity scaling factor (10% of the maximum speed)
    move_group_interface->setMaxAccelerationScalingFactor(0.1); // Set the maximum acceleration scaling factor (10% of the maximum acceleration)
    move_group_interface->setPoseTarget(target_pose);
  
    moveit::core::MoveItErrorCode error_code;
    error_code = move_group_interface->plan(*plan);

    if (error_code == moveit::core::MoveItErrorCode::SUCCESS) {
      RCLCPP_INFO(this->get_logger(), "The trajectory has been planned succesfully");
      *plan_available = true;
      response->log = "The trajectory has been planned succesfully";
      response->success = true;
    } else {
      RCLCPP_ERROR(this->get_logger(), "Failed to plan to target pose");
      response->log = "Failed to plan to target pose";
      response->success = false;
    }
  }

  // Callback to execute the planned trajectory
  void handle_execute_service(const std::shared_ptr<project_interfaces::srv::ExecuteMoveCommand::Request> request,
                      const std::shared_ptr<project_interfaces::srv::ExecuteMoveCommand::Response> response) {
    
    RCLCPP_INFO(this->get_logger(), "Received request to execute planned trajectory for %s arm", request->arm.c_str());

    std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface;
    moveit::planning_interface::MoveGroupInterface::Plan *plan;
    bool *plan_available;

    // Check if the request is for the right or left arm
    if (request->arm == "right") {
      RCLCPP_INFO(this->get_logger(), "Planning for right arm");
      move_group_interface = move_group_interface_right;
      plan = &plan_right;
      plan_available = &plan_available_right;
    } else if (request->arm == "left") {
      RCLCPP_INFO(this->get_logger(), "Planning for left arm");
      move_group_interface = move_group_interface_left;
      plan = &plan_left;
      plan_available = &plan_available_left;
    } else {
      RCLCPP_ERROR(this->get_logger(), "Invalid arm specified");
      response->log = "Invalid arm specified";
      response->success = false;
      return;
    }

    if (*plan_available)
    {
      RCLCPP_INFO(this->get_logger(), "The planned trajectory is being executed");

      move_group_interface->execute(*plan);

      RCLCPP_INFO(this->get_logger(), "The plan has been executed");
      *plan_available = false;
      response->success = true;
    } else {
      RCLCPP_ERROR(this->get_logger(), "No plan available for %s arm", request->arm.c_str());
      response->log = "No plan available for " + request->arm + " arm";
      response->success = false;
    }

  }
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<RobotControllerService>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}