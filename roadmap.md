# Roadmap Verilog module generator (testbench extension)


#### file 'verilog_codeGenerator'
* [ ] parse input arguments
* [ ] decide action (module generation, additional testbench generation, module to testbench, module instantiation (TODO)
* [ ] invoke action

---

#### class 'VerilogFile'
used to hold a VerilogModule plus the additional information which doesn't functionally belong to the module
###### attributes
* verilogModule 
* author
* creationDate
* indentObj
* includeGuards
* language
###### functions
* [ ] write_moduleFile (file_out)
* [ ] write_testbenchFile (file_out)
* [ ] scan (file_in)  
scan input file for language and maybe author, pass to VerilogModule.scan
--- 

#### class 'VerilogModule'  
hold relevant parameters of a verilog module
###### attributes
* moduleName  
* list_ports
* list_parameters
* s_timescale
* outputReg (boolean value)
###### functions
* [ ] init(...)  
init by passing properties directly (intended to be used by module generator)
* [ ] init(file_in)  
call scanner
* [ ] scan(file_in)  
scan file_in and extract VerilogModule from it
* [ ] write_out(file_out, indentObj, language)  
writes the whole module code body (functional part)
* [ ] write_instantiation(file_out, indentObj)
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
* [x] write_declaration(file_out, indentObj, language)  
	write out port declaration (e.g. "input	[7:0] bits")
* [x] write_reg(file_out, indentObj, language)  
	write corresponding variable (e.g. "reg [7:0] bits")
* [x] write_instantiation(file_out, indentObj)  
  	write port instantiation (e.g. ".portName	(portName)")
---

#### module HelperFunctions
* [x] get_tabbedString(attributes, indentObj)  
	attempts to print the tupel in given order, each tupel item at minimum at new tab, so that the last tupel item is at desiredIndentation relative to first item if possible (left tabs are inserted before last item)
