#include "geometry_msgs/msg/pose.hpp"
#include "sensor_msgs/msg/joint_state.hpp"
#include "moveit/move_group_interface/move_group_interface.h"
#include "moveit/robot_state/robot_state.h"
#include "moveit/robot_model_loader/robot_model_loader.h"
#include "rclcpp/rclcpp.hpp"
#include "project_interfaces/srv/plan_move_command.hpp"
#include "project_interfaces/srv/execute_move_command.hpp"
#include "project_interfaces/srv/get_current_pose.hpp"
//include <moveit_visual_tools/moveit_visual_tools.h>
#include <string>
#include <sstream>

using namespace Eigen;

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

    // Fix bug in MoveGroupInterface
    ee_link_right = move_group_interface_right->getEndEffectorLink();
    ee_link_left = move_group_interface_left->getEndEffectorLink();


    RCLCPP_INFO(this->get_logger(), "End effector link for right arm: %s", ee_link_right.c_str());
    RCLCPP_INFO(this->get_logger(), "End effector link for left arm: %s", ee_link_left.c_str());

    auto current_pose_right = move_group_interface_right->getCurrentPose(ee_link_right);
    auto current_pose_left = move_group_interface_left->getCurrentPose(ee_link_left);

    RCLCPP_INFO(this->get_logger(), "Current position for right arm: x=%f, y=%f, z=%f", 
          current_pose_right.pose.position.x, 
          current_pose_right.pose.position.y, 
          current_pose_right.pose.position.z);

    RCLCPP_INFO(this->get_logger(), "Current position for left arm: x=%f, y=%f, z=%f", 
          current_pose_left.pose.position.x, 
          current_pose_left.pose.position.y, 
          current_pose_left.pose.position.z);

    //getPoseReferenceFrame = move_group_interface_right->getPoseReferenceFrame();
    //RCLCPP_INFO(this->get_logger(), "Received request to plan a trajectory");
       
    // Pass the options and the shared pointer of the current node
    planner_service = this->create_service<project_interfaces::srv::PlanMoveCommand>(
        "plan_move_command", std::bind(&RobotControllerService::handle_planner_service, this, std::placeholders::_1, std::placeholders::_2));

    execute_service = this->create_service<project_interfaces::srv::ExecuteMoveCommand>(
        "execute_move_command", std::bind(&RobotControllerService::handle_execute_service, this, std::placeholders::_1, std::placeholders::_2));

    get_pose_service = this->create_service<project_interfaces::srv::GetCurrentPose>(
        "get_pose", std::bind(&RobotControllerService::handle_pose_request_service, this, std::placeholders::_1, std::placeholders::_2));

    joint_state_subscriber = this->create_subscription<sensor_msgs::msg::JointState>(
      "joint_states", 10, std::bind(&RobotControllerService::joint_state_callback, this, std::placeholders::_1));

    // Print the pose
    //RCLCPP_INFO(this->get_logger(), "End effector pose:\n%s", end_effector_state.matrix().format(Eigen::IOFormat()).c_str());
  }

