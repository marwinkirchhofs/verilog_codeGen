`timescale 1ns/1ps

/*
* company:
* author/engineer:	Marwin Kirchhofs
* creation date:	2020-05-22
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
*		port1	
*		clk_i	
* * outputs:
*		port2	
* * inout:
*		port3	
*
*
* * parameters:
*		param1	
*		param2	
*/


module mod_init #(
	parameter				param1,
	parameter				param2 = DEF2
)
(
	input	[7:0]			port1,
	input					clk_i,

	output	[MSG_BITS-1:0]	port2,

	inout	[3:0]			port3
);

	// output registers
	logic	[MSG_BITS-1:0]	port2;



endmodule
