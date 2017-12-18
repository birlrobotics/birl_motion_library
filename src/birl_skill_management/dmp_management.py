import os
from birl_baxter_dmp.dmp_train import train
from birl_baxter_dmp.dmp_generalize import dmp_imitate
import re
import logging
import pandas as pd
from birl_skill_management.core import store_skill, extract_skill
from skill_building_util import get_list_of_interested_column_name
from birl_runtime_parameter_filler.interface import fill_in_runtime_param
import sys

logger = logging.getLogger("birl_motion_library."+__name__)
logger.setLevel(logging.INFO)

def build_skill(dataset_path, control_mode, skill_id_prefix):
    traj_group_by_label = {}

    files = os.listdir(dataset_path)
    prog = re.compile(r"label_\((\d+)\).*\.csv")
    count = 0
    list_of_interested_column_name = None
    for f in files:
        m = prog.match(f)
        if not m:
            logger.warning('bad filename \"%s\" found in \"%s\"', f, dataset_path)
            continue
        else:
            label = m.group(1)
            if label not in traj_group_by_label:
                traj_group_by_label[label] = []
            logger.info("label=%s for file \"%s\"", label, f)  
            count += 1

        df = pd.read_csv(os.path.join(dataset_path, f), sep=',')  
        if count == 1:
            list_of_interested_column_name = get_list_of_interested_column_name(
                df.columns, control_mode
            ) 
            logger.info("list_of_interested_column_name: %s", list_of_interested_column_name)

        traj_group_by_label[label].append(df[list_of_interested_column_name].values)


    list_of_new_skill_id = []
    for label, list_of_traj_mat in traj_group_by_label.iteritems():
        basis_weight, basis_function_type = train(list_of_traj_mat)

        skill_param = {
            "start": "GetFromSkillParamServer[robot_current_right_gripper_pose]",
            "end": "GetFromSkillParamServer[object_picking_pose]",
            "basis_weight": basis_weight,
            "basis_function_type": basis_function_type,
        }

        skill_data = {
            "id": "%s_label_%s"%(skill_id_prefix, label),
            "model_type": "dmp",
            "skill_param": skill_param,
            "control_mode": "pose",
            "control_dimensions": list_of_interested_column_name 
        }

        store_skill(skill_data['id'], skill_data) 
        list_of_new_skill_id.append(skill_data['id'])

    return list_of_new_skill_id

def cook_array_from_object_using_postfixs(list_of_postfix, obj):
    ret = []
    for postfix in list_of_postfix:
        exec_str = "obj"+postfix
        try:
            val = eval(exec_str)
        except AttributeError as e:
            logger.error("obj \"%s\" cannot be accessed by postfix\"%s\""%(obj, postfix))    
            continue
        ret.append(val)

    return ret

def execute_skill(skill_data):
    fill_in_runtime_param(skill_data)

    control_mode = skill_data["control_mode"]
    control_dimensions = skill_data["control_dimensions"]
    prog = re.compile(ur".*%s(.*)"%(control_mode,))

    list_of_postfix = []
    for i in control_dimensions:
        m = prog.match(i)
        if not m:
            logger.error("control dimension \"%s\" cannot be handled by control mode \"%s\""%(i, control_mode))    
            raise Exception("control dimension \"%s\" cannot be handled by control mode \"%s\""%(i, control_mode))    
        list_of_postfix.append(m.group(1))

    raw_start = skill_data["skill_param"]["start"]
    raw_end = skill_data["skill_param"]["end"]

    start = cook_array_from_object_using_postfixs(list_of_postfix, raw_start)
    end = cook_array_from_object_using_postfixs(list_of_postfix, raw_end)

    logger.info("start: %s"%(start,))
    logger.info("end: %s"%(end,))

    gen_matrix = dmp_imitate(starting_pose=start, ending_pose=end, weight_mat=skill_data["skill_param"]["basis_weight"])

    logger.info("gen matrix: %s"%(gen_matrix,))



