//Misc dep
#include <cstdio>
#include <memory>

// Ros dep
#include <rclcpp/rclcpp.hpp>
#include <thread>

// Move it dep
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit_visual_tools/moveit_visual_tools.h>

// Math 
#include <tf2/LinearMath/Quaternion.h>

int main(int argc, char * argv[])
{
  // Initialize ROS and create the Node
  rclcpp::init(argc, argv);
  auto const node = std::make_shared<rclcpp::Node>("send_cudes",
  rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true));

  // Create a ROS logger
  auto const logger = rclcpp::get_logger("send_cudes");
  
  RCLCPP_INFO(logger, "This message will be logged every time.");
  
  // We spin up a SingleThreadedExecutor so MoveItVisualTools interact with ROS
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(node);
  auto spinner = std::thread([&executor]() { executor.spin(); });

  // Create the MoveIt MoveGroup Interface
  using moveit::planning_interface::MoveGroupInterface;
  auto move_group_interface = MoveGroupInterface(node, "kuka_left");
   
  // Chnage moveit parameters 
  //move_group_interface.setPlannerId("RRTstar");
  //move_group_interface.setPlanningTime(10.0); 

  // Set a target Pose
  auto const target_pose = []{
    /*
    geometry_msgs::msg::Pose msg;

    // Set position in XYZ
    msg.position.x = 0.2;
    msg.position.y = 0.4;
    msg.position.z = 1.0;

    // Convert RPY (roll, pitch, yaw) to quaternion
    tf2::Quaternion q;
    double roll = 0.0;  // Set roll value
    double pitch = 0.0; // Set pitch value
    double yaw = 0.0;   // Set yaw value
    q.setRPY(roll, pitch, yaw);

    // Set the orientation in quaternion form
    msg.orientation.x = q.x();
    msg.orientation.y = q.y();
    msg.orientation.z = q.z();
    msg.orientation.w = q.w();
    return msg;
    */
    
    geometry_msgs::msg::Pose msg;
    msg.orientation.w = 1.0;
    msg.position.x = 0;
    msg.position.y = 0.5;
    msg.position.z = 1.8;
    return msg;
  }();
  
  move_group_interface.setPoseTarget(target_pose);
  
  
  // Construct and initialize MoveItVisualTools  
  auto moveit_visual_tools = moveit_visual_tools::MoveItVisualTools{node, "kuka_1_mount", rviz_visual_tools::RVIZ_MARKER_TOPIC, move_group_interface.getRobotModel()};
  moveit_visual_tools.deleteAllMarkers();
  moveit_visual_tools.loadRemoteControl();
  
  // Create a closures for visualization
  auto const draw_title = [&moveit_visual_tools](auto text) {
    auto const text_pose = [] {
      auto msg = Eigen::Isometry3d::Identity();
      msg.translation().z() = 1.0;
      return msg;
    }();
    moveit_visual_tools.publishText(text_pose, text, rviz_visual_tools::WHITE,rviz_visual_tools::XLARGE);                            
  };
  
  auto const prompt = [&moveit_visual_tools](auto text) {
  moveit_visual_tools.prompt(text);
  };
  	
  auto const draw_trajectory_tool_path =
    [&moveit_visual_tools,jmg = move_group_interface.getRobotModel()->getJointModelGroup("kuka_left")](auto const trajectory) {moveit_visual_tools.publishTrajectoryLine(trajectory, jmg);
  };
  
  // Create a plan to that target pose
  prompt("Press 'Next' in the RvizVisualToolsGui window to plan");
  draw_title("Planning");
  moveit_visual_tools.trigger();
  
  auto const [success, plan] = [&move_group_interface]{
    moveit::planning_interface::MoveGroupInterface::Plan msg;
    auto const ok = static_cast<bool>(move_group_interface.plan(msg));
    return std::make_pair(ok, msg);
  }();

  // Execute the plan
  if (success) {
    draw_trajectory_tool_path(plan.trajectory_);
    moveit_visual_tools.trigger();
    prompt("Press 'Next' in the RvizVisualToolsGui window to execute");
    draw_title("Executing");
    moveit_visual_tools.trigger();
    move_group_interface.execute(plan);
  } else {
    draw_title("Planning Failed!");
    moveit_visual_tools.trigger();
    RCLCPP_ERROR(logger, "Planing failed!");
  }

  // Shutdown ROS
  rclcpp::shutdown();  // <--- This will cause the spin function in the thread to return
  spinner.join();  // <--- Join the thread before exiting
  return 0;
}
