import os
from birl_baxter_dmp.dmp_train import train
from birl_baxter_dmp.dmp_generalize import dmp_imitate
import re
import logging
import pandas as pd
from birl_skill_management.interface import store_skill, extract_skill
from skill_building_util import get_list_of_interested_column_name
from birl_runtime_parameter_filler.interface import fill_in_runtime_param

logging.basicConfig(level=logging.INFO)

def build_skill(dataset_path, control_mode, skill_id_prefix):
    traj_group_by_label = {}

    files = os.listdir(dataset_path)
    prog = re.compile(r"label_\((\d+)\).*\.csv")
    count = 0
    list_of_interested_column_name = None
    for f in files:
        m = prog.match(f)
        if not m:
            logging.warning('bad filename \"%s\" found in \"%s\"', f, dataset_path)
            continue
        else:
            label = m.group(1)
            if label not in traj_group_by_label:
                traj_group_by_label[label] = []
            logging.info("label=%s for file \"%s\"", label, f)  
            count += 1

        df = pd.read_csv(os.path.join(dataset_path, f), sep=',')  
        if count == 1:
            list_of_interested_column_name = get_list_of_interested_column_name(
                df.columns, control_mode
            ) 
            logging.info("list_of_interested_column_name: %s", list_of_interested_column_name)

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

def execute_skill(skill_id):
    skill_data = extract_skill(skill_id) 
    if skill_data is None:
        logging.error("skill not found")    
        return False
    fill_in_runtime_param(skill_data)
    return True
