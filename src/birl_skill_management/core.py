import os
import logging
import pickle
import sys

logger = logging.getLogger("birl_motion_library."+__name__)
logger.setLevel(logging.INFO)

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
SKILL_DATA_DIR =  os.path.join(PACKAGE_ROOT, "skill_data_dir")
PICKLE_DATA_DIR = os.path.join(SKILL_DATA_DIR, "pickle_data_dir")

class SkillNotFound(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class PickleSkillManager(object):
    def __init__(self):
        if not os.path.isdir(PICKLE_DATA_DIR):
            os.makedirs(PICKLE_DATA_DIR)

    def store(self, data_id, data):
        pkl_path = os.path.join(PICKLE_DATA_DIR, str(data_id)+".pkl")
        logger.info("gonna store data with id \"%s\" into a pickle file \"%s\".", data_id, pkl_path)  

        output_file = open(pkl_path, 'wb')
        pickle.dump(data, output_file) 

    def extract(self, data_id):
        pkl_path = os.path.join(PICKLE_DATA_DIR, str(data_id)+".pkl")
        if not os.path.isfile(pkl_path):
            logger.error("data with id \"%s\" not found since pickle file \"%s\" doesn't exist.", data_id, pkl_path)  
            raise SkillNotFound()
        logger.info("gonna extract data with id \"%s\" from pickle file \"%s\".", data_id, pkl_path)  
        input_file = open(pkl_path, 'rb')
        data = pickle.load(input_file)
        return data
