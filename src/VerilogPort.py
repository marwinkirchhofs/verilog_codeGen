
#
# represent a Verilog Port
#

import re
from VerilogCodeGen_Helper import *

class VerilogPort:
    """
    represents a Verilog Port
    """

    # valid port types for comparison in instantiation/scanning
    __validPortTypes = ("input","output","inout")
    # pattern to match a port declaration 
    # -> group(1): portType, group(2): s_portWidthDeclaration (may be empty), group(3): identifier
    __validPortDeclaration_pattern = r"\s*(input|output|inout)\s*(\[[\w-]+:[\w-]+\]|)\s*([\w-]+)"


    def __init__(self, portType, identifier, portWidthDeclaration=None):
        """
        creates a VerilogPort, portWidthDeclaration defaults to None
        
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
            

        self.portType   = portType
        self.identifier = identifier
        
        # determine correct port width declaration string (can be passed as int, as full declaration or as string e.g. representing a parameter)
        if portWidthDeclaration:
            try:
                # check for int value
                self.s_portWidthDeclaration = "[" + str(int(portWidthDeclaration) - 1) + ":0]"
            except:
                if re.match(r"\[", portWidthDeclaration):
                    # full declaration passed
                    self.s_portWidthDeclaration = portWidthDeclaration
                else:
                    # parameter identifier passed
                    self.s_portWidthDeclaration = "[" + portWidthDeclaration + "-1:0]"
        else:
            self.s_portWidthDeclaration = None


    def __str__(self):
        return("portType: " + self.portType + ", identifier: " + self.identifier + ", portWidth: " + self.s_portWidthDeclaration)


    @classmethod
    def scan(cls, s_lineIn):
        """
        scans s_lineIn (intended to be a line of Verilog module declaration) for a port declaration

        :s_lineIn: line of Verilog code 
        :returns: VerilogPort object if s_lineIn declared a port; None if not
        """
        # check for port declaration and assign if declaration found
        matchObj = re.search(cls.__validPortDeclaration_pattern, s_lineIn)
        if matchObj:
            portType = matchObj.group(1)
            s_portWidthDeclaration = matchObj.group(2) if matchObj.group(2) else None
            identifier = matchObj.group(3)
            
            return cls(portType, identifier, s_portWidthDeclaration)
        else: 
            return None


    def write_declaration(self, file_out, indentObj: IndentObj):
        """
        writes a port declaration (without leading or trailing whitespace characters) to the given output file (must be open)

        :file_out: output file
        :indentObj: IndentObj specifying tabwidth and desiredIndentation 
        :language: "Verilog" or "SystemVerilog"
        """
        if self.s_portWidthDeclaration:
            t_declaration = (self.portType, self.s_portWidthDeclaration, self.identifier)
        else:
            t_declaration = (self.portType, self.identifier)

        file_out.write( get_tabbedString(t_declaration, indentObj) )


    def write_reg(self, file_out, indentObj: IndentObj, language: HDL_Enum=HDL_Enum.VERILOG):
        """ 
        write an variable declaration to file_out according to the given language
        """
        if self.s_portWidthDeclaration:
            t_declaration = (language.get_regType(), self.s_portWidthDeclaration, self.identifier)
        else:
            t_declaration = (language.get_regType(), self.identifier)
        
        file_out.write( get_tabbedString(t_declaration, indentObj) )


    def write_instantiation(self, file_out, indentObj, removeIOSuffix=True):
        """
        writes a port instantiation (without leading or trailing characters) to the given output file (must be open)

        :file_out: output file
        :indentObj: IndentObj specifying tabwidth and desiredIndentation 
        """
        # remove trailing "_i/_o" in identifier for port naming in instantiation
        if removeIOSuffix and re.search(r"[_i|_o]$", self.identifier):
            s_instantiationName = self.identifier[:-2]
        else:
            s_instantiationName = self.identifier

        t_declaration = ("." + self.identifier, "(" + s_instantiationName + ")") 
        file_out.write( get_tabbedString(t_declaration, indentObj) )
