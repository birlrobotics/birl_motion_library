#!/usr/bin/env python
import logging
import birl_skill_management.dmp_management

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    options = build_skill_util.parse_arg()
    dataset_path = options.dataset_path
    control_mode = options.control_mode

    list_of_new_skill_id = birl_skill_management.dmp_management.build_skill(dataset_path, control_mode, "anomaly_recovery_skill") 
    print list_of_new_skill_id


