#!/usr/bin/env python
from  birl_skill_management.interface import build_skill

if __name__ == "__main__":
    options = build_skill_util.parse_arg()
    dataset_path = options.dataset_path
    control_mode = options.control_mode

    list_of_new_skill_id = build_skill(dataset_path, control_mode, "anomaly_recovery_skill", "dmp") 
    print list_of_new_skill_id


