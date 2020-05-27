
import re, sys, os
from VerilogPort import VerilogPort
from VerilogParameter import VerilogParameter
from VerilogCodeGen_Helper import *

class VerilogModule():
    """
    functionally represents a Verilog module
    """

    def __init__(self, moduleName, ports, parameters=None, outputReg: bool=False):

        self.moduleName     = moduleName
        self.ports          = { "input": [], "output": [], "inout": [] }
        for port in ports:
            self.ports[ port.get_portType() ].append(port)
        self.l_parameters   = list(parameters) if parameters else []
        self.outputReg      = outputReg

    
    def __str__(self):
        l_print = []
        l_print.extend( ["module: ", self.moduleName, "\n"] )
        l_print.extend( "parameters:\n" )
        for parameter in self.l_parameters:
            l_print.extend( ["\t", str(parameter), "\n"] )
        l_print.extend( "ports:\n" )
        for port in self.ports["input"]:
            l_print.extend( ["\t", str(port), "\n"] )
        for port in self.ports["output"]:
            l_print.extend( ["\t", str(port), "\n"] )
        for port in self.ports["inout"]:
            l_print.extend( ["\t", str(port), "\n"] )
        l_print.extend( "output registers: " + str(self.outputReg) )
        
        return "".join(l_print)


    @classmethod
    def scan(cls, fileDescriptor):
        """
        scans file_in for a Verilog module declaration (looks for the first declaration!)
        If it finds a declaration, returns a corresponding VerilogModule object, otherwise returns None

        :fileDescriptor: either a string or a read-open file
        :returns: VerilogModule object if module declaration is found, else None
        """
        
        # regular expression to match module declaration, parameter declaration beginning/ending and port declaration beginning/ending
