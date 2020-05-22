# Roadmap Verilog module generator (testbench extension)

#### general TODOs
* [ ] make it possible for each command to pass either a module or a file name as argument (don't ask me which classes are affected by this)
 
---

#### file 'verilog_codeGenerator'
* [x] parse input arguments
* [x] decide action (module generation, additional testbench generation, module to testbench, module instantiation (TODO) )
* [x] invoke action  
TODO: implement module instantiation

---

#### class 'Verilog_codeGen_config'
class to hold a configuration containing:
* search paths for module instantiation
* author  
###### methods
* [ ] readConfig(cls, file_in)  
  reads a config file (no idea of which format yet) and returns a Verilog_codeGen_config object in case of successful reading
* [ ] findModule(self, moduleName)  
  find the specified module in the search paths (recursively), order:  1) current working directory, 2) search paths
if multiple modules found, prompt which one should be instantiated  
(TODO: maybe this method fits better in an own class or somewhere else, we will see. But this way it has direct access to the search path variable)

---

#### class 'VerilogFile'
used to hold a VerilogModule plus the additional information which doesn't functionally belong to the module
###### attributes
* verilogModule 
* s_timescale
* author
* creationDate
* indentObj
* includeGuards
* language
###### functions
* [x] write_moduleFile (file_out)
* [x] write_testbenchFile (file_out)
* [x] scan (file_in)  
  TODO: preprocess file_in to eliminate commentaries completely from the code (needed e.g. for error-safe module declaration scanning)
scan input file for language and maybe author, pass to VerilogModule.scan
--- 

#### class 'VerilogModule'  
hold relevant parameters of a verilog module  
TODO: move s_timescale to VerilogFile
###### attributes
* moduleName  
* list_ports
* list_parameters
* outputReg (boolean value)
###### functions
* [x] init(...)  
init by passing properties directly (intended to be used by module generator)
* [x] scan(file_in)  
scan file_in and extract VerilogModule from it  
TODO: is not able to handle Verilog 1995 style parameter declarations (declaration after module declaration); presumably will never be...
* [x] write_declaration(file_out, indentObj, language)  
writes the whole module code body (functional part)
* [x] write_instantiation(file_out, indentObj)  
generates a module instantiation (connected variable names equal to internal port names)
---

#### class 'VerilogPort'  
full port description  
###### attributes  
* identifier
* portType (input, output, inout)
* width (ideally directly as string to handle different formats)
###### functions
* [x] scan(s_lineIn)  
	scans a line of code and attempts to extract a port from it  
	TODO: does only work with one-dimensional (packed) ports
* [x] write_declaration(file_out, indentObj, language)  
	write out port declaration (e.g. "input	[7:0] bits")
* [x] write_reg(file_out, indentObj, language)  
	write corresponding variable (e.g. "reg [7:0] bits")
* [x] write_instantiation(file_out, indentObj)  
  	write port instantiation (e.g. ".portName	(portName)")
---

#### class 'VerilogParameter'  
full parameter description  
###### attributes  
* identifier
* default value
###### functions
* [x] scan(s_lineIn)  
	scans a line of code and attempts to extract parameters port from it
* [x] write_declaration(file_out, indentObj, language)  
	write out parameter declaration (e.g. "parameter MY_PARAM")
* [x] write_instantiation(file_out, indentObj)  
  	write parameter instantiation (e.g. ".PARAM_NAME (PARAM_NAME)")
---

#### module HelperFunctions
* [x] get_tabbedString(attributes, indentObj)  
	attempts to print the tupel in given order, each tupel item at minimum at new tab, so that the last tupel item is at desiredIndentation relative to first item if possible (left tabs are inserted before last item)
