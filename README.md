# Verilog module generator
This tool generates a code body for a verilog/systemverilog module. You can specify characteristics like input/output ports and parameters directly as command line arguments. The tool also generates a leading commentary section with templates for each specified property. For more precise information refer to the usage section.


## Usage
`verilog_genModule [options] module_name`  

options:
* input ports: `-i <port_name_1>#<port_width_1>,<port_name_2>,...`   
`port_width` is optional, can be either an int or a string (presumably referring to a parameter)  
multiple ports are passed as comma-separated list (not by repetedly specifying `-i` option)
* output ports: `-o <port_name>#<port_width>,...`  
* parameters: `-p <parameter_name1>,<parameter_name2>,...`   
* output registers: `--output-reg`  
generates variables (with respect to language selection) to register output variables
* timescale: `--timescale "timescale"`  
set a timescale for the generated module
* language selection: `--sv`/`--systemverilog`/`--SystemVerilog`  
use SystemVerilog for variable types and file ending if specified, if not, Verilog is used
* include guards: `--include_guards`  
generates include guards at file begin and ending
* author: `-a "author"`/`--author "author"`   
`author` gets automatically inserted in the leading commentary
* tabwidth: `--tabwidth tabwidth`  
`tabwidth` is used to set up proper indentations and alignments for things like port width specifications and identifiers in the code. This option aims to get the generated source code compliant to your editing preferations. Default value is 4. (I apologize if you prefer indenting with spaces rather than tab characters, maybe a great topic for your contribution...)

## Example

* uart receiver in verilog:  
`verilog_genModule -i clk,rst_n,uart_i -o symbol_o#MSG_BITS,newSymbol_o --output-reg -p CLK_FREQ,BAUD_RATE,MSG_BITS --include-guards -a "John Doe" uartRx`

* respective wrapper in systemverilog by other user:  
`verilog_genModule -i clk,rst_n,uart_rxd_out -o symbol_o#8,newSymbol_o --timescale 1ns/1ps -a "N. Otjohndoe" --tabwidth=8 --sv wrapper_uartRx`

resulting files:  
uartRx.v, wrapper_uartRx.sv
