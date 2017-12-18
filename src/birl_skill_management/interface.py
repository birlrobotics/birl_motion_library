from core import PickleSkillManager, SkillNotFound
import logging
logger = logging.getLogger("birl_motion_library."+__name__)
logger.setLevel(logging.INFO)

def store_skill(data_id, data):
    psm = PickleSkillManager()
    psm.store(data_id, data)

def extract_skill(data_id):
    psm = PickleSkillManager()
    try:
        data = psm.extract(data_id)
    except SkillNotFound as e:
        return None
    else:
        return data

def build_skill(dataset_path, control_mode, skill_id_prefix, skill_model='dmp'):
    if skill_model == 'dmp':
        import birl_skill_management.dmp_management
        return birl_skill_management.dmp_management.build_skill(dataset_path, control_mode, skill_id_prefix)
    else:
        logger.error("skill model \"%s\" not supported for build now"%(skill_model,))
        raise Exception("skill model \"%s\" not supported for build now"%(skill_model,))
        

def execute_skill(skill_id):
    skill_data = extract_skill(skill_id) 
    if skill_data is None:
        logger.error("skill not found")    
        raise Exception("skill not found")
    
    model_type = skill_data["model_type"]
    if model_type == 'dmp':
        import birl_skill_management.dmp_management
        birl_skill_management.dmp_management.execute_skill(skill_data)
    else:
        logger.error("skill model \"%s\" not supported for execution now"%(skill_model,))
        raise Exception("skill model \"%s\" not supported for execution now"%(skill_model,))
