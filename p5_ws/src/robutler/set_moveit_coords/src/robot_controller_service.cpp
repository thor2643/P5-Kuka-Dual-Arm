#include "geometry_msgs/msg/pose.hpp"
#include "moveit/move_group_interface/move_group_interface.h"
#include "rclcpp/rclcpp.hpp"
#include "project_interfaces/srv/move_command.hpp"


class RobotControllerService : public rclcpp::Node{
public:
  RobotControllerService() : Node("robot_controller_service") {
    // Configure node
    //auto node_ptr = this->shared_from_this();
    this->declare_parameter("robot_name", "iiwa7_table");
    auto robot_name = this->get_parameter("robot_name").as_string();

    // Create the options for the MoveGroupInterface
    moveit::planning_interface::MoveGroupInterface::Options options("right_arm", "robot_description", robot_name);
    
    // Pass the options and the shared pointer of the current node
    move_group_interface_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(std::make_shared<rclcpp::Node>(this->get_name()), options);

    service_ = this->create_service<project_interfaces::srv::MoveCommand>(
        "move_command", std::bind(&RobotControllerService::handle_service, this, std::placeholders::_1, std::placeholders::_2));
  }

private:
  std::string robot_name_;
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface_;
  rclcpp::Service<project_interfaces::srv::MoveCommand>::SharedPtr service_;

  void handle_service(const std::shared_ptr<project_interfaces::srv::MoveCommand::Request> request,
                      const std::shared_ptr<project_interfaces::srv::MoveCommand::Response> response) {
    geometry_msgs::msg::Pose target_pose;

    RCLCPP_INFO(this->get_logger(), "Received request to move to target pose");

    target_pose.orientation.x = request->orientation.x; //0.707; //request->orientation.x;
    target_pose.orientation.y = request->orientation.y; //0.707; //request->orientation.y;
    target_pose.orientation.z = request->orientation.z; //0; //request->orientation.z;
    target_pose.orientation.w = request->orientation.w; //0; //request->orientation.w;
    target_pose.position.x = request->position.x; // Example usage of request data
    target_pose.position.y = request->position.y;
    target_pose.position.z = request->position.z;

    move_group_interface_->setPoseTarget(target_pose);

    moveit::planning_interface::MoveGroupInterface::Plan plan;
    auto error_code = move_group_interface_->plan(plan);

    if (error_code == moveit::core::MoveItErrorCode::SUCCESS) {
      RCLCPP_INFO(this->get_logger(), "The plan is now executed");
      move_group_interface_->execute(plan);
      RCLCPP_INFO(this->get_logger(), "The plan has been executed");
      response->result = true;
    } else {
      RCLCPP_ERROR(this->get_logger(), "Failed to plan to target pose");
      response->result = false;
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

