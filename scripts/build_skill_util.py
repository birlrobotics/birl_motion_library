from optparse import OptionParser
import re

def parse_arg():
    parser = OptionParser()

    parser.add_option("-d", action="store", type="string", dest="dataset_path",
        help="The path to a dataset folder which contains files with this format: \"label_(*)_*.csv\". Each csv is a human demonstration recorded during the recovery of the labelled anomaly. One recovery skill is trained for each anomaly label and later added into the skill library.")

    parser.add_option("-c", action="store", type="string", dest="control_mode", default='pose',
        help="The control mode of the skill. Possible values: pose.")

    (options, args) = parser.parse_args()

    if options.dataset_path is None:
        parser.error("dataset_path not specified.")

    prog = re.compile(r'^(pose)$')
    if not prog.match(options.control_mode):
        parser.error("invalid control_mode.")

    return options

