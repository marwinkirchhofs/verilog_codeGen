#!/usr/bin/env python3


# verilog_codeGen
# Copyright © 2020 Marwin Kirchhofs <marwin.kirchhofs@rwth-aachen.de>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# code generator for Verilog/SystemVerilog
# 
#   ######################
#   #### capabilities ####
#   ######################
#   
#   * module file generation based on command line arguments
#       * optional additional generation of a suitable testbench file
#   * testbench generation for an existing Verilog/SystemVerilog file
#   * prints a module instantiation scanned from an existing module file (to be used while coding, e.g. as a terminal command from within vim)
#   
#   It is possible to set up a json configuration file named 'config.json' either in $HOME/.config/verilog_codeGen or in the top level of this repo (-> this file's directory). 
#   The configuration file may contain:
#       - searchPaths: list of paths where the specified module is searched in module instantiation (besides the working directory which is always used for the search)
#       - author: author to be used in each file generating mode
#       - tabwidth: set to your desired tabwidth, used in each writing operation
#   Every option (except from searchPaths) is overwritten if a command line parameter is given for this option
#
#
#   ###############
#   #### usage ####
#   ###############
#
#   * module file generation (with additional testbench)
#   verilog_codeGen [-i <input ports> -o <output ports> --output-reg -p <parameters> --timescale <timescale> --sv/systemverilog/SystemVerilog --include-guards --add-testbench/add-tb -a/--author <author> --tabwidth <tabwidth>] <module/file name> 
# 
#   * testbench generation
#       verilog_codeGen --testbench/tb <module/file name>
#
#   * module instantiation
#       verilog_codeGen --module-instantiation/mod-inst/modInst <module/file name>
#   
#   the different options may overlap, but in most cases invoking multiple different operations (besides the --add-testbench option) does not make much sense does not make much sense to me
#
#   #######################
#   #### configuration ####
#   #######################
#
#   * write a template configuration to just fill in your preferences
#       verilog_codeGen --config-template [target directory]
#           (target directory is optional, if not used, empty config is written to $HOME/.config/verilog_codeGen or to this repo's top level directory
#
#   #################
#   #### example ####
#   #################
#
#   * module file generation
#       uart receiver in verilog:
#       verilog_codeGen -i clk,rst_n,uart_i -o symbol_o#MSG_BITS,newSymbol_o --output-reg -p CLK_FREQ,BAUD_RATE,MSG_BITS --include-guards --author="John Doe" uartRx
#
#       respective wrapper in systemverilog:
#       verilog_codeGen -i clk,rst_n,uart_rxd_out -o symbol_o#8,newSymbol_o --timescale 1ns/1ps -a "N. Otjohndoe" --tabwidth=8 --sv wrapper_uartRx
#
#       resulting files: 
#       uartRx.v, uartRx.sv
#
#   * testbench generation
#       verilog_codeGen --testbench wrapper_uartRx.sv
#
#   * module instantiation
#       verilog_codeGen --modInst fifo_buffer 
#           searches for fifo_buffer.v/.sv in the current working directory and in search paths recursively
#           output is just printed to stdout, needs to be redirected in your preferred text editor (e.g. in vim: ':read !verilog_codeGen --modInst fifo_buffer')
#
#       
#

# add src path to python's module search path 
def add_srcPath():
    s_thisPath = os.path.realpath(__file__)
    l_srcPath = s_thisPath.split("/")[:-1] + ["src"]
    sys.path.append( "/".join(l_srcPath) )
    

import sys, os, re
from optparse import OptionParser
from time import localtime, strftime
from pathlib import Path
add_srcPath()
from VerilogModule import VerilogModule
from VerilogFile import VerilogFile
from VerilogPort import VerilogPort
from VerilogParameter import VerilogParameter
from Verilog_codeGen_config import Verilog_codeGen_config
from VerilogCodeGen_Helper import *


######################
#### main program ####
######################

