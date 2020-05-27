# Verilog/SystemVerilog code generator
This tool generates different code blocks/files for Verilog/SystemVerilog modules.  
Features are:  
* ##### module file generation based on command line arguments (with optional additional testbench generation)
	You can specify characteristics like input/output ports and parameters directly as command line arguments. The tool also generates a leading commentary section with templates for each specified property. For more precise information refer to the usage section.   
* ##### testbench generation for an existing Verilog/SystemVerilog file  
	This scans an existing Verilog/SystemVerilog file for a module declaration and generates a matching testbench. The language is derived from the found module or the file extension of the command line argument. (Please note that explicitly specifying a non-matching language via e.g. --sv is invalid. If you run into a case where generating for example a SystemVerilog testbench for a Verilog file is needed, feel free to give me a feedback)  
* ##### generation of a module instantiation from a searched file
	_! Note that this feature is in a beta/test state !_  
I think that it would be really helpful to have the possibility of getting a module instantiation generated from within the text editor you're currently writing in. As at least in my workflow often used module often do not reside in the directory/project I'm currently working on, I wanted to make it possible to also instantiate those modules without much overhead.  
Therefore, it is possible to set up `searchPaths` in a configuration file which are then recursively scanned for the specified module/file. Additionally, the current working directory always also get's scanned. It is possible to pass a module name with or without file name. In the latter case, both Verilog and SystemVerilog files are searched.  
Issue: My intention is to redirect the command's output via the text editor (e.g. `:read` in vim). This currently only works properly if just one matching file is found. In the current state, in the case of multiple matches, the tool prompts which module you want to get instantiated. I assume this not to be visible as an editor reading from a terminal command waits for the command to terminate until it shows the output (at least, vim does).  
I currently do not know what the best solution to this would be, but I still wanted to provide the functionality with this disclaimer. If you have an idea on that or a feedback for me how it would suit your workflow, I'm really looking forward to getting your input!

If you encounter any errors, miss features or have other suggestions, please don't hesitate to contact me. (I myself do not have years of Verilog experience. It just felt like a good idea to write a small empty-module-generation tool during some private projects which ended up escalating a bit and slightly influencing my exam period ;-) ) 


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

* ##### module instantiation from file search
  	* module search mode: `--module-instantiation`/`--mod-inst`/`--modInst`  

* ##### configuration
  	* write empty configuration file: `--config-template`  
  	  	In this case, target directory is passed as argument (optionally) rather than modulename/filename. It is therefore not usable at the same time with other actions.

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
`verilog_codeGen -i clk,rst_n,uart_i -o symbol_o#MSG_BITS,newSymbol_o --output-reg -p CLK_FREQ,BAUD_RATE=9600,MSG_BITS --include-guards --author="John Doe" uartRx`

	* respective wrapper in systemverilog by other user:  
`verilog_codeGen -i clk,rst_n,uart_rxd_out -o symbol_o#8,newSymbol_o --timescale 1ns/1ps -a "N. Otjohndoe" --tabwidth=8 --sv wrapper_uartRx`  

* ##### testbench generation:  
	`verilog_codeGen --tb --tabwidth=8 -a "Mr. TB" --timescale "1ns/1ps" wrapper_uartRx.sv`

The resulting files can be found in the `Examples` directory to give you an impression.


## Future work
##### SystemVerilog multi-dimensional (packed and unpacked) arrays  
So far, the tool only supports one-dimensional (packed) arrays. This needs to be adapted to the extended capabilities of SystemVerilog in an update.

##### commentary elimination
Comments in the module declaration containing tokens like '(',')' or ';' may cause file scanning to not work correctly. My plan is to integrate a preprocessor to eliminate all commentaries from a file in temporary file when scanning a file.

