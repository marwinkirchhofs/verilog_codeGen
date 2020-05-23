# Verilog code generator
This tool generates different code blocks/files for Verilog/SystemVerilog modules.  
Features are:  
* ##### module file generation based on command line arguments  
You can specify characteristics like input/output ports and parameters directly as command line arguments. The tool also generates a leading commentary section with templates for each specified property. For more precise information refer to the usage section.  
	* optional additional generation of a suitable testbench file  
* ##### testbench generation for an existing Verilog/SystemVerilog file  
This scans an existing Verilog/SystemVerilog file for a module declaration and generates a matching testbench. The language is derived from the found module or the file extension of the command line argument. (Please note that explicitly specifying a non-matching language via e.g. --sv is invalid. If you encounter a case where generating for example a SystemVerilog testbench for a Verilog file is needed, feel free to report it to me ;-) )  
* (planned: generation of a module instantiation for a given input file with the definition of the instantiated module not necessarily in the current working directory)  

If you encounter any errors or have suggestions, please feel free to contact me. (I myself do not have years of Verilog experience. It just felt like a good idea to write a small empty-module-generation tool during some private projects which ended up escalating a bit ;-) ) 


## Usage
`verilog_codeGen [options] <module_name/file_name>`  
(assuming you symlinked `src/verilog_codeGen.py` to `verilog_codeGen` somewhere in your `$PATH`)  
Each usage works with either a module or a file name as argument.

##### options
* ##### file generation from command line arguments
	* input ports: `-i <port_name_1>#<port_width_1>,<port_name_2>,...`   
	`port_width` is optional, can be either an int or a string (presumably referring to a parameter)  
	multiple ports are passed as comma-separated list (not by repeatedly specifying `-i` option)
	* output ports: `-o <port_name>#<port_width>,...`  
	same as input ports
	* parameters: `-p <parameter_name1>=<default value>,<parameter_name2>,...`   
	default parameter is optional, same scheme as input ports
	* output registers: `--output-reg`  
	generates variables (with respect to language selection) to register output variables
	* language selection: `--sv`/`--systemverilog`/`--SystemVerilog`  
	use SystemVerilog for variable types and file ending if specified, if not, Verilog is used
	* include guards: `--include_guards`  
	generates include guards at file begin and ending
	* add testbench: `--add-testbench`/`--add-tb`  
	generates an additional testbench file for the specified module

* ##### testbench generation from existing file
  	* testbench generation: `--testbench`/`--tb`  
  	causes `module_name`/`file_name` to be scanned (if it is in current directory) and invokes the generation of a suitable testbench file

* ##### general options
	* author: `-a "author"`/`--author "author"`   
	`author` gets automatically inserted in the leading commentary
	* timescale: `--timescale "timescale"`  
	set a timescale for the generated module
	* tabwidth: `--tabwidth tabwidth`  
	`tabwidth` is used to set up proper indentations and alignments for things like port width specifications and identifiers in the code. This option aims to get the generated source code compliant to your editing preferations. Default value is 4. (I apologize if you prefer indenting with spaces rather than tab characters, maybe a great topic for your contribution...)
* ##### help: `-h`/`--help`  
display help messages


## Examples

(different assignment syntaxes just show the possibilities, everything works which is compliant to python module optparse)

* ##### module generation  
	* uart receiver in verilog:  
`verilog_codeGen -i clk,rst_n,uart_i -o symbol_o#MSG_BITS,newSymbol_o --output-reg -p CLK_FREQ,BAUD_RATE,MSG_BITS --include-guards --author="John Doe" uartRx`

	* respective wrapper in systemverilog by other user:  
`verilog_codeGen -i clk,rst_n,uart_rxd_out -o symbol_o#8,newSymbol_o --timescale 1ns/1ps -a "N. Otjohndoe" --tabwidth=8 --sv wrapper_uartRx`  

	resulting files:  
	uartRx.v  
	wrapper_uartRx.sv

* ##### testbench generation:  
`verilog_codeGen --tb --tabwidth=8 -a "Mr. TB" --timescale "1ns/1ps" wrapper_uartRx.sv`

	resulting file:  
	tb_wrapper_uartRx.sv


## Future work
##### SystemVerilog multi-dimensional (packed and unpacked) arrays  
So far, the tool only supports one-dimensional (packed) arrays. This needs to be adapted to the extended capabilities of SystemVerilog in an update.

##### module instantiation, configuration  
As stated above, I'm working on also providing a command to print an instantiation for a specified module which then needs to be redirected to the opened file in your text editor of choice. I would like it to contain an option to try to automatically insert an include statement, but I'm not sure about how complex this is to implement in a way which can be used independently from the chosen text editor.
I think that it would be nice to have the possibility to also instantiate modules which are not in your current working directory (or a subdirectory) with the same command. Therefore, I'm planning to integrate a configuration file where you can specify search paths for module definition files used by this command. 
And if it's already there, why not allowing to set an author and maybe a tabwidth in the configuration file so that these automatically get used at each invocation if not manually overwritten.
