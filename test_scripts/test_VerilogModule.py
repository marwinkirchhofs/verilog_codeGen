#!/usr/bin/env python3

from sys import stdout

from Test_helper import add_srcPath
add_srcPath()
from VerilogModule import VerilogModule
from VerilogPort import VerilogPort
from VerilogParameter import VerilogParameter
from Verilog_codeGen_config import Verilog_codeGen_config
from VerilogCodeGen_Helper import *

if __name__ == "__main__":

#     #### create a module with constructor calls ####
#     l_ports = [ 
#             VerilogPort(identifier="port1", portType="input", portWidthDeclaration=8),
#             VerilogPort(identifier="port2", portType="output", portWidthDeclaration="MSG_BITS"),
#             VerilogPort(identifier="port3", portType="inout", portWidthDeclaration="[3:0]")
#             ]
#     l_parameters = [
#             VerilogParameter(identifier="param1"),
#             VerilogParameter(identifier="param2", defaultValue="DEF2")
#             ]
#     mod_init = VerilogModule( moduleName="mod_init", ports = l_ports, parameters = l_parameters)
#     print(mod_init)
# 
# 
#     print("\n----------------------\n")
# 
# 
#     #### create a module by scanning a file ####
#     s_testModule = "artyWrapper_uartController.sv"
#     mod_scan = VerilogModule.scan( s_testModule )
#     mod_scan.outputReg = True
#     print(mod_scan) if mod_scan else print("no module found!")
# 
#     stdout.write("\n\n")
#     indentObj = IndentObj(tabwidth=4, desiredIndentation=24)
# #     language = HDL_Enum.VERILOG
#     language = HDL_Enum.SYSTEMVERILOG
#     mod_scan.write_declaration(stdout, indentObj, language)
#     stdout.write("\n\n")
#     mod_scan.write_instantiation(stdout, indentObj)


    #### generate module instantiation from search ####
    # load config
    config = Verilog_codeGen_config.load()

    moduleName = "uartTransceiver"
    VerilogModule.generate_instantiationFromSearch( moduleName, config )

