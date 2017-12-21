#!/usr/bin/env python
import sys
import logging
from  birl_skill_management.interface import build_skill, execute_skill
import rospy
import ipdb
import moveit_commander

logger = logging.getLogger("birl_motion_library")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch) 

def move_to_too_right_pose():
    import sys
    import copy
    import rospy
    import moveit_commander
    import moveit_msgs.msg
    import geometry_msgs.msg
    robot = moveit_commander.RobotCommander()
    group = moveit_commander.MoveGroupCommander("right_arm")

    name = ['head_nod', 'head_pan', 'left_e0', 'left_e1', 'left_s0', 'left_s1', 'left_w0', 'left_w1', 'left_w2', 'right_e0', 'right_e1', 'right_s0', 'right_s1', 'right_w0', 'right_w1', 'right_w2', 'torso_t0']
    position = (0.0, -0.07631554419729933, -1.1861506442323961, 1.9381847254932203, -0.07784952498518474, -0.9978545025194616, 0.6676651379271263, 1.0281506230801987, -0.49816026086578813, 0.31101460474376763, 1.3502865885361355, 0.5380437613508089, -0.7535680620487095, -0.26000974354657763, 0.9713933339284383, 0.059825250727531136, -12.565987119160338) 
    d = dict(zip(name, position))

    group_variable_values = [d[k] for k in group.get_active_joints()]
    group.set_joint_value_target(group_variable_values)
    plan = group.plan()
    group.execute(plan, wait=True)
    raw_input()
    

if __name__ == "__main__":
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node("test_dmp_skill_build_and_exec", anonymous=True)

    dataset_path = '/home/sklaw/Desktop/experiment/birl/data_for_or_from_HMM/baxter_pick_and_place_data/real_baxter_mini_pnp_v_2/extracted_anomalies_dir/20171204165831.345227/dataset_of_resampled_DTWed_lfd_dir/'
    control_mode = 'pose'
    list_of_new_skill_id = build_skill(dataset_path, control_mode, "anomaly_recovery_skill", "dmp") 
    logger.info("list_of_new_skill_id: %s"%(list_of_new_skill_id,))

    logger.info("click to exec")
    raw_input()
    
    move_to_too_right_pose()
    execute_skill("anomaly_recovery_skill_label_1")
