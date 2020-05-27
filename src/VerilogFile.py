
from time import localtime, strftime
import re

from VerilogModule import VerilogModule
from VerilogCodeGen_Helper import *


class VerilogFile():

    """represents a Verilog file"""

    def __init__(self, verilogModule: VerilogModule, s_timescale="", s_author="", s_creationDate="", includeGuards: bool=False, indentObj: IndentObj=IndentObj(tabwidth=4, desiredIndentation=24), language: HDL_Enum=HDL_Enum.VERILOG ):
         
        self.verilogModule  = verilogModule
        self.s_timescale    = s_timescale
        self.s_author       = s_author
        self.includeGuards  = includeGuards
        self.indentObj      = indentObj
        self.language       = language
        self.s_creationDate = s_creationDate if s_creationDate else strftime("%Y-%m-%d", localtime())


    def __str__(self):
        l_print = [] 
        l_print.extend( ["language: ", str(self.language), "\n"] )
        l_print.extend( ["timescale: ", self.s_timescale, "\n"] )
        l_print.extend( ["author: ", self.s_author, "\n"] )
        l_print.extend( ["include guards: ", str(self.includeGuards), "\n"] )
        # append module printing
        l_print.extend( [str(self.verilogModule), "\n"] )

        return "".join( l_print )


    @classmethod
    def scan(cls, s_fileIn):
        """scan s_fileIn for a Verilog module declaration and file properties (timescale, language).
        As I assume that scanning a file will be used to generate a testbench or a module instantiation, the method does not scan for the properties s_author and includeGuards (same with VerilogModule.outputReg). They are not practical to match and not needed in those applications.

        :s_fileIn: string representing Verilog/Systemverilog source file to be scanned (gets opened)
        :returns: VerilogFile object if successful, otherwise None
        """
        # determine language from file ending (or exit if no known ending)
        mo_fileEnding = re.search(r"\.(v|sv)$", s_fileIn)
        if mo_fileEnding:
            s_fileEnding = mo_fileEnding.group(1) 
