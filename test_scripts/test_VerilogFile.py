#!/usr/bin/env python3

from sys import stdout
import os

from Test_helper import add_srcPath
add_srcPath()
from VerilogFile import VerilogFile
from VerilogModule import VerilogModule
from VerilogPort import VerilogPort
from VerilogParameter import VerilogParameter
from VerilogCodeGen_Helper import *

if __name__ == "__main__":

    #### create a file with constructor calls ####
#     l_ports = [ 
#             VerilogPort(identifier="port1", portType="input", portWidthDeclaration=8),
#             VerilogPort(identifier="clk_i", portType="input"),
#             VerilogPort(identifier="port2", portType="output", portWidthDeclaration="MSG_BITS"),
#             VerilogPort(identifier="port3", portType="inout", portWidthDeclaration="[3:0]")
#             ]
#     l_parameters = [
#             VerilogParameter(identifier="param1"),
#             VerilogParameter(identifier="param2", defaultValue="DEF2")
#             ]
#     file_init = VerilogFile( 
#             verilogModule=VerilogModule( 
#                 moduleName="mod_init", 
#                 ports = l_ports, 
#                 parameters = l_parameters,
#                 outputReg = True), 
#             s_timescale="1ns/1ps",
#             s_author="Marwin Kirchhofs",
#             includeGuards=False,
#             indentObj=IndentObj(tabwidth=4, desiredIndentation=24),
#             language=HDL_Enum.SYSTEMVERILOG )
# 
#     print(file_init)
# 
#     # write module
#     file_init.write_moduleFile()
#     os.system("cat mod_init.sv")
# 
#     # write testbench
#     file_init.write_testbenchFile()
#     os.system("cat tb_mod_init.sv")


    print("\n----------------------\n")


    #### create a module by scanning a file ####
    s_testFile = "artyWrapper_uartController.sv"
    file_scan = VerilogFile.scan( s_testFile )
    print(file_scan) if file_scan else print("no module found!")

    stdout.write("\n\n")
    indentObj = IndentObj(tabwidth=4, desiredIndentation=24)
#     language = HDL_Enum.VERILOG
#     language = HDL_Enum.SYSTEMVERILOG
#     file_scan.write_declaration(stdout, indentObj, language)
#     stdout.write("\n\n")
#     file_scan.write_instantiation(stdout, indentObj)
    file_scan.indentObj = indentObj
    file_scan.write_testbenchFile()
    os.system("cat tb_artyWrapper_uartController.sv")