private:
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface_right;
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_interface_left;

  rclcpp::Service<project_interfaces::srv::PlanMoveCommand>::SharedPtr planner_service;
  rclcpp::Service<project_interfaces::srv::ExecuteMoveCommand>::SharedPtr execute_service;
  rclcpp::Service<project_interfaces::srv::GetCurrentPose>::SharedPtr get_pose_service;
  rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr joint_state_subscriber;
  moveit::planning_interface::MoveGroupInterface::Plan plan_right;
  moveit::planning_interface::MoveGroupInterface::Plan plan_left;
  const moveit::core::JointModelGroup* joint_model_group_right;
  const moveit::core::JointModelGroup* joint_model_group_left;
  moveit::core::RobotModelPtr kinematic_model;

  sensor_msgs::msg::JointState::SharedPtr current_joint_state;

  std::string ee_link_right;
  std::string ee_link_left;

  bool plan_available_right = false;
  bool plan_available_left = false;

  std::vector<double> joint_values_right;
  std::vector<double> joint_values_left;
  
  void joint_state_callback(const sensor_msgs::msg::JointState::SharedPtr msg)
    {
        //current_joint_state = msg->position;
        joint_values_right.clear();
        joint_values_left.clear();

        joint_values_right.resize(7);
        joint_values_left.resize(7);

        for (size_t i = 0; i < msg->name.size(); ++i) {
            if (msg->name[i].find("right_") != std::string::npos) {
              if (msg->name[i] == "right_A1") joint_values_right[0] = msg->position[i];
              else if (msg->name[i] == "right_A2") joint_values_right[1] = msg->position[i];
              else if (msg->name[i] == "right_A3") joint_values_right[2] = msg->position[i];
              else if (msg->name[i] == "right_A4") joint_values_right[3] = msg->position[i];
              else if (msg->name[i] == "right_A5") joint_values_right[4] = msg->position[i];
              else if (msg->name[i] == "right_A6") joint_values_right[5] = msg->position[i];
              else if (msg->name[i] == "right_A7") joint_values_right[6] = msg->position[i];

            } else if (msg->name[i].find("left_") != std::string::npos) {
              if (msg->name[i] == "left_A1") joint_values_left[0] = msg->position[i];
              else if (msg->name[i] == "left_A2") joint_values_left[1] = msg->position[i];
              else if (msg->name[i] == "left_A3") joint_values_left[2] = msg->position[i];
              else if (msg->name[i] == "left_A4") joint_values_left[3] = msg->position[i];
              else if (msg->name[i] == "left_A5") joint_values_left[4] = msg->position[i];
              else if (msg->name[i] == "left_A6") joint_values_left[5] = msg->position[i];
              else if (msg->name[i] == "left_A7") joint_values_left[6] = msg->position[i];
            }
        }
    }

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
    /*
    moveit_msgs::msg::JointConstraint joint_constraint1;
    joint_constraint1.joint_name = (*linkArray)[0]; // The first joint
    joint_constraint1.position = 0.0;       // Center of the allowed range
    joint_constraint1.tolerance_above = 0;  // +0 degrees in radians
    joint_constraint1.tolerance_below = 2.9;  // -170 degrees in radians
    joint_constraint1.weight = 1.0;         // Weight of the constraint
    // We add joint constraints to the generic constraints
    constraints.joint_constraints.push_back(joint_constraint1);
    
    
    moveit_msgs::msg::JointConstraint joint_constraint2;
    joint_constraint2.joint_name = (*linkArray)[1]; // The second joint
    joint_constraint2.position = 0.0;    // Center of the allowed range
    joint_constraint2.tolerance_above = 0;  // +0 degrees in radians
    joint_constraint2.tolerance_below = 2; // -120 degrees in radians
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

    /*
    moveit_msgs::msg::JointConstraint joint_constraint5;
    joint_constraint5.joint_name = (*linkArray)[4]; // The fifth joint
    joint_constraint5.position = 0.0;       // Center of the allowed range
    joint_constraint5.tolerance_above = 1.57;  // +90 degrees in radians
    joint_constraint5.tolerance_below = 1.57;  // -90 degrees in radians
    joint_constraint5.weight = 1.0;         // Weight of the constraint
    constraints.joint_constraints.push_back(joint_constraint5);
    */
    
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

    // Cartesian path planning
    std::vector<geometry_msgs::msg::Pose> waypoints;
    waypoints.push_back(target_pose);

    double eef_step = 0.005;  // Step size for end-effector
    double jump_threshold = 5.0; // If the jump is bigger than this, it will be considered invalid
    moveit_msgs::msg::RobotTrajectory trajectory;

    // Fraction is how big a precentage of the path that was successfully planned
    double fraction = move_group_interface->computeCartesianPath(
    waypoints,           // Waypoints to follow
    eef_step,            // Step size
    jump_threshold,      // Jump threshold
    trajectory           // Resulting trajectory
    );

    moveit::core::MoveItErrorCode error_code;
    move_group_interface->setMaxVelocityScalingFactor(0.05); // Set the maximum velocity scaling factor (10% of the maximum speed)
    if (fraction > 0.95) {
      RCLCPP_INFO(this->get_logger(), "Cartesian path computed successfully");
      plan->trajectory_ = trajectory;
    } else {
      RCLCPP_ERROR(this->get_logger(), "Failed to compute Cartesian path, uisng planner instead");

      // Applying planner configurations and constraints
      //move_group_interface.setEndEffectorLink("3f_tool"); // Do not set this, depends on the arm
      move_group_interface->setPlanningTime(59);
      move_group_interface->setPlannerId("RRT"); // Other options in ompl_planning.yaml
      move_group_interface->setStartStateToCurrentState(); // Ensure that the planner has the current state of the robot
      move_group_interface->setPathConstraints(constraints);
      move_group_interface->setMaxAccelerationScalingFactor(0.1); // Set the maximum acceleration scaling factor (10% of the maximum acceleration)
      move_group_interface->setPoseTarget(target_pose);
  
      error_code = move_group_interface->plan(*plan);
    }

    if (error_code == moveit::core::MoveItErrorCode::SUCCESS || fraction > 0.95) {
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

  //TODO: Make moveit actually listen to the joint_states topic to make the function below work
  //Alternatively as suggested by a student assistent, listen to the tf topic and calculate the joint states from the tf topic
  /*
  void handle_pose_request_service(const std::shared_ptr<project_interfaces::srv::GetCurrentPose::Request> request,
                      const std::shared_ptr<project_interfaces::srv::GetCurrentPose::Response> response) {
    RCLCPP_INFO(this->get_logger(), "Received request to get current pose for %s arm", request->arm.c_str());

    // Check if the request is for the right or left arm
    if (request->arm == "right") {
      move_group_interface_right->setStartStateToCurrentState();
      geometry_msgs::msg::PoseStamped current_pose = move_group_interface_right->getCurrentPose(ee_link_right); // The end effector link for the right arm

      std::vector<double> joint_values = move_group_interface_right->getCurrentJointValues();	

      for (size_t i = 0; i < joint_values.size(); ++i) {
        RCLCPP_INFO(this->get_logger(), "Joint %zu: %f", i, joint_values[i]);
      }

      response->pose = current_pose.pose;
      response->success = true;
      RCLCPP_INFO(this->get_logger(), "Current pose retrieved successfully");

    } else if (request->arm == "left") {
      geometry_msgs::msg::PoseStamped current_pose = move_group_interface_left->getCurrentPose(ee_link_left); // The end effector link for the left arm

      std::vector<double> joint_values = move_group_interface_left->getCurrentJointValues();	

      for (size_t i = 0; i < joint_values.size(); ++i) {
        RCLCPP_INFO(this->get_logger(), "Joint %zu: %f", i, joint_values[i]);
      }

      response->pose = current_pose.pose;
      response->success = true;
      RCLCPP_INFO(this->get_logger(), "Current pose retrieved successfully");
    } else {
      RCLCPP_ERROR(this->get_logger(), "Invalid arm specified");
      response->log = "Invalid arm specified";
      response->success = false;
      return;
    }
    }
    */
    
    void handle_pose_request_service(const std::shared_ptr<project_interfaces::srv::GetCurrentPose::Request> request,
                      const std::shared_ptr<project_interfaces::srv::GetCurrentPose::Response> response) {
      Matrix4d pose;

      if (request->arm == "left") {
          pose = forward_kinematics_left(joint_values_left);
          RCLCPP_INFO(this->get_logger(), "Calculated pose for left arm");
      } else if (request->arm == "right") {
          pose = forward_kinematics_right(joint_values_right);
          RCLCPP_INFO(this->get_logger(), "Calculated pose for right arm");
      } else {
          RCLCPP_ERROR(this->get_logger(), "Invalid arm specified. Use 'left' or 'right'.");
          response->success = false;
          response->log = "Invalid arm specified. Use 'left' or 'right'.";
          return;
      }

      RCLCPP_INFO(this->get_logger(), "Parsing the pose to the response message");
      response->pose.position.x = pose(0, 3);
      response->pose.position.y = pose(1, 3);
      response->pose.position.z = pose(2, 3);

      RCLCPP_INFO(this->get_logger(), "Position: x=%f, y=%f, z=%f", response->pose.position.x, response->pose.position.y, response->pose.position.z);

      Quaterniond q(pose.block<3,3>(0,0));
      response->pose.orientation.x = q.x();
      response->pose.orientation.y = q.y();
      response->pose.orientation.z = q.z();
      response->pose.orientation.w = q.w();

      RCLCPP_INFO(this->get_logger(), "Orientation: x=%f, y=%f, z=%f, w=%f", response->pose.orientation.x, response->pose.orientation.y, response->pose.orientation.z, response->pose.orientation.w);

      response->success = true;

      return;
    }     

    Matrix4d transformation_matrix(Vector3d rpy, Vector3d xyz) {
    double roll = rpy(0), pitch = rpy(1), yaw = rpy(2);
    //double x = xyz(0), y = xyz(1), z = xyz(2);

    Matrix3d Rx, Ry, Rz;

    Rx << 1, 0, 0,
          0, cos(roll), -sin(roll),
          0, sin(roll), cos(roll);

    Ry << cos(pitch), 0, sin(pitch),
          0, 1, 0,
          -sin(pitch), 0, cos(pitch);

    Rz << cos(yaw), -sin(yaw), 0,
          sin(yaw), cos(yaw), 0,
          0, 0, 1;

    Matrix3d R = Rz * Ry * Rx;

    Matrix4d T = Matrix4d::Identity();
    T.block<3,3>(0,0) = R;
    T.block<3,1>(0,3) = xyz;

    return T;
  }

  Matrix4d forward_kinematics_left(const std::vector<double>& joint_angles) {
    Matrix4d T_mount_left = transformation_matrix(Vector3d(-0.785398163, 0, -1.57079633), Vector3d(0.711114, 0.756691, 1.037203));
    Matrix4d T_left_A1 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0, 0.1475));
    Matrix4d T_left_A2 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, -0.0105, 0.1925));
    Matrix4d T_left_A3 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0105, 0.2075));
    Matrix4d T_left_A4 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0105, 0.1925));
    Matrix4d T_left_A5 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, -0.0105, 0.2075));
    Matrix4d T_left_A6 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, -0.0707, 0.1925));
    Matrix4d T_left_A7 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0707, 0.091));
    Matrix4d T_left_joint_ee = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0, 0, 0.035));

    Matrix4d R_left_A1 = transformation_matrix(Vector3d(0, 0, joint_angles[0]), Vector3d(0, 0, 0));
    Matrix4d R_left_A2 = transformation_matrix(Vector3d(0, joint_angles[1], 0), Vector3d(0, 0, 0));
    Matrix4d R_left_A3 = transformation_matrix(Vector3d(0, 0, joint_angles[2]), Vector3d(0, 0, 0));
    Matrix4d R_left_A4 = transformation_matrix(Vector3d(0, -joint_angles[3], 0), Vector3d(0, 0, 0));
    Matrix4d R_left_A5 = transformation_matrix(Vector3d(0, 0, joint_angles[4]), Vector3d(0, 0, 0));
    Matrix4d R_left_A6 = transformation_matrix(Vector3d(0, joint_angles[5], 0), Vector3d(0, 0, 0));
    Matrix4d R_left_A7 = transformation_matrix(Vector3d(0, 0, joint_angles[6]), Vector3d(0, 0, 0));

    Matrix4d T = T_mount_left * T_left_A1 * R_left_A1 * T_left_A2 * R_left_A2 * T_left_A3 * R_left_A3 * T_left_A4 * R_left_A4 * T_left_A5 * R_left_A5 * T_left_A6 * R_left_A6 * T_left_A7 * R_left_A7 * T_left_joint_ee;

    return T;
  }

  Matrix4d forward_kinematics_right(const std::vector<double>& joint_angles) {
    Matrix4d T_mount_right = transformation_matrix(Vector3d(0.785398163, 0, -1.57079633), Vector3d(0.268524, 0.756691, 1.037203));
    Matrix4d T_right_A1 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0, 0.1475));
    Matrix4d T_right_A2 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, -0.0105, 0.1925));
    Matrix4d T_right_A3 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0105, 0.2075));
    Matrix4d T_right_A4 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0105, 0.1925));
    Matrix4d T_right_A5 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, -0.0105, 0.2075));
    Matrix4d T_right_A6 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, -0.0707, 0.1925));
    Matrix4d T_right_A7 = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0.0, 0.0707, 0.091));
    Matrix4d T_right_joint_ee = transformation_matrix(Vector3d(0, 0, 0), Vector3d(0, 0, 0.035));

    Matrix4d R_right_A1 = transformation_matrix(Vector3d(0, 0, joint_angles[0]), Vector3d(0, 0, 0));
    Matrix4d R_right_A2 = transformation_matrix(Vector3d(0, joint_angles[1], 0), Vector3d(0, 0, 0));
    Matrix4d R_right_A3 = transformation_matrix(Vector3d(0, 0, joint_angles[2]), Vector3d(0, 0, 0));
    Matrix4d R_right_A4 = transformation_matrix(Vector3d(0, -joint_angles[3], 0), Vector3d(0, 0, 0));
    Matrix4d R_right_A5 = transformation_matrix(Vector3d(0, 0, joint_angles[4]), Vector3d(0, 0, 0));
    Matrix4d R_right_A6 = transformation_matrix(Vector3d(0, joint_angles[5], 0), Vector3d(0, 0, 0));
    Matrix4d R_right_A7 = transformation_matrix(Vector3d(0, 0, joint_angles[6]), Vector3d(0, 0, 0));

    Matrix4d T = T_mount_right * T_right_A1 * R_right_A1 * T_right_A2 * R_right_A2 * T_right_A3 * R_right_A3 * T_right_A4 * R_right_A4 * T_right_A5 * R_right_A5 * T_right_A6 * R_right_A6 * T_right_A7 * R_right_A7 * T_right_joint_ee;

    return T;
  }

};


int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<RobotControllerService>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
