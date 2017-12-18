#!/usr/bin/env python
import sys
import logging
from  birl_skill_management.interface import build_skill, execute_skill

logger = logging.getLogger("birl_motion_library")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch) 

if __name__ == "__main__":
    dataset_path = '/home/sklaw/Desktop/experiment/birl/data_for_or_from_HMM/baxter_pick_and_place_data/real_baxter_mini_pnp_v_2/extracted_anomalies_dir/20171204165831.345227/dataset_of_resampled_DTWed_lfd_dir/'
    control_mode = 'pose'
    list_of_new_skill_id = build_skill(dataset_path, control_mode, "anomaly_recovery_skill", "dmp") 
    logger.info("list_of_new_skill_id: %s"%(list_of_new_skill_id,))

    for skill_id in list_of_new_skill_id:
        logger.info("test exec of skill id: %s"%(skill_id,))
        execute_skill(skill_id)