#             if s_fileEnding == "v":
            if s_fileEnding == HDL_Enum.VERILOG.get_fileEnding():
                language = HDL_Enum.VERILOG
            else:
                language = HDL_Enum.SYSTEMVERILOG
        else:
            print("no valid input file ending!")
            return None

        # regular expression to match timescale definition
        __re_timescaleDefintion = r"\s*`timescale\s*(\w+\s*/\s*\w+)"

        with open(s_fileIn, "r") as file_in: 
            # scan for module declaration 
            verilogModule = VerilogModule.scan( file_in )

            # if module declaration found, rescan file for timescale definition, else return None
            if verilogModule:
                # reset read pointer
                file_in.seek(0)

                currentLine = file_in.readline()
                while currentLine:

                    matchObj = re.match( __re_timescaleDefintion , currentLine)
                    if  matchObj:
                        # remove whitespaces from identified timescale string
                        s_timescale = (matchObj.group(1)).replace(" ","")
                        return cls( verilogModule=verilogModule, s_timescale=s_timescale, language=language)
                    else:
                        currentLine = file_in.readline()

                # return VerilogFile object without timescale definition
                return cls( verilogModule=verilogModule, language=language)

            else:
                return None


    def write_moduleFile(self, s_fileOut=""):
        """writes a complete code body to the specified output file

        :s_fileOut: string identifying output file; if empty, s_fileOut will be set to <verilogModule.moduleName>.v/sv depending on self.language
        """
        # determine s_fileOut if not passed
        if not s_fileOut:
            s_fileOut = self.verilogModule.moduleName + "." + self.language.get_fileEnding()

        # check for file existance
        try:
            with open(s_fileOut, "r") as file_out:
                # file exists -> query for overwriting
                overwrite = input("File " + s_fileOut + " exists! Are you sure you want to overwrite it? [y/n]")

                if overwrite == 'y':
                    print("File " + s_fileOut + " will be overwritten...")
                else :
                    print("File " + s_fileOut + " will not be overwritten. Exiting...")
                    return None
        except FileNotFoundError: 
            pass

        ##############################
        #### write to output file ####
        ##############################
        with open(s_fileOut, "w") as file_out:
                        
            #### timescale ####
            self.write_timescale(file_out)
            writeBlankLines(file_out, 1)

            #### include guards ####
            if self.includeGuards:
                self.verilogModule.write_includeGuards(file_out, "top")
                writeBlankLines(file_out, 1)

            #### file description commentary ####
            file_out.write("""/*
* company:
* author/engineer:\t""" + self.s_author + """
* creation date:\t""" + self.s_creationDate + """
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
            # fetch port dictionary
            d_ports = self.verilogModule.ports

            # TODO: maybe use get_tabbedString function to align port/parameter commentaries...
            # write example line
            file_out.write("*\t\t[port name]\t\t- [port description]\n")
            # input ports
            file_out.write("* * inputs:\n" if d_ports["input"] else "")
            for port in d_ports["input"]:
                file_out.write("*\t\t" + port.get_identifier() + "\t\n")

            # output ports
            file_out.write("* * outputs:\n" if d_ports["output"] else "")
            for port in d_ports["output"]:
                file_out.write("*\t\t" + port.get_identifier() + "\t\n")

            # inout ports
            file_out.write("* * inout:\n" if d_ports["inout"] else "")
            for port in d_ports["inout"]:
                file_out.write("*\t\t" + port.get_identifier() + "\t\n")
            
            # fetch parameter list
            l_parameters = self.verilogModule.l_parameters 

            # parameters
            if l_parameters:
                writeBlankLines(file_out,2,leading_string="*")
                file_out.write("* * parameters:\n")
                for parameter in l_parameters:
                    file_out.write("*\t\t" + parameter.identifier + "\t\n")

            file_out.write("*/\n")

            writeBlankLines(file_out,2)

            #### module declaration ####
            self.verilogModule.write_declaration(file_out, indentObj=self.indentObj, language=self.language)

            # end if
            if self.includeGuards:
                writeBlankLines(file_out,1)
                self.verilogModule.write_includeGuards(file_out, "bottom")


    def write_testbenchFile(self, s_fileOut="", b_removeIOSuffix=True):
        """generates a testbench file for self.verilogModule

        :s_fileOut: string identifying output file; if empty, s_fileOut will be set to <verilogModule.moduleName>.v/sv depending on self.language
        """
        # determine s_fileOut if not passed
        if not s_fileOut:
            s_fileOut = "tb_" + self.verilogModule.moduleName + "." + self.language.get_fileEnding()

        # check for file existance
        try:
            with open(s_fileOut, "r") as file_out:
                # file exists -> query for overwriting
                overwrite = input("File " + s_fileOut + " exists! Are you sure you want to overwrite it? [y/n]")

                if overwrite == 'y':
                    print("File " + s_fileOut + " will be overwritten...")
                else:
                    print("File " + s_fileOut + " will not be overwritten. Exiting...")
                    return None
        except FileNotFoundError: 
            pass

        ##############################
        #### write to output file ####
        ##############################
        with open(s_fileOut, "w") as file_out:
                        
            #### timescale ####
            self.write_timescale(file_out)
            writeBlankLines(file_out, 1)

            #### file description commentary ####
            file_out.write("""/*
* testbench for """ + self.verilogModule.moduleName + """
* 
* company:
* author/engineer:\t""" + self.s_author + """
* creation date:\t""" + self.s_creationDate + """
* project name:
* tool versions:
*/
""")

            writeBlankLines(file_out, 1)

            #### tb module generation ####
            file_out.write("module tb_" + self.verilogModule.moduleName + ";\n")
            writeBlankLines(file_out, 1)

            ## variable declarations ##
            # fetch port dictionary
            d_ports = self.verilogModule.ports
            
            # input ports
            file_out.write("\t// dut inputs\n" if d_ports["input"] else "")
            for port in d_ports["input"]:
                file_out.write("\t")
                port.write_connectedVariable(file_out, self.indentObj, self.language, b_removeIOSuffix=b_removeIOSuffix)
                file_out.write(";\n")
            if d_ports["input"]: writeBlankLines(file_out, 1)
            # output ports
            file_out.write("\t// dut outputs\n" if d_ports["output"] else "")
            for port in d_ports["output"]:
                file_out.write("\t")
                port.write_connectedVariable(file_out, self.indentObj, self.language, b_removeIOSuffix=b_removeIOSuffix)
                file_out.write(";\n")
            if d_ports["output"]: writeBlankLines(file_out, 1)
            # inout ports
            file_out.write("\t// dut inouts\n" if d_ports["inout"] else "")
            for port in d_ports["inout"]:
                file_out.write("\t")
                port.write_connectedVariable(file_out, self.indentObj, self.language, b_removeIOSuffix=b_removeIOSuffix)
                file_out.write(";\n")
                    
            writeBlankLines(file_out, 2)

            ## clock initialization ##
            # TODO: maybe deactivate by a parameter
            # search for clock signal and set up clock 
            # (I know it may not always be switching at 5 time units, but better that writing nothing)
            re_clk = r"(clk|CLK|clock|Clock)"
            for port in d_ports["input"]:
                mo_clk = re.search(re_clk, port.get_identifier() )
                if mo_clk:
                    file_out.writelines(["\talways begin\n", "\t\t #5 "])
                    s_variableIdentifier = port.get_identifier() if not b_removeIOSuffix else removeIOSuffix(port.get_identifier()) 
                    file_out.write( "\t\t" + s_variableIdentifier + " <= ~" + s_variableIdentifier+ ";\n")
                    file_out.write("\tend\n")
                    writeBlankLines(file_out, 1)

            writeBlankLines(file_out, 1)

            ## empty initial block (with clock initialized to 1 if exists) ##
            file_out.write("\tinitial begin\n")

            # initialize clock if found
            for port in d_ports["input"]:
                mo_clk = re.search(re_clk, port.get_identifier() )
                if mo_clk:
                    s_variableIdentifier = port.get_identifier() if not b_removeIOSuffix else removeIOSuffix(port.get_identifier()) 
                    file_out.write("\t\t" + s_variableIdentifier + " <= 1;\n")

            writeBlankLines(file_out, 2)
            file_out.writelines(["\t\t$finish\n", "\tend\n"])

            writeBlankLines(file_out, 2)

            ## dut instantiation
            # TODO: will not be indented
            self.verilogModule.write_instantiation(file_out, self.indentObj)

            writeBlankLines(file_out, 1)

            ## end module ##
            file_out.write("endmodule")
        

    def write_timescale(self, file_out):
        """writes a timescale definition to fileOut_Descriptor if self.s_timescale is not empty

        :file_out: output file object
        """
        if file_out.closed:
            print("file_out must be open!")
            return None

        if self.s_timescale:
            file_out.write("`timescale " + self.s_timescale + "\n")

