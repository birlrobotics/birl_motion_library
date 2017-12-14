import logging
import sys
import birl_skill_management.dmp_management

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    dataset_path = '/home/sklaw/Desktop/experiment/birl/data_for_or_from_HMM/baxter_pick_and_place_data/real_baxter_mini_pnp_v_2/extracted_anomalies_dir/20171204165831.345227/dataset_of_resampled_DTWed_lfd_dir/'
    control_mode = 'pose'
    list_of_new_skill_id = birl_skill_management.dmp_management.build_skill(dataset_path, control_mode, "anomaly_recovery_skill") 
    print list_of_new_skill_id
