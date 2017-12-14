import re

def get_list_of_interested_column_name(list_of_column_name, control_mode):
    if control_mode == 'pose':
        prog = re.compile(ur".*(pose).*")
    else:
        raise Exception("control_mode \"%s\" is not supported now."%(control_mode,))

    ret = []
    for i in list_of_column_name:
        if prog.match(i):
            ret.append(i)
    return ret

