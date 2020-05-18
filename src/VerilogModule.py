
import re, sys
from VerilogPort import VerilogPort
from VerilogParameter import VerilogParameter

class VerilogModule():
    """
    functionally represents a Verilog module
    """

    def __init__(self, moduleName, ports, parameters=None, s_timescale=None, outputReg: bool=False):

        self.moduleName     = moduleName
        self.ports          = list(ports) if ports else []
        self.parameters     = list(parameters) if parameters else []
        self.s_timescale    = s_timescale if s_timescale else ""
        self.outputReg      = outputReg

    
    def __str__(self):
        l_print = []
        l_print.extend( ["module: ", self.moduleName, "\n"] )
        l_print.extend( "parameters:\n" )
        for parameter in self.parameters:
            l_print.extend( ["\t", str(parameter), "\n"] )
        l_print.extend( "ports:\n" )
        for port in self.ports:
            l_print.extend( ["\t", str(port), "\n"] )
        l_print.extend( "timescale: " + self.s_timescale + "\n" )
        l_print.extend( "output registers: " + str(self.outputReg) )
        
        return "".join(l_print)


    @classmethod
    def scan(cls, fileDescriptor):
        """
        scans file_in for a Verilog module declaration (looks for the first declaration!)
        If it finds a declaration, returns a corresponding VerilogModule object, otherwise returns None

        :fileDescriptor: either a string or an read-open file
        :returns: VerilogModule object if module declaration is found
        """
        
        # regular expressions to match timescale definition, module declaration, parameter declaration beginning/ending and port declaration beginning/ending
        __re_timescaleDefintion = r"\s*`(timescale)\s*(\w+\s*/\s*\w+)"
        __re_moduleDeclaration = r"\s*(module)\s*([\w-]+)\s*(\(|#\(|)"

        l_parameters = []
        l_ports = []

        # open file if string is passed
        if isinstance( fileDescriptor, str ):
            file_in = open(fileDescriptor, "r") 
        else: 
            file_in = fileDescriptor

        # set file pointer to beginning
        file_in.seek(0)

        moduleFound = False
        s_timescale = ""
        l_ports = []
        l_parameters = []

        currentLine = file_in.readline()

        while currentLine:
            # matchObj will either hold timescale specifiers in matchObj.group(2-3) or module declaration items in matchObj.group(4-6) (if not empty for sure)
            matchObj = re.match("(" + __re_timescaleDefintion + "|" + __re_moduleDeclaration + ")", currentLine)

            # decide between timescale or module declaration
            if  matchObj and matchObj.group(2) == "timescale":
                # remove whitespaces from identified timescale string
                s_timescale = (matchObj.group(3)).replace(" ","")

            elif matchObj and matchObj.group(4) == "module":
                moduleFound = True

                # set file pointer one line up to repeat readline() in scan subfunctions
                file_in.seek( file_in.tell() - len(currentLine) )
                
                moduleName = matchObj.group(5)
                # scan for parameters and ports
                l_parameters = cls.__scanParameters( file_in )
                l_ports = cls.__scanPorts( file_in )

            if moduleFound:
                return cls( 
                        moduleName = moduleName, 
                        ports = l_ports,
                        parameters = l_parameters, 
                        s_timescale = s_timescale )

            currentLine = file_in.readline()

        # end of file reached without module declaration found
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

        

