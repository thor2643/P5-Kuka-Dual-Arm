#include "geometry_msgs/msg/pose.hpp"
#include "moveit/move_group_interface/move_group_interface.h"
#include "rclcpp/rclcpp.hpp"
#include "project_interfaces/srv/plan_move_command.hpp"
#include "project_interfaces/srv/execute_move_command.hpp"


class RobotControllerService : public rclcpp::Node{
public:
  RobotControllerService() : Node("robot_controller_service") {
    // Configure node
    //auto node_ptr = this->shared_from_this();
    this->declare_parameter("robot_name", "dual_arm");
    auto robot_name = this->get_parameter("robot_name").as_string();

    // Create the options for the MoveGroupInterface
    moveit::planning_interface::MoveGroupInterface::Options right_options("right_arm", "robot_description", robot_name);
    moveit::planning_interface::MoveGroupInterface::Options left_options("left_arm", "robot_description", robot_name);
    
    // Pass the options and the shared pointer of the current node
    move_group_interface_right = std::make_shared<moveit::planning_interface::MoveGroupInterface>(std::make_shared<rclcpp::Node>(this->get_name()), right_options);
    move_group_interface_left = std::make_shared<moveit::planning_interface::MoveGroupInterface>(std::make_shared<rclcpp::Node>(this->get_name()), left_options);

    planner_service_ = this->create_service<project_interfaces::srv::PlanMoveCommand>(
        "plan_move_command", std::bind(&RobotControllerService::handle_planner_service, this, std::placeholders::_1, std::placeholders::_2));

    execute_service_ = this->create_service<project_interfaces::srv::ExecuteMoveCommand>(
        "execute_move_command", std::bind(&RobotControllerService::handle_execute_service, this, std::placeholders::_1, std::placeholders::_2));
  }

private:
  std::string robot_name_;
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface_right;
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface_left;
  rclcpp::Service<project_interfaces::srv::PlanMoveCommand>::SharedPtr planner_service_;
  rclcpp::Service<project_interfaces::srv::ExecuteMoveCommand>::SharedPtr execute_service_;
  moveit::planning_interface::MoveGroupInterface::Plan plan_;

  bool plan_available_ = false;

  // Callback to plan the trajectory to the target pose
  void handle_planner_service(const std::shared_ptr<project_interfaces::srv::PlanMoveCommand::Request> request,
                      const std::shared_ptr<project_interfaces::srv::PlanMoveCommand::Response> response) {
    geometry_msgs::msg::Pose target_pose;

    RCLCPP_INFO(this->get_logger(), "Received request to plan move to target pose");

    target_pose.orientation.x = request->orientation.x; //0.707; //request->orientation.x;
    target_pose.orientation.y = request->orientation.y; //0.707; //request->orientation.y;
    target_pose.orientation.z = request->orientation.z; //0; //request->orientation.z;
    target_pose.orientation.w = request->orientation.w; //0; //request->orientation.w;
    target_pose.position.x = request->position.x; // Example usage of request data
    target_pose.position.y = request->position.y;
    target_pose.position.z = request->position.z;

    move_group_interface_right->setPoseTarget(target_pose);

    auto error_code = move_group_interface_right->plan(plan_);

    if (error_code == moveit::core::MoveItErrorCode::SUCCESS) {
      RCLCPP_INFO(this->get_logger(), "The trajectory has been planned succesfully");
      plan_available_ = true;
      response->result = true;
    } else {
      RCLCPP_ERROR(this->get_logger(), "Failed to plan to target pose");
      response->result = false;
      response->log = "Failed to plan to target pose";
    }
  }

  // Callback to execute the planned trajectory
  void handle_execute_service(const std::shared_ptr<project_interfaces::srv::ExecuteMoveCommand::Request> request,
                      const std::shared_ptr<project_interfaces::srv::ExecuteMoveCommand::Response> response) {
    
    RCLCPP_INFO(this->get_logger(), "Received request to execute planned trajectory");

    if (plan_available_)
    {
      RCLCPP_INFO(this->get_logger(), "The planned trajectory is being executed");
      move_group_interface_right->execute(plan_);
      RCLCPP_INFO(this->get_logger(), "The plan has been executed");
      plan_available_ = false;
      response->success = true;
      response->log = "The plan has been executed";
    } else {
      RCLCPP_ERROR(this->get_logger(), "No plan available to execute");
      response->success = false;
      response->log = "No plan available to execute";
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