#         __re_moduleDeclaration = r"\s*module\s+([\w-]+)\s*(\(|#\(|)"
        __re_moduleDeclaration = r"\s*module\s+([\w-]+)"

        l_parameters = []
        l_ports = []

        # open file if string is passed
        if isinstance( fileDescriptor, str ):
            file_in = open(fileDescriptor, "r") 
        else: 
            file_in = fileDescriptor

        # set file pointer to beginning
        file_in.seek(0)

        l_ports = []
        l_parameters = []

        currentLine = file_in.readline()

        while currentLine:
            # matchObj will hold module declaration items in matchObj.group(4-6) (if not empty for sure)
            matchObj = re.match( __re_moduleDeclaration , currentLine)

            if matchObj:
                
                # set file pointer one line up to repeat readline() in scan subfunctions
                file_in.seek( file_in.tell() - len(currentLine) )
                
                moduleName = matchObj.group(1)
                # scan for parameters and ports
                l_parameters = cls.__scanParameters( file_in )
                l_ports = cls.__scanPorts( file_in )

                return cls( 
                        moduleName = moduleName, 
                        ports = l_ports,
                        parameters = l_parameters )

            currentLine = file_in.readline()

        # end of file reached without module declaration found
        return None


    def write_declaration(self, file_out, indentObj: IndentObj, language: HDL_Enum=HDL_Enum.VERILOG):
        """writes a complete module declaration to file_out (must be open!) 

        :file_out: output file; may be passed as string or as file object
        :indentObj: IndentObj to handle indentations
        :language: HDL_Enum object to specify HDL language
        """
        if file_out.closed:
            print("file_out must be open!")
            return None

        #### write module interface ####

        # parameters
        if self.l_parameters:
            file_out.write("module " + self.moduleName + " #(\n")
            for parameter in self.l_parameters:
                file_out.write("\t")
                parameter.write_declaration(file_out, indentObj)
                if not parameter == self.l_parameters[-1]:
                    file_out.write(",")
                file_out.write("\n")

            file_out.write(")\n")
            file_out.write("(\n")
        else:
            file_out.write("module " + self.moduleName + " (\n")

        # inputs
        for port in self.ports["input"]:
            file_out.write("\t")
            port.write_declaration(file_out, indentObj)
            if not port == self.ports["input"][-1] or self.ports["output"] or self.ports["inout"]:
                file_out.write(",")
            file_out.write("\n")

        if self.ports["input"]: writeBlankLines(file_out,1)
        
        # outputs
        for port in self.ports["output"]:
            file_out.write("\t")
            port.write_declaration(file_out, indentObj)
            if not port == self.ports["output"][-1] or self.ports["inout"]:
                file_out.write(",")
            file_out.write("\n")

        if self.ports["output"]: writeBlankLines(file_out,1)

        # inout
        for port in self.ports["inout"]:
            file_out.write("\t")
            port.write_declaration(file_out, indentObj)
            if not port == self.ports["inout"][-1]:
                file_out.write(",")
            file_out.write("\n")

        file_out.write(");\n")

        #### output register instantiations ####

        if self.outputReg:

            writeBlankLines(file_out,1)
            file_out.write("\t// output registers\n")
            for port in self.ports["output"]:
                file_out.write("\t")
                port.write_variable(file_out, indentObj, language)
                file_out.write(";\n")
        
        #### module body ####
        writeBlankLines(file_out,3)

        # end module
        file_out.writelines("endmodule\n")


    def write_instantiation(self, file_out, indentObj: IndentObj):
        """writes a module istantiation to file_out (must be open!) 

        :file_out: output file; may be passed as string or as file object
        :indentObj: IndentObj to handle indentations
        """
        if file_out.closed:
            print("file_out must be open!")
            return None

        #### write module interface ####

        # parameters
        if self.l_parameters:
            file_out.write(self.moduleName + " #(\n")
            for parameter in self.l_parameters:
                file_out.write("\t")
                parameter.write_instantiation(file_out, indentObj)
                if not parameter == self.l_parameters[-1]:
                    file_out.write(",")
                file_out.write("\n")

            file_out.write(") mod_" + self.moduleName + " (\n")
        else:
            file_out.write(self.moduleName + " mod_" + self.moduleName + " (\n")

        # inputs
        for port in self.ports["input"]:
            file_out.write("\t")
            port.write_instantiation(file_out, indentObj)
            if not port == self.ports["input"][-1] or self.ports["output"] or self.ports["inout"]:
                file_out.write(",")
            file_out.write("\n")

        if self.ports["input"]: writeBlankLines(file_out,1)
        
        # outputs
        for port in self.ports["output"]:
            file_out.write("\t")
            port.write_instantiation(file_out, indentObj)
            if not port == self.ports["output"][-1] or self.ports["inout"]:
                file_out.write(",")
            file_out.write("\n")

        if self.ports["output"]: writeBlankLines(file_out,1)

        # inout
        for port in self.ports["inout"]:
            file_out.write("\t")
            port.write_instantiation(file_out, indentObj)
            if not port == self.ports["inout"][-1]:
                file_out.write(",")
            file_out.write("\n")

        file_out.write(");\n")


    def write_includeGuards(self, file_out, s_topBottom):
        """writes include guards for top or bottom of file

        :file_out:  opened output file
        :s_topBottom: specify if top or bottom ("`ifndef ..." or "`endif ...") shall be written, valid values: "top"/"bottom"
        """
        # no file checking here, just a helper function
        if s_topBottom == "top":
            file_out.write("`ifndef " + self.moduleName.upper() + "_H\n")
            file_out.write("`define " + self.moduleName.upper() + "_H\n")

        elif s_topBottom == "bottom":
            file_out.write("`endif\n")

        else:
            print("invalid file position declarator: " + s_topBottom)
            return None


    @classmethod
    def __scanParameters(cls, file_in):
        """scans a module declaration for parameters

        :file_in: input file, must be read-open with file-pointer at the line before(!) the module declaration 
        :returns: list of found VerilogParameter objects
        """
        l_parameters = [] 
        
        currentLine = file_in.readline()
        blockTokens = cls.__get_paramPortDeclTokens(currentLine) 
        
        # read lines until parameter or port block start is detected
        while not blockTokens or not blockTokens["paramBegin"]:
            if blockTokens and (blockTokens["portBegin"] or blockTokens["modDeclarationEnd"]):
                # no parameter block -> go back one line to allow next scanner to start in same line
                file_in.seek( file_in.tell() - len(currentLine) )
                return l_parameters
            else:
                currentLine = file_in.readline()
                blockTokens = cls.__get_paramPortDeclTokens(currentLine) 
            
            # prevent endless loop in case of errorneous code
            if not currentLine:
                print("Declaration block detection reached end of file! Exiting with syntax error")
                sys.exit(1)

        # parameter block begin found
        while True:
            l_parameters.extend( VerilogParameter.scan(currentLine) ) 
            if blockTokens and blockTokens["paramOrPortEnd"]:
                # parameter block ended -> go back one line to allow next scanner to start in same line
                file_in.seek( file_in.tell() - len(currentLine) )
                return l_parameters
            else:
                currentLine = file_in.readline()
                blockTokens = cls.__get_paramPortDeclTokens(currentLine) 

            # prevent endless loop in case of errorneous code
            if not currentLine:
                print("Parameter detection reached end of file! Exiting with syntax error")
                sys.exit(1)


    @classmethod
    def __scanPorts(cls, file_in):
        """scans a module declaration for ports

        :file_in: input file, must be read-open with file-pointer at the line before(!) the beginning of the port declaration
        :returns: list of found VerilogPort objects 
        """
        l_ports = [] 
        
        currentLine = file_in.readline()
        blockTokens = cls.__get_paramPortDeclTokens(currentLine) 
        
        # read lines until port block start is detected
        while not blockTokens or not blockTokens["portBegin"]:
            if blockTokens and blockTokens["modDeclarationEnd"]:
                # no port block -> go back one line to allow next scanner to start in same line
                file_in.seek( file_in.tell() - len(currentLine) )
                return l_ports
            else:
                currentLine = file_in.readline()
                blockTokens = cls.__get_paramPortDeclTokens(currentLine) 

        while True:
            l_ports.extend( VerilogPort.scan(currentLine) ) 
            if blockTokens and (
                    (
                            blockTokens["paramOrPortEnd"] and not 
                            blockTokens["paramBegin"]
                    ) or 
                            blockTokens["paramAndPortEnd"] ) :
                # port block ended -> go back one line to allow next scanner to start in same line
                file_in.seek( file_in.tell() - len(currentLine) )
                return l_ports
            else:
                currentLine = file_in.readline()
                blockTokens = cls.__get_paramPortDeclTokens(currentLine) 

            # just to prevent endless loop in case of errorneous code
            if not currentLine:
                print("Port detection reached end of file! Exiting with syntax error")
                sys.exit(1)


    @classmethod
    def __get_paramPortDeclTokens(cls, s_lineIn):
        """looks for begin/end identifiers for port ar parameter declaration blocks in s_lineIn

        :s_lineIn: one line of code
        :returns: dictionary containing boolean values for paramBegin, paramEnd, portBegin, portEnd
        """
         
        # regex to identify beginning/ending parameter and port declaration blocks by boolean combinations of the 4 l_blockTokens values
        __re_paramPortDeclBegin = r"(#\(|\(|\)|;)"
        l_blockTokens = re.findall( __re_paramPortDeclBegin, s_lineIn )

        if l_blockTokens:
            return  {   "paramBegin": "#(" in l_blockTokens,
                        "portBegin": "(" in l_blockTokens, 
                        "paramOrPortEnd": ")" in l_blockTokens,
                        "paramAndPortEnd": l_blockTokens.count(")") == 2,
                        "modDeclarationEnd": ";" in l_blockTokens, 
                    }
        else:
            return None

        
    @classmethod
    def generate_instantiationFromSearch(cls, moduleName, configObj, fileDescriptor=None, indentObj=None ):
        """searches the configObj's searchPaths for an instantiation matching moduleName, queries if multiple module files were found and afterwords either writes an instantiation to file_out or, if empty, simply prints it to be redirected e.g. via the text editor

        :moduleName: name of the module (may optionally contain ".v/.sv" ending)
        :configObj: Verilog_codeGen_config whose searchPaths is used
        :indentObj: IndentObj which overrides configObj.tabwidth
        """
        if not indentObj:
            indentObj = IndentObj(tabwidth = configObj.tabwidth if configObj.tabwidth else 4)

        # determine module to be instantiated
        l_foundModules = cls.__find_moduleFiles(moduleName, configObj)

        if not l_foundModules:
            print("No modules found for module name '" + moduleName + "'!")
        elif len(l_foundModules) == 1:
            s_selectedModule = l_foundModules[0]
        else:
            print("Multiple module were found:")
            count = 0
            for moduleFile in l_foundModules:
                print( str(count) + ") " + moduleFile )
                count += 1
                
            i_selectedModule = input("Please enter the number of the desired module (any other character to abort):")
            
            try:
                if int(i_selectedModule) in range(len(l_foundModules)):
                    # valid module selection
                    s_selectedModule = l_foundModules[int(i_selectedModule)]
                else:
                    return None
            except Exception:
                return None

        # generate module object from s_selectedModule 
        selectedModule = cls.scan( s_selectedModule )

        # write instantiation to file_out or print it
        if fileDescriptor:
            if isinstance(fileDescriptor, str):
                file_out = open(fileDescriptor, "w")
            else:
                file_out = fileDescriptor
        else:
            file_out = sys.stdout

        selectedModule.write_instantiation( file_out, indentObj )
            

    @classmethod
    def __find_moduleFiles(cls, moduleName, configObj):
        """recursively searches the moduleName in current working directory and in configObj.searchPaths

        :moduleName: name of the module (may optionally contain ".v/.sv" ending)
        :configObj: Verilog_codeGen_config whose searchPaths is used
        :returns: list of found matches
        """
        # determine string to be searched dependant on file ending if given
        if re.search(r"(\.v|\.sv)\s*$", moduleName):
            re_searchModule = r"^" + moduleName
        else:
            re_searchModule = r"^" + moduleName + r"(\.v|\.sv)\s*$"

        l_foundModules = []

        # iterate through current working directory to find modules
        for (path, directories, filenames) in os.walk( os.getcwd() ):
            # covering the unusual case that a module exists in both Verilog and SystemVerilog
            l_foundModules.extend(
                    [ path + "/" + filename for filename in filenames if re.search(re_searchModule, filename) ] )

        # iterate through searchPaths and find re_searchModule recursively
        for searchPath in configObj.searchPaths:
            for (path, directories, filenames) in os.walk(searchPath):
                # covering the unusual case that a module exists in both Verilog and SystemVerilog
                l_foundModules.extend(
                        [ path + "/" + filename for filename in filenames if re.search(re_searchModule, filename) ] )
        
        return l_foundModules
