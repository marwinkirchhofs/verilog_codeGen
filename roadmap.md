# Roadmap Verilog module generator (testbench extension)

#### general TODOs
* [ ] add support for SystemVerilog multi-dimensional and packed/unpacked arrays
* [ ] allow directories to be explicitly ignored in searchPaths by setting a leading '!' in the searchPaths element (similar to .gitignore file)
* [ ] include a preprocessor removing comments
 
---

#### file 'verilog_codeGenerator'
* [x] parse input arguments
* [x] decide action (module generation, additional testbench generation, module to testbench, module instantiation)
* [x] invoke action  

---

#### class 'Verilog_codeGen_config'
class to hold a configuration containing:
* search paths for module instantiation
* author  
###### methods
* [x] init(self, searchPaths, author, tabwidth, configFile)
* [x] from_Config(cls)  
  reads a json config file and returns a Verilog_codeGen_config object in case of successful reading  
config file is obtained from \_\_findConfig()
* [ ] write_template(cls, path="")  (TODO)
writes a config template to be edited by user to path (or to top level or src directory if path is empty)
* [x] write_config(self)
writes the config object out to the json file specified in self.\_\_configFile (may not be needed as the file is intended to be edited by user, but useful for testing and maybe for writing an empty config file as template)

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
###### methods
* [x] write_moduleFile (file_out)
* [x] write_testbenchFile (file_out)
* [x] scan (file_in)  
  TODO: preprocess file_in to eliminate commentaries completely from the code (needed e.g. for error-safe module declaration scanning)
scan input file for language and maybe author, pass to VerilogModule.scan
--- 

#### class 'VerilogModule'  
hold relevant parameters of a verilog module  
###### attributes
* moduleName  
* list_ports
* list_parameters
* outputReg (boolean value)
###### methods
* [x] init(...)  
init by passing properties directly (intended to be used by module generator)
* [x] scan(file_in)  
scan file_in and extract VerilogModule from it  
TODO: is not able to handle Verilog 1995 style parameter declarations (declaration after module declaration); presumably will never be...
* [x] write_declaration(file_out, indentObj, language)  
writes the whole module code body (functional part)
* [x] write_instantiation(file_out, indentObj)  
generates a module instantiation (connected variable names equal to internal port names)
* [x] findModuleFile(cls, moduleName, config)  
  find the specified module in the config's search paths (recursively), order:  1) current working directory, 2) search paths
if multiple modules found, prompt which one should be instantiated  

---

#### class 'VerilogPort'  
full port description  
###### attributes  
* identifier
* portType (input, output, inout)
* width (ideally directly as string to handle different formats)
###### methods
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
###### methods
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
