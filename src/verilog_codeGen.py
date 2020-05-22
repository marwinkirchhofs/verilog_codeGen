#!/usr/bin/env python3

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
#   ###############
#   #### usage ####
#   ###############
#
#   * module file generation (with additional testbench)
#   verilog_codeGen [-i <input ports> -o <output ports> --output-reg -p <parameters> --timescale <timescale> --sv/systemverilog/SystemVerilog --include-guards --add-testbench/add-tb -a/--author <author> --tabwidth <tabwidth>] <module/file name> 
# 
#   * testbench generation
#   verilog_codeGen --testbench/tb <module/file name>
#
#   * module instantiation
#   verilog_codeGen --module-instantiation/mod-inst/modInst <module/file name>
#   
#   the different options may overlap, but I don't see any sense in invoking multiple of the three options at a time
#
#   #######################
#   #### configuration ####
#   #######################
#
#   TODO
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


from sys import exit
from optparse import OptionParser
from time import localtime, strftime
import re
from VerilogModule import VerilogModule
from VerilogFile import VerilogFile
from VerilogPort import VerilogPort
from VerilogParameter import VerilogParameter
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
    parser.add_option("-a","--author",
            dest="author",
            help="specify author (pass as string)",
            metavar="author")
    parser.add_option("--tabwidth",
            dest="tabwidth",
            help="specify tabwidth for proper indentation, defaults to 4",
            metavar="tabwidth")


    #### parse options ####

    # call parser
    (options, args) = parser.parse_args()
    print(args)
    

    # check for module name
    if len(args) != 1 :
        print( "Please specify a module/file name!" )
        exit(1)
    else:
        re_validFileEnding = r"(\.v|\.sv)\s*$"
       
        # determine language
        if options.systemverilog or re.search(r"\.sv", args[0]):
            language = HDL_Enum.SYSTEMVERILOG
        else:
            language = HDL_Enum.VERILOG

        if re.search(re_validFileEnding, args[0]):
            s_fileName = args[0]
            s_moduleName = re.sub(re_validFileEnding, args[0])
        else:
            s_fileName = args[0] + "." + language.get_fileEnding()
            s_moduleName = args[0] 


    ###########################
    #### module generation ####
    ###########################

    if options.inputs or options.outputs or options.parameters:
        # setup port/parameter lists
        ports = []
        for portDescription in options.inputs.split(',') if options.inputs else []:
            ports.append( VerilogPort( portType="input", s_portDescription=portDescription ) )
        for portDescription in options.outputs.split(',') if options.outputs else []:
            ports.append( VerilogPort( portType="output", s_portDescription=portDescription ) )
        parameters = []
        for parameterDescription in options.parameters.split(',') if options.parameters else []:
            parameters.append( VerilogParameter( parameterDescription) )

        # determine tabwidth
        indentObj = IndentObj( tabwidth=int(options.tabwidth) if options.tabwidth else 4, desiredIndentation=24 )

        # determine string for author name
        s_author = options.author if options.author else ""

        verilogModule = VerilogModule( moduleName=s_moduleName, ports=ports, parameters=parameters, outputReg=options.output_reg)
        verilogFile = VerilogFile( verilogModule, 
                            s_timescale=options.timescale if options.timescale else "",
                            s_author=options.author if options.author else "",
                            includeGuards=options.b_include_guards,
                            indentObj=indentObj,
                            language=language )

        print(verilogFile)
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
        # TODO
        pass
    
    ##############################
    #### module instantiation ####
    ##############################
    if options.b_moduleInstantiation:
        # TODO
        pass

    print("code generation done")
