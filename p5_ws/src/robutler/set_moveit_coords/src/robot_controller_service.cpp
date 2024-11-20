#include "geometry_msgs/msg/pose.hpp"
#include "moveit/move_group_interface/move_group_interface.h"
#include "rclcpp/rclcpp.hpp"
#include "project_interfaces/srv/plan_move_command.hpp"
#include "project_interfaces/srv/execute_move_command.hpp"



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

    geometry_msgs::msg::Pose target_pose;
    target_pose.orientation.x = request->orientation.x; //0.707; //request->orientation.x;
    target_pose.orientation.y = request->orientation.y; //0.707; //request->orientation.y;
    target_pose.orientation.z = request->orientation.z; //0; //request->orientation.z;
    target_pose.orientation.w = request->orientation.w; //0; //request->orientation.w;
    target_pose.position.x = request->position.x; // Example usage of request data
    target_pose.position.y = request->position.y;
    target_pose.position.z = request->position.z;


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