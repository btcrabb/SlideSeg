# ******************************************************************************
# SPAWAR, Systems Center Pacific
# Created August 1, 2017
# Author: Brendan Crabb <brendancrabb8388@pointloma.edu>
#
# ******************************************************************************

# Import necessary packages
from chip_test import run
import os


class Parameters(object):
    """Loads parameter options from text file"""

    def __init__(self, parameter_file):
        self._parameters = parameter_file

    def load_parameters(self):
        params = {}
        file = open(self._parameters, "r")

        # Load parameters from Parameters.txt
        for line in file:
            option = line.partition(":")[0]
            value = line.partition(":")[2]
            value = value.partition("#")[0].strip()
            params[option] = value
        return params


def main():
    def str2bool(value):
        return value.lower() in ("true", "yes", "1")

    params = Parameters('Parameters.txt').load_parameters()
    print('running __main__ with parameters: {0}'.format(params))

    if str2bool(params["single_slide"]) is True:
        path, filename = os.path.split(params["slide_path"])
        xpath, xml_filename = os.path.split(params["xml_path"])
        params["slide_path"] = path
        params["xml_path"] = xpath

        print('loading {0}'.format(filename))
        run(params, filename)

    else:
        for filename in os.listdir(params["slide_path"]):
            run(params, filename)

if __name__ == "__main__":
    main()