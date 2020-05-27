`timescale 1ns/1ps

/*
* testbench for artyWrapper_uartController
* 
* company:
* author/engineer:	
* creation date:	2020-05-22
* project name:
* tool versions:
*/

module tb_artyWrapper_uartController;

	// dut inputs
	logic					CLK100MHZ;
	logic					ck_rst;
	logic					rst_p;
	logic					uart_rxd;
	logic	[MSG_BITS:0]	and_another;

	// dut output
	logic	[7:0]			one_more;
	logic	[7:0]			one_second;
	logic					uart_txd;

	// dut inout
	wire					arbitrary_inout_port;
	wire	[255-1:0]		HUUUGGE_port;


	always begin
		 #5 		CLK100MHZ <= ~CLK100MHZ;
	end


	initial begin
		CLK100MHZ <= 1;


		$finish
	end


artyWrapper_uartController #(
	.PARAM					(12),
	.SECOND_PARAM			()
) mod_artyWrapper_uartController (
	.CLK100MHZ				(CLK100MHZ),
	.ck_rst					(ck_rst),
	.rst_p					(rst_p),
	.uart_rxd_out			(uart_rxd),
	.and_another_i			(and_another),

	.one_more_input			(one_more),
	.one_second_input		(one_second),
	.uart_txd_in			(uart_txd),

	.arbitrary_inout_port	(arbitrary_inout_port),
	.HUUUGGE_port			(HUUUGGE_port)
);

endmodule