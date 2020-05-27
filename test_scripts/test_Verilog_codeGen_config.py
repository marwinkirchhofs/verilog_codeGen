#!/usr/bin/env python3

import os, sys

from Test_helper import add_srcPath
add_srcPath()
from VerilogFile import VerilogFile
from VerilogModule import VerilogModule
from VerilogPort import VerilogPort
from VerilogParameter import VerilogParameter
from Verilog_codeGen_config import Verilog_codeGen_config
from VerilogCodeGen_Helper import *

if __name__ == "__main__":

    s_configFile = os.getenv("HOME") + "/Programming/Python/Verilog_genModule/testconfig.json"
#     with open(s_configFile, "w") as file_out:
#         config = Verilog_codeGen_config(configFile = file_out, searchPaths=["path1", "path2"], author="Marwin", tabwidth=4)
#         config.write_config()

    config_loaded = Verilog_codeGen_config.from_json()
    print(config_loaded)