if __name__ == '__main__':

    ####################################
    #### parse command line options ####
    ####################################

    parser = OptionParser()
    parser.add_option("-i",
            dest="inputs",
            help="input ports (comma-separated list) - port width syntax: <port_name>#<port_width> (port_width can be int or string, e.g. a parameter identifier) - specifying port_width is optional - example: \"-i data_i#MSG_BITS,btn_i#2,clk\"",
            metavar="input_ports")
    parser.add_option("-o",
            dest="outputs",
            help="output ports (comma-separated list) - port_width exactly the same as input ports",
            metavar="output_ports")
    parser.add_option("--output-reg",
            action="store_true",
            dest="output_reg",
            help="create output register variables")
    parser.add_option("-p",
            dest="parameters",
            help="parameter list (comma-separated")
    parser.add_option("--timescale",
            dest="timescale",
            help="timescale definition (e.g. \"1ns/1ps\")",
            metavar="timescale")
    parser.add_option("--sv","--systemverilog","--SystemVerilog",
            action="store_true",
            dest="systemverilog",
            help="if set, SystemVerilog is used instead of verilog")
    parser.add_option("--add-testbench","--add-tb",
            action="store_true",
            dest="b_addTestbench",
            help="invokes generation of a suitable testbench for specified module")
    parser.add_option("--include-guards",
            action="store_true",
            dest="b_include_guards",
            help="inserts include guards")
    parser.add_option("--testbench","--tb",
            action="store_true",
            dest="b_createTestbench",
            help="scans the specified input file and generates a suitable testbench")
    parser.add_option("--module-instantiation","--mod-inst","--modInst",
            action="store_true",
            dest="b_moduleInstantiation",
            help="searches the specified module and prints an instantiation")
    parser.add_option("--config-template",
            action="store_true",
            dest="b_configTemplate",
            help="writes an empty config to the directory passed as argument, to $HOME/.config/verilog_codeGen if $HOME/.config exists or to the top level of this project otherwise")
    parser.add_option("-a","--author",
            dest="author",
            help="specify author (pass as string)",
            metavar="author")
    parser.add_option("--tabwidth",
            dest="tabwidth",
            help="specify tabwidth for proper indentation, defaults to 4",
            metavar="tabwidth")


    #### parse options ####
    # (everything that may also be set in configuration file is evaluated after loading config file)

    # call parser
    (options, args) = parser.parse_args()

    # check for module name
    if len(args) != 1 :
        print( "Please specify a module/file name!" )
        exit(1)
    else:
        re_validFileEnding = r"(\.v|\.sv)\s*$"
       
        # determine language
        if options.systemverilog or re.search(r"\.sv", args[0]) or Path(args[0] + ".sv").is_file():
            language = HDL_Enum.SYSTEMVERILOG
        else:
            language = HDL_Enum.VERILOG

        if re.search(re_validFileEnding, args[0]):
            s_fileName = args[0]
            s_moduleName = re.sub(re_validFileEnding, "", args[0])
        else:
            s_fileName = args[0] + "." + language.get_fileEnding()
            s_moduleName = args[0] 

    # determine timescale string
    s_timescale = options.timescale if options.timescale else ""


    ##########################
    #### load config file ####
    ##########################

    config = Verilog_codeGen_config.load()
    l_searchPaths = config.searchPaths if config.searchPaths else []
    if not options.b_moduleInstantiation: print("Configuration loaded from " + config.get_configFile() )


    # determine tabwidth
    if options.tabwidth:
        tabwidth = int(options.tabwidth)
    elif config.tabwidth:
        tabwidth = config.tabwidth
    else: 
        tabwidth = 4
    indentObj = IndentObj( tabwidth, desiredIndentation=24 )
    
    # determine string for author name
    if options.author:
        s_author = options.author
    elif config.author:
        s_author = config.author
    else: 
        s_author = ""


    ###########################
    #### write config file ####
    ###########################

    if options.b_configTemplate:
        Verilog_codeGen_config.write_template(args[0] if args[0] else None)

    ###########################
    #### module generation ####
    ###########################

    if options.inputs or options.outputs or options.parameters:
        # setup port/parameter lists
        ports = []
        for portDescription in options.inputs.split(',') if options.inputs else []:
            ports.append( VerilogPort.fromPortDescription( portType="input", s_portDescription=portDescription ) )
        for portDescription in options.outputs.split(',') if options.outputs else []:
            ports.append( VerilogPort.fromPortDescription( portType="output", s_portDescription=portDescription ) )
        parameters = []
        for parameterDescription in options.parameters.split(',') if options.parameters else []:
            parameters.append( VerilogParameter.fromParameterDescription( parameterDescription) )

        verilogModule = VerilogModule( moduleName=s_moduleName, ports=ports, parameters=parameters, outputReg=options.output_reg)
        verilogFile = VerilogFile( verilogModule, 
                            s_timescale=s_timescale,
                            s_author=s_author,
                            includeGuards=options.b_include_guards,
                            indentObj=indentObj,
                            language=language )

        print("generating module file...")
        verilogFile.write_moduleFile()

        #### additional testbench generation ####
        if options.b_addTestbench:
            print("adding a testbench...")
            verilogFile.write_testbenchFile()


    ##############################
    #### testbench generation ####
    ##############################
    if options.b_createTestbench:
        verilogFile = VerilogFile.scan( s_fileName )
        verilogFile.indentObj = indentObj
        verilogFile.s_author = s_author
        verilogFile.s_timescale = s_timescale
        print("writing testbench file...")
        verilogFile.write_testbenchFile()

    
    ##############################
    #### module instantiation ####
    ##############################
    if options.b_moduleInstantiation:
        verilogModule = VerilogModule.generate_instantiationFromSearch( s_moduleName, config, indentObj=indentObj )
    

    if not options.b_moduleInstantiation:
        print("code generation done")
