import re
import logging

logging.basicConfig(level=logging.INFO)
prog = re.compile(r"GetFromSkillParamServer\[(.*)\]")

def recursive_filler(data_dict):
    global prog
    for key in data_dict:
        value = data_dict[key]
        if type(value) == dict:
            logging.info("delve into \"%s\""%(key,)) 
            recursive_filler(data_dict[key])
            continue
        elif type(value) == str:
            m = prog.match(value)
            if m:
                param_name = m.group(1)
                logging.info("gonna fill runtime value for key \"%s\" whose param name is \"%s\""%(key, param_name)) 
            else:
                logging.info("skip \"%s\""%(key,)) 
