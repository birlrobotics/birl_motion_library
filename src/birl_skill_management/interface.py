from birl_skill_management.core import PickleSkillManager, SkillNotFound
from birl_skill_management.core import store_skill, extract_skill
from birl_skill_management.util import get_moveit_plan
import logging
logger = logging.getLogger("birl_motion_library."+__name__)
logger.setLevel(logging.INFO)


def build_skill(dataset_path, control_mode, skill_id_prefix, skill_model='dmp'):
    if skill_model == 'dmp':
        import birl_skill_management.dmp_management
        list_of_new_skill_data = birl_skill_management.dmp_management.build_skill(dataset_path, control_mode, skill_id_prefix)
    else:
        logger.error("skill model \"%s\" not supported for build now"%(skill_model,))
        raise Exception("skill model \"%s\" not supported for build now"%(skill_model,))

    for skill_data in list_of_new_skill_data:
        store_skill(skill_data['id'], skill_data) 

    list_of_skill_id = [i['id'] for i in list_of_new_skill_data]
    return list_of_skill_id
        

def execute_skill(skill_id):
    skill_data = extract_skill(skill_id) 
    if skill_data is None:
        logger.error("skill not found")    
        raise Exception("skill not found")
    
    model_type = skill_data["model_type"]
    if model_type == 'dmp':
        import birl_skill_management.dmp_management
        command_matrix = birl_skill_management.dmp_management.execute_skill(skill_data)
    else:
        logger.error("skill model \"%s\" not supported for execution now"%(skill_model,))
        raise Exception("skill model \"%s\" not supported for execution now"%(skill_model,))

    control_mode = skill_data["control_mode"]
    control_dimensions = skill_data["control_dimensions"]
    if control_mode == 'pose':
        get_moveit_plan(command_matrix, control_dimensions, control_mode)
    else:
        raise Exception("control_mode \"%s\" is not supported now."%(control_mode,))






