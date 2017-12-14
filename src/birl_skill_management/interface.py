from core import PickleSkillManager, SkillNotFound
import logging

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
