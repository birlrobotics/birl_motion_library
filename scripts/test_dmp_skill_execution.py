from birl_skill_management.interface import extract_skill
from birl_runtime_parameter_filler.interface import fill_in_runtime_param
from optparse import OptionParser
import logging
import sys

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-s", action="store", type="string", dest="skill_id", help="Skill id")

    (options, args) = parser.parse_args()

    if options.skill_id is None:
        parser.error("skill id not specified.") 

    skill_id = options.skill_id
    
    skill_data = extract_skill(skill_id) 
    if skill_data is None:
        logging.error("skill not found")    
        sys.exit(1)    

    fill_in_runtime_param(skill_data)

    print skill_data
