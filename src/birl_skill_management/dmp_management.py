import os
from birl_baxter_dmp.dmp_train import train
from birl_baxter_dmp.dmp_generalize import dmp_imitate
import re
import logging
import pandas as pd
from birl_runtime_parameter_filler.interface import fill_in_runtime_param
import sys
from birl_skill_management.util import get_moveit_plan, get_eval_postfix, get_list_of_interested_column_name
import ipdb
import numpy as np

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


    list_of_new_skill_data = []
    for label, list_of_traj_mat in traj_group_by_label.iteritems():
        if label == '0':
            continue

        from util import plot_cmd_matrix
        for mat in list_of_traj_mat:
            plot_cmd_matrix(mat, list_of_interested_column_name, control_mode)

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
            "control_mode": control_mode,
            "control_dimensions": list_of_interested_column_name 
        }

        list_of_new_skill_data.append(skill_data)

    return list_of_new_skill_data

def cook_array_from_object_using_postfixs(list_of_postfix, obj):
    ret = []
    for postfix in list_of_postfix:
        eval_str = "obj"+postfix
        try:
            val = eval(eval_str)
        except AttributeError as e:
            logger.error("obj \"%s\" cannot be accessed by postfix\"%s\""%(obj, postfix))    
            continue
        ret.append(val)

    return ret

def execute_skill(skill_data):
    fill_in_runtime_param(skill_data)

    control_mode = skill_data["control_mode"]
    control_dimensions = skill_data["control_dimensions"]

    list_of_postfix = get_eval_postfix(control_dimensions, control_mode)

    raw_start = skill_data["skill_param"]["start"]
    raw_end = skill_data["skill_param"]["end"]

    start = cook_array_from_object_using_postfixs(list_of_postfix, raw_start)
    end = cook_array_from_object_using_postfixs(list_of_postfix, raw_end)

    logger.info("start: %s"%(start,))
    logger.info("end: %s"%(end,))
    command_matrix = dmp_imitate(starting_pose=start, ending_pose=end, weight_mat=skill_data["skill_param"]["basis_weight"])

    logger.info("command_matrix: %s"%(command_matrix,))
    return command_matrix



