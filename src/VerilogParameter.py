
import re
from VerilogCodeGen_Helper import *

class VerilogParameter:
    """represents a Verilog Parameter
    """

    # (TODO:) maybe move those patterns as static parameters to the scan method, if they don't get used somewhere else
    # pattern to match a parameter declaration 
    # -> group(1): parameterType, group(2): variable type (if given), group(3): s_parameterWidthDeclaration (if given)
    __re_validParameterDeclaration = r".*parameter\s+"
    # pattern to look for identifiers in a parameter declaration (with declaration part deleted by re.sub -> string starting with parameter name(s) )
    # parameter identifier will be zeroeth element of match, default value will be second element
    __re_parameterIdentifier = r"([\w-]+)\s*(=\s*([\w-]+))?"


    def __init__(self, identifier, defaultValue=""):
        """creates a VerilogParameter
        
        :identifier: parameter name
        """
        if not identifier:
            print("Identifier must not be empty!")
            return None

        self.identifier = identifier
        self.defaultValue = defaultValue 


    @classmethod
    def fromParameterDescription(self, s_parameterDescription):
        """creates a VerilogParameter for a parameter description with syntax: <parameterName>[=<default value>]
        """
        l_parameterProperties = re.split(r"=", s_parameterDescription)
        identifier = l_parameterProperties[0]
        defaultValue = l_parameterProperties[1] if len(l_parameterProperties) > 1 else ""
        return cls(identifier, defaultValue)


    def __str__(self):
        return("identifier: " + self.identifier + ", default value: " + self.defaultValue)


    @classmethod
    def scan(cls, s_lineIn):
        """scans s_lineIn (intended to be a line of Verilog module declaration) for a parameter declaration

        :s_lineIn: line of Verilog code 
        :returns: list of VerilogParameter objects if s_lineIn declared at least one parameter; None if not
        """
        l_parameters = []

        # check for parameter declaration and assign if declaration found
        matchObj = re.search(cls.__re_validParameterDeclaration, s_lineIn)
        if matchObj:
            
            # find identifiers and default values (may be multiple ones) in reduced input string (declaration removed by re.sub)
            for parameterMatch in re.findall( cls.__re_parameterIdentifier, re.sub( "(" + cls.__re_validParameterDeclaration + r"|\).*$)", "", s_lineIn ) ):
                l_parameters.append( cls(parameterMatch[0], parameterMatch[2]) )
            
        return l_parameters


    def write_declaration(self, file_out, indentObj: IndentObj):
        """writes a parameter declaration (without leading or trailing whitespace characters) to the given output file (must be open)

        :file_out: output file
        :indentObj: IndentObj specifying tabwidth and desiredIndentation 
        :language: "Verilog" or "SystemVerilog"
        """
        if self.defaultValue:
            t_declaration = ("parameter", self.identifier + " = " + self.defaultValue)
        else:
            t_declaration = ("parameter", self.identifier)

        file_out.write( get_tabbedString(t_declaration, indentObj) )


    def write_instantiation(self, file_out, indentObj):
        """writes a parameter instantiation (without leading or trailing characters) to the given output file (must be open)

        :file_out: output file
        :indentObj: IndentObj specifying tabwidth and desiredIndentation 
        """
        t_declaration = ("." + self.identifier, "(" + self.defaultValue + ")") 
        file_out.write( get_tabbedString(t_declaration, indentObj) )
