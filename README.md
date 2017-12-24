# birl_motion_library

## How to run scripts/test_dmp_skill_build_and_exec.py

1. Install [birl_baxter_dmp](https://github.com/birlrobotics/birl_baxter_dmp). To test installation, make sure the following command runs successfully
  
    ```sh
    rosrun birl_baxter_dmp demo.py
    ```

1. Launch sim/real baxter

1. Enable the robot
  
    ```sh
   rosrun baxter_tools enable_robot.py -e
   ```

1. Launch moveit
  
    ```sh
    rosrun baxter_interface joint_trajectory_action_server.py
    rosrun birl_motion_library joint_states_topic_rewriter.py 
    roslaunch baxter_moveit_config baxter_grippers.launch
    ```

1. In the pop-up rviz, add a Marker in DIsplay panel

1. To make IK easier, move baxter arms to neutral poses
  
   ```sh
   rosrun baxter_examples joint_velocity_wobbler.py
   Ctrl+C
    ```

1. Download [our dataset repo](https://github.com/birlrobotics/birl_dataset)

1. Fix [the dataset path in the script](https://github.com/birlrobotics/birl_motion_library/blob/master/scripts/test_dmp_skill_build_and_exec.py#L42) so that it points to the same folder in the dataset repo

1. Run the script
  
   ```sh
   rosrun birl_motion_library test_dmp_skill_build_and_exec.py
   ```

