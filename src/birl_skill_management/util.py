import logging
import moveit_commander
import moveit_msgs.msg 
import sys
import rospy
from geometry_msgs.msg import (
    Pose,
)
from visualization_msgs.msg import (
    Marker
)

logger = logging.getLogger("birl_motion_library."+__name__)
logger.setLevel(logging.INFO)

def get_list_of_interested_column_name(list_of_column_name, control_mode):
    import re
    if control_mode == 'pose':
        prog = re.compile(ur".*(pose).*")
    else:
        raise Exception("control_mode \"%s\" is not supported now."%(control_mode,))

    ret = []
    for i in list_of_column_name:
        if prog.match(i):
            ret.append(i)
    return ret


def get_eval_postfix(control_dimensions, control_mode):
    import re
    prog = re.compile(ur".*%s(.*)"%(control_mode,))
    list_of_postfix = []
    for i in control_dimensions:
        m = prog.match(i)
        if not m:
            logger.error("control dimension \"%s\" cannot be handled by control mode \"%s\""%(i, control_mode))    
            raise Exception("control dimension \"%s\" cannot be handled by control mode \"%s\""%(i, control_mode))    
        list_of_postfix.append(m.group(1))
    return list_of_postfix


def send_traj_point_marker(marker_pub, pose, id, rgba_tuple):
    marker = Marker()
    marker.header.frame_id = "/base"
    marker.header.stamp = rospy.Time.now()
    marker.ns = "traj_point" 
    marker.id = id
    marker.type = Marker.SPHERE
    marker.action = Marker.ADD
    marker.pose = pose
    marker.scale.x = 0.01
    marker.scale.y = 0.01
    marker.scale.z = 0.01
    marker.color.r = rgba_tuple[0]
    marker.color.g = rgba_tuple[1]
    marker.color.b = rgba_tuple[2]
    marker.color.a = rgba_tuple[3]
    marker.lifetime = rospy.Duration()
    marker_pub.publish(marker)  

    
def get_moveit_plan(command_matrix, control_dimensions, control_mode):

    marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size=100)
    
    list_of_postfix = get_eval_postfix(control_dimensions, control_mode)

    list_of_poses = []
    for row_no in range(command_matrix.shape[0]):
        pose = Pose() 
        for col_no in range(command_matrix.shape[1]):
            exec_str = 'pose'+list_of_postfix[col_no]+'=command_matrix[row_no, col_no]'
            exec(exec_str)
        logger.info("should pub")
        alpha = float(row_no)/command_matrix.shape[0]*0.5+0.5 
        rgba_tuple = (0, 0.5, 0.5, alpha)
        send_traj_point_marker(marker_pub=marker_pub, pose=pose, id=row_no, rgba_tuple=rgba_tuple)
        rospy.sleep(0.1)
        list_of_poses.append(pose)

    moveit_commander.roscpp_initialize(sys.argv)

    robot = moveit_commander.RobotCommander()
    group = moveit_commander.MoveGroupCommander("right_arm")

    display_trajectory_publisher = rospy.Publisher(
        '/move_group/display_planned_path',
        moveit_msgs.msg.DisplayTrajectory,
        queue_size=1000,
    )

    group.set_max_acceleration_scaling_factor(0.01)
    group.set_max_velocity_scaling_factor(0.01)
    (plan, fraction) = group.compute_cartesian_path(
                             list_of_poses,   # waypoints to follow
                             0.01,        # eef_step
                             0.0)         # jump_threshold

    display_trajectory = moveit_msgs.msg.DisplayTrajectory()
    display_trajectory.trajectory_start = robot.get_current_state()
    display_trajectory.trajectory.append(plan)
    rospy.loginfo("============ Visulaize plan")
    display_trajectory_publisher.publish(display_trajectory)

    raw_input()
