
`timescale 1ns/1ps

`ifndef ARTYWRAPPER_UARTCONTROLLER_H
`define ARTYWRAPPER_UARTCONTROLLER_H

/*
* company:
* author/engineer:	Marwin Kirchhofs
* creation date:	2020-05-18
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
* * inputs:
*		[port name]		- [port description]
*		CLK100MHZ	
*		ck_rst	
*		uart_rxd_out	
* * outputs:
*		uart_txd_in	
*/


module artyWrapper_uartController 

#( parameter PARAM = 12, SECOND_PARAM )


( input CLK100MHZ,
	input					ck_rst, rst_p,
	input					uart_rxd_out,
	output	[7:0]			one_more_input, one_second_input,
	inout					arbitrary_inout_port,
	input	[MSG_BITS:0]			and_another_i,
	inout	[255-1:0]		HUUUGGE_port,

	output					uart_txd_in
);






endmodule

`endif
