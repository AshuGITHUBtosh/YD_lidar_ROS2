cd lidar_ws

ros2 launch ydlidar_ros2_driver slam_with_lidar.launch.py

NEW TERMINAL

ros2 launch ydlidar_ros2_driver slam_with_lidar.launch.py

NEW terminal

ros2 run slam_toolbox sync_slam_toolbox_node   --ros-args   -p scan_topic:=/scan   -p use_odom:=false   -p base_frame:=base_link   -p odom_frame:=odom   -p map_frame:=map   -p resolution:=0.05   -p mode:=mapping


NEW TERMINAL

rviz2
choose fixed frame=map
by topic add =map
laser scan=/scan
