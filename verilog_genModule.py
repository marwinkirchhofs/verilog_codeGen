#!/usr/bin/env python3

# generates the body for a verilog/systemverilog module
# 
# The module's name is specified as last command line argument. The file name gets derived from it by appending .v/.sv.
#
#
#   ###############
#   #### usage ####
#   ###############
#
#   verilog_genModule [-i <input ports> -o <output ports> --output-reg -p <parameters> --timescale <timescale> --sv/systemverilog/SystemVerilog --include-guards -a/--author <author> --tabwidth <tabwidth>] <name of module> 
# 
#
#   #################
#   #### example ####
#   #################
#
#   uart receiver in verilog:
#   verilog_genModule -i clk,rst_n,uart_i -o symbol_o#MSG_BITS,newSymbol_o --output-reg -p CLK_FREQ,BAUD_RATE,MSG_BITS --include-guards --author="John Doe" uartRx
#
#   respective wrapper in systemverilog:
#   verilog_genModule -i clk,rst_n,uart_rxd_out -o symbol_o#8,newSymbol_o --timescale 1ns/1ps -a "N. Otjohndoe" --tabwidth=8 --sv wrapper_uartRx
#
#   resulting files: 
#   uartRx.v, uartRx.sv
#   for resulting hdl see example files (TODO) or just try ;-)
#


from sys import exit
from optparse import OptionParser
from time import localtime, strftime


# small helper to write blank lines to an open file
def writeBlankLines(filename, number, leading_string=None):
    for i in range(number):
        if leading_string: filename.writelines(leading_string)
        filename.writelines("\n")

#
# extract port name from port_description
def get_port_name(port_description):
    return port_description.split('#')[0]


# extract port width from port_description
# returns string one of the following formats, depending on how port width was specified:
# "[7:0]"
# "[WIDTH-1:0]"
def get_s_port_width(port_description):
    if '#' in port_description:
        port_width = port_description.split('#')[1]
    else:
        port_width = None

    # determine suitable string representation for port_width
    if port_width:
        # differ between passed as int or as parameter
        try:
            s_port_width = str( int(port_width) - 1)
        except:
            s_port_width = port_width + "-1"

        return s_port_width
    else:
        return None


# returns a formatted string to print a port in verilog/systemverilog syntax
# port_description is the port specification as extracted by the OptionParser ("<port_name>#<port_width>). port_name and port_width are derived from it
# format:   "<port_type> [<port_width>-1:0]  <port_name>"
# format:   "<port_type>                    <port_name>"
# all three columns aligned if possible (referring to desired portName indentation)
def s_printPort(port_description, port_type, tabwidth=4):
    
    # extract port name and width 
    port_name = get_port_name(port_description)
    s_port_width = get_s_port_width(port_description)

    # evaluate maximum tab chars until port_name dependant on tabwidth
    desiredIndentation = 24
    portName_indentation = int( desiredIndentation / tabwidth )

    list_s_out = []     # list to take parts of output string
    list_s_out.append(port_type + "\t")
    
    # add s_port_width if given
    if s_port_width and s_port_width != "[0:0]":
        list_s_out.append("[" + s_port_width + ":0]\t")

    # compute remaining tab characters 
    remainingTabs = portName_indentation - ( int( len(port_type) / tabwidth) + 1)
    if s_port_width:
        remainingTabs -= ( int( (len(s_port_width) + 4) / tabwidth) + 1)

    # append remaining tabs (won't append anything if remainingTabs <= 0)
    for i in range(remainingTabs):
        list_s_out.append("\t")

    # append port name
    list_s_out.append(port_name)
    
    return "".join(list_s_out)





######################
#### main program ####
######################

