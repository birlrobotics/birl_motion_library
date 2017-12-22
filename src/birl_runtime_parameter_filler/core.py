import re
import logging
from util import get_topic_message_once
from baxter_core_msgs.msg import EndpointState
from geometry_msgs.msg import (
    Pose,
    Quaternion,
)
import sys

logger = logging.getLogger("birl_motion_library."+__name__)
logger.setLevel(logging.INFO)

def param_fetcher(param_name):
    m = re.match(r"robot.*((left|right)).*gripper.*pose", param_name)
    if m:
        direction = m.group(1)
        logger.info("fetching robot %s gripper pose"%(direction,)) 
        topic_name = "/robot/limb/%s/endpoint_state"%(direction,)
        topic_type = EndpointState
        endpoint_state_msg = get_topic_message_once(topic_name, topic_type)
        return endpoint_state_msg.pose

    m = re.match(r"object_picking_pose", param_name)
    if m:
        logger.info("fetching object_picking_pose") 

        pick_object_pose = Pose()
        pick_object_pose.position.x = 0.74928596188
        pick_object_pose.position.y = -0.148838816821
        pick_object_pose.position.z = -0.0279642309342
        pick_object_pose.orientation = Quaternion(
            x= -0.00840934474046,
            y= 0.999184372723,
            z= 0.0164415452673,
            w= 0.0359098580458,
        )

        return pick_object_pose


    return None

def recursive_filler(data_dict):
    prog = re.compile(r"GetFromSkillParamServer\[(.*)\]")
    for key in data_dict:
        value = data_dict[key]
        if type(value) == dict:
            logger.info("delve into \"%s\""%(key,)) 
            recursive_filler(data_dict[key])
            continue
        elif type(value) == str:
            m = prog.match(value)
            if m:
                param_name = m.group(1)
                logger.info("gonna fill runtime value for key \"%s\" whose param name is \"%s\""%(key, param_name)) 
                param = param_fetcher(param_name)
                data_dict[key] = param 
            else:
                logger.info("skip \"%s\""%(key,)) 
