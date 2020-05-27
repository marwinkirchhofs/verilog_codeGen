`timescale 1ns/1ps

/*
* company:
* author/engineer:	N. Otjohndoe
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
*		uart_rxd_out	
* * outputs:
*		symbol_o	
*		newSymbol_o	
*/


module wrapper_uartRx (
	input			clk,
	input			rst_n,
	input			uart_rxd_out,

	output	[7:0]		symbol_o,
	output			newSymbol_o

);



endmodule