if __name__ == '__main__':

    ####################################
    #### parse command line options ####
    ####################################

    parser = OptionParser()
    parser.add_option("-i", dest="inputs", help="input ports (comma-separated list) - port width syntax: <port_name>#<port_width> (port_width can be int or string, e.g. a parameter identifier) - specifying port_width is optional - example: \"-i data_i#MSG_BITS,btn_i#2,clk\"", metavar="input_ports")
    parser.add_option("-o", dest="outputs", help="output ports (comma-separated list) - port_width exactly the same as input ports", metavar="output_ports")
    parser.add_option("--output-reg", action="store_true", dest="output_reg", help="create output register variables")
    parser.add_option("-p", dest="parameters", help="parameter list (comma-separated")
    parser.add_option("--timescale", dest="timescale", help="timescale definition (e.g. \"1ns/1ps\")", metavar="timescale")
    parser.add_option("--sv", "--systemverilog", "--SystemVerilog", action="store_true", dest="systemverilog", help="if set, SystemVerilog is used instead of verilog")
    parser.add_option("--include-guards", action="store_true", dest="include_guards", help="inserts include guards")
    parser.add_option("-a", "--author", dest="author", help="specify author (pass as string)", metavar="author")
    parser.add_option("--tabwidth", dest="tabwidth", help="specify tabwidth for proper indentation, defaults to 4", metavar="tabwidth")


    #### parse options ####

    # call parser
    (options, args) = parser.parse_args()
    
    # check for module name
    if len(args) != 1 :
        print( "Please specify a module name!" )
        exit(1)
    else:
        moduleName = args[0]

    # setup port/parameter lists
    list_inputs = options.inputs.split(',') if options.inputs else []
    list_outputs = options.outputs.split(',') if options.outputs else []
    list_parameters = options.parameters.split(',') if options.parameters else []

    # determine tabwidth
    tabwidth = int(options.tabwidth) if options.tabwidth else 4

    # determine variable type for registers
    if options.systemverilog:
        s_regType = "logic"
    else:
        s_regType = "reg"

    # determine string for author name
    s_author = options.author if options.author else ""

    ###################
    #### open file ####
    ###################

    # determine file name
    if options.systemverilog :
        s_file_out = moduleName + ".sv"
    else : 
        s_file_out = moduleName + ".v"
    
    # check for file existance
    try:
        with open(s_file_out) as file_out:
            # file exists -> query for overwriting
            overwrite = input("File " + s_file_out + " exists! Are you sure you want to overwrite it? [y/n]")

            if overwrite == 'y':
                print("File " + s_file_out + " will be overwritten...")
                file_out.close()
            else :
                print("File " + s_file_out + " will not be overwritten. Exiting...")
                file_out.close()
                exit(1)
    except FileNotFoundError: 
        pass

    # open file
    file_out = open(s_file_out, "w")


    ##############################
    #### write to output file ####
    ##############################

    #### timescale ####
    if options.timescale : 
        file_out.writelines("`timescale " + options.timescale + "\n")

    writeBlankLines(file_out, 1) 

    #### include guards ####
    if options.include_guards : 
        file_out.writelines("`ifndef " + moduleName.upper() + "_H\n")
        file_out.writelines("`define " + moduleName.upper() + "_H\n")
        writeBlankLines(file_out, 1) 

    #### file description commentary ####
    file_out.writelines("""/*
* company:
* author/engineer:\t""" + s_author + """
* creation date:\t""" + strftime("%Y-%m-%d", localtime()) + """
* project name:
* target devices:
* tool versions:
*
*
* * description:
* [module description]
*
* * interface:
* [interfacing description]
*
*
""")
    # input ports
    file_out.writelines("* * inputs:\n")
    # write example line
    file_out.writelines("*\t\t[port name]\t\t- [port description]\n")
    for port in list_inputs:
        file_out.writelines("*\t\t" + get_port_name(port) + "\t\n")

    # output ports
    file_out.writelines("* * outputs:\n")
    for port in list_outputs:
        file_out.writelines("*\t\t" + get_port_name(port) + "\t\n")

    # parameters
    if options.parameters:
        writeBlankLines(file_out,2,leading_string="*")
        file_out.writelines("* * parameters:\n")
        for parameter in list_parameters:
            file_out.writelines("*\t" + parameter + "\t\n")

    file_out.writelines("*/\n")

    writeBlankLines(file_out,2)

    #### module declaration ####
    # parameters
    if list_parameters:
        file_out.writelines("module " + moduleName + " #(\n")
        for parameter in list_parameters:
            file_out.writelines("\tparameter\t\t" + parameter)
            if parameter != list_parameters[-1]:
                file_out.writelines(",")
            file_out.writelines("\n")

        file_out.writelines(")\n")
        file_out.writelines("(\n")
    else:
        file_out.writelines("module " + moduleName + " (\n")

    # inputs
    for port in list_inputs:
        file_out.writelines("\t" + s_printPort(port_description=port, port_type="input", tabwidth=tabwidth) )
        if port != list_inputs[-1] or list_outputs:
            file_out.writelines(",")
        file_out.writelines("\n")

    writeBlankLines(file_out,1)
    
    # outputs
    for port in list_outputs:
        file_out.writelines("\t" + s_printPort(port_description=port, port_type="output", tabwidth=tabwidth) )
        if port != list_outputs[-1]:
            file_out.writelines(",")
        file_out.writelines("\n")

    file_out.writelines(");\n")

    writeBlankLines(file_out,1)

    #### output registers ####
    if options.output_reg:

        file_out.writelines("\t// output registers\n")
        for port in list_outputs:
#            file_out.writelines("\t" + s_regType + "\t\t\t" + port + ";\n")
            file_out.writelines("\t" + s_printPort(port_description=port, port_type=s_regType, tabwidth=tabwidth) + ";\n" )

    
    #### module body ####
    writeBlankLines(file_out,5)

    # end module
    file_out.writelines("endmodule\n")

    # end if
    if options.include_guards:
        writeBlankLines(file_out,1)
        file_out.writelines("`endif\n")

