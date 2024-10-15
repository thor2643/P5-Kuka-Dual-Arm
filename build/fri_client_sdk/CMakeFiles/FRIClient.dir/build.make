# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/gustav/P5-Kuka-Dual-Arm/p5_ws/src/fri

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk

# Include any dependencies generated for this target.
include CMakeFiles/FRIClient.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/FRIClient.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/FRIClient.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/FRIClient.dir/flags.make

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp.o: CMakeFiles/FRIClient.dir/flags.make
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp.o: FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp.o: CMakeFiles/FRIClient.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp.o -MF CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp.o.d -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp.o -c /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp > CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp.i

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp.s

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp.o: CMakeFiles/FRIClient.dir/flags.make
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp.o: FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp.o: CMakeFiles/FRIClient.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp.o -MF CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp.o.d -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp.o -c /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp > CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp.i

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp.s

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp.o: CMakeFiles/FRIClient.dir/flags.make
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp.o: FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp.o: CMakeFiles/FRIClient.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp.o -MF CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp.o.d -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp.o -c /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp > CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp.i

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp.s

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp.o: CMakeFiles/FRIClient.dir/flags.make
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp.o: FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp.o: CMakeFiles/FRIClient.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp.o -MF CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp.o.d -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp.o -c /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp > CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp.i

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp.s

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp.o: CMakeFiles/FRIClient.dir/flags.make
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp.o: FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp.o: CMakeFiles/FRIClient.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building CXX object CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp.o -MF CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp.o.d -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp.o -c /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp > CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp.i

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp.s

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp.o: CMakeFiles/FRIClient.dir/flags.make
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp.o: FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp.o: CMakeFiles/FRIClient.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Building CXX object CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp.o -MF CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp.o.d -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp.o -c /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp > CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp.i

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp.s

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp.o: CMakeFiles/FRIClient.dir/flags.make
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp.o: FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp.o: CMakeFiles/FRIClient.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "Building CXX object CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp.o -MF CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp.o.d -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp.o -c /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp > CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp.i

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp.s

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp.o: CMakeFiles/FRIClient.dir/flags.make
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp.o: FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp.o: CMakeFiles/FRIClient.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "Building CXX object CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp.o -MF CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp.o.d -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp.o -c /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp > CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp.i

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp.s

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c.o: CMakeFiles/FRIClient.dir/flags.make
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c.o: FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c.o: CMakeFiles/FRIClient.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/CMakeFiles --progress-num=$(CMAKE_PROGRESS_9) "Building C object CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c.o -MF CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c.o.d -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c.o -c /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c > CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c.i

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c.s

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c.o: CMakeFiles/FRIClient.dir/flags.make
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c.o: FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c.o: CMakeFiles/FRIClient.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/CMakeFiles --progress-num=$(CMAKE_PROGRESS_10) "Building C object CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c.o -MF CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c.o.d -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c.o -c /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c > CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c.i

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c.s

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c.o: CMakeFiles/FRIClient.dir/flags.make
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c.o: FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c.o: CMakeFiles/FRIClient.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/CMakeFiles --progress-num=$(CMAKE_PROGRESS_11) "Building C object CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c.o -MF CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c.o.d -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c.o -c /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c > CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c.i

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c.s

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c.o: CMakeFiles/FRIClient.dir/flags.make
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c.o: FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c
CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c.o: CMakeFiles/FRIClient.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/CMakeFiles --progress-num=$(CMAKE_PROGRESS_12) "Building C object CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c.o -MF CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c.o.d -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c.o -c /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c > CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c.i

CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c -o CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c.s

# Object files for target FRIClient
FRIClient_OBJECTS = \
"CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp.o" \
"CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp.o" \
"CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp.o" \
"CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp.o" \
"CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp.o" \
"CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp.o" \
"CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp.o" \
"CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp.o" \
"CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c.o" \
"CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c.o" \
"CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c.o" \
"CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c.o"

# External object files for target FRIClient
FRIClient_EXTERNAL_OBJECTS =

libFRIClient.so: CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/base/friClientApplication.cpp.o
libFRIClient.so: CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRClient.cpp.o
libFRIClient.so: CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRCommand.cpp.o
libFRIClient.so: CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_lbr/friLBRState.cpp.o
libFRIClient.so: CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/client_trafo/friTransformationClient.cpp.o
libFRIClient.so: CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/connection/friUdpConnection.cpp.o
libFRIClient.so: CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friCommandMessageEncoder.cpp.o
libFRIClient.so: CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/friMonitoringMessageDecoder.cpp.o
libFRIClient.so: CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf/pb_frimessages_callbacks.c.o
libFRIClient.so: CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/protobuf_gen/FRIMessages.pb.c.o
libFRIClient.so: CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_decode.c.o
libFRIClient.so: CMakeFiles/FRIClient.dir/FRI-Client-SDK_Cpp/src/nanopb-0.2.8/pb_encode.c.o
libFRIClient.so: CMakeFiles/FRIClient.dir/build.make
libFRIClient.so: CMakeFiles/FRIClient.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/CMakeFiles --progress-num=$(CMAKE_PROGRESS_13) "Linking CXX shared library libFRIClient.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/FRIClient.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/FRIClient.dir/build: libFRIClient.so
.PHONY : CMakeFiles/FRIClient.dir/build

CMakeFiles/FRIClient.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/FRIClient.dir/cmake_clean.cmake
.PHONY : CMakeFiles/FRIClient.dir/clean

CMakeFiles/FRIClient.dir/depend:
	cd /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/gustav/P5-Kuka-Dual-Arm/p5_ws/src/fri /home/gustav/P5-Kuka-Dual-Arm/p5_ws/src/fri /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk /home/gustav/P5-Kuka-Dual-Arm/build/fri_client_sdk/CMakeFiles/FRIClient.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/FRIClient.dir/depend

