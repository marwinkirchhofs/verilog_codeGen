
#
# represent a Verilog Port
#

import re
from VerilogCodeGen_Helper import *

class VerilogPort:
    """represents a Verilog Port
    """

    # valid port types for comparison in instantiation/scanning
    __validPortTypes = ("input","output","inout")
    # (TODO:) maybe move those patterns as static parameters to the scan method, if they don't get used somewhere else
    # pattern to match a port declaration 
    # -> group(1): portType, group(2): variable type (if given), group(3): s_portWidthDeclaration (if given)
    __re_validPortDeclaration = r".*(input|output|inout)\s+(reg|wire|logic|)\s*(\[[\w-]+:[\w-]+\]|)"
    # pattern to look for identifiers in a port declaration (with declaration part deleted by re.sub -> string starting with port name(s) )
    __re_portIdentifier = r"[\w-]"


    def __init__(self, portType, identifier, portWidthDeclaration=None):
        """creates a VerilogPort, portWidthDeclaration defaults to None
        
        :portType: port type as string (one of "input", "output", "inout")
        :portWidthDeclaration: port width in bits as a string or int (e.g. 8, "MSG-BITS")
        :identifier: port name
        """
        # check for correct arguments
        if not portType in type(self).__validPortTypes:
            print("'" + portType + "' is not a valid port type! Valid port types are: input, output, inout!")
            return None
        if not identifier:
            print("Identifier must not be empty!")
            return None

        self.__portType   = portType
        self.__identifier = identifier
        
        # determine correct port width declaration string (can be passed as int, as full declaration or as string e.g. representing a parameter)
        if portWidthDeclaration:
            try:
                # check for int value
                self.__s_portWidthDeclaration = "[" + str(int(portWidthDeclaration) - 1) + ":0]"
            except:
                if re.match(r"\[", portWidthDeclaration):
                    # full declaration passed
                    self.__s_portWidthDeclaration = portWidthDeclaration
                else:
                    # parameter identifier passed
                    self.__s_portWidthDeclaration = "[" + portWidthDeclaration + "-1:0]"
        else:
            self.__s_portWidthDeclaration = None


    def __str__(self):
        return("portType: " + self.__portType + ", identifier: " + self.__identifier + ", portWidth: " + (self.__s_portWidthDeclaration if self.__s_portWidthDeclaration else "None"))


    def get_identifier(self):
        return self.__identifier


    def get_portType(self):
        return self.__portType


    @classmethod
    def scan(cls, s_lineIn):
        """scans s_lineIn (intended to be a line of Verilog module declaration) for a port declaration

        :s_lineIn: line of Verilog code 
        :returns: VerilogPort object if s_lineIn declared a port; empty list if not
        """
        # check for port declaration and assign if declaration found
        matchObj = re.search(cls.__re_validPortDeclaration, s_lineIn)
        if matchObj:
            portType = matchObj.group(1)
            s_portWidthDeclaration = matchObj.group(3) if matchObj.group(3) else None
            # find identifiers (may be multiple ones) in reduced input string (declaration removed by re.sub)
            identifiers = re.findall( r"[\w-]+", re.sub( cls.__re_validPortDeclaration, "", s_lineIn, count=1 ) )
             
#             for identifier in re.findall( cls.__re_portIdentifier, re.sub( cls.__re_validPortDeclaration, "", s_lineIn ) ):
#                 identifiers.append(identifier)
            
            return [ cls(portType, identifier, s_portWidthDeclaration) for identifier in identifiers ]

        else: 
            return []


    def write_declaration(self, file_out, indentObj: IndentObj):
        """writes a port declaration (without leading or trailing whitespace characters) to the given output file (must be open)

        :file_out: output file
        :indentObj: IndentObj specifying tabwidth and desiredIndentation 
        :language: "Verilog" or "SystemVerilog"
        """
        if self.__s_portWidthDeclaration:
            t_declaration = (self.__portType, self.__s_portWidthDeclaration, self.__identifier)
        else:
            t_declaration = (self.__portType, self.__identifier)

        file_out.write( get_tabbedString(t_declaration, indentObj) )


    def write_reg(self, file_out, indentObj: IndentObj, language: HDL_Enum=HDL_Enum.VERILOG):
        """write a variable declaration to file_out according to the given language
        """
        if self.__s_portWidthDeclaration:
            t_declaration = (language.get_regType(), self.__s_portWidthDeclaration, self.__identifier)
        else:
            t_declaration = (language.get_regType(), self.__identifier)
        
        file_out.write( get_tabbedString(t_declaration, indentObj) )


    def write_instantiation(self, file_out, indentObj, removeIOSuffix=True):
        """writes a port instantiation (without leading or trailing characters) to the given output file (must be open)

        :file_out: output file
        :indentObj: IndentObj specifying tabwidth and desiredIndentation 
        """
        # remove trailing "_i/_o" in identifier for port naming in instantiation
#         if removeIOSuffix and re.search(r"(_i|_in|_input|_o|_out|_output)$", self.__identifier):
#             s_instantiationName = self.__identifier[:-2]
        if removeIOSuffix :
            s_instantiationName = re.sub(r"(_i|_in|_input|_o|_out|_output)$", "", self.__identifier)
        else:
            s_instantiationName = self.__identifier

        t_declaration = ("." + self.__identifier, "(" + s_instantiationName + ")") 
        file_out.write( get_tabbedString(t_declaration, indentObj) )
