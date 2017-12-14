import re
import logging
from util import get_topic_message_once
from baxter_core_msgs.msg import EndpointState
from geometry_msgs.msg import (
    Pose,
    Quaternion,
)

logging.basicConfig(level=logging.INFO)

def param_fetcher(param_name):
    m = re.match(r"robot.*((left|right)).*gripper.*pose", param_name)
    if m:
        direction = m.group(1)
        logging.info("fetching robot %s gripper pose"%(direction,)) 
        topic_name = "/robot/limb/%s/endpoint_state"%(direction,)
        topic_type = EndpointState
        endpoint_state_msg = get_topic_message_once(topic_name, topic_type)
        return endpoint_state_msg.pose

    m = re.match(r"object_picking_pose", param_name)
    if m:
        logging.info("fetching object_picking_pose") 

        pick_object_pose = Pose()
        pick_object_pose.position.x = 0.76301988477
        pick_object_pose.position.y = -0.290728116404
        pick_object_pose.position.z = -0.0195624201388
        pick_object_pose.orientation = Quaternion(
            x= -0.0259799924463,
            y= 0.999465665097,
            z= 0.00445775211005,
            w= 0.0193275122869,
        )

        return pick_object_pose


    return None

def recursive_filler(data_dict):
    prog = re.compile(r"GetFromSkillParamServer\[(.*)\]")
    for key in data_dict:
        value = data_dict[key]
        if type(value) == dict:
            logging.info("delve into \"%s\""%(key,)) 
            recursive_filler(data_dict[key])
            continue
        elif type(value) == str:
            m = prog.match(value)
            if m:
                param_name = m.group(1)
                logging.info("gonna fill runtime value for key \"%s\" whose param name is \"%s\""%(key, param_name)) 
                param = param_fetcher(param_name)
                data_dict[key] = param 
            else:
                logging.info("skip \"%s\""%(key,)) 
