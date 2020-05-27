
`ifndef UARTRX_H
`define UARTRX_H

/*
* company:
* author/engineer:	John Doe
* creation date:	2020-05-27
* project name:
* target devices:
* tool versions:
*
*
* * description:
* [module description]
*
* * interface:
* [interfacing description]
*
*
*		[port name]		- [port description]
* * inputs:
*		clk	
*		rst_n	
*		uart_i	
* * outputs:
*		symbol_o	
*		newSymbol_o	
*
*
* * parameters:
*		CLK_FREQ	
*		BAUD_RATE	
*		MSG_BITS	
*/


module uartRx #(
	parameter				CLK_FREQ,
	parameter				BAUD_RATE = 9600,
	parameter				MSG_BITS
)
(
	input					clk,
	input					rst_n,
	input					uart_i,

	output	[MSG_BITS-1:0]	symbol_o,
	output					newSymbol_o

);

	// output registers
	reg	[MSG_BITS-1:0]		symbol_o;
	reg						newSymbol_o;



endmodule

`endif
