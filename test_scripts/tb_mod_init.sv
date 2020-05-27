`timescale 1ns/1ps

/*
* testbench for mod_init
* 
* company:
* author/engineer:	Marwin Kirchhofs
* creation date:	2020-05-22
* project name:
* tool versions:
*/

module tb_mod_init;

	// dut inputs:
	logic	[7:0]			port1
	logic					clk

	// dut output:
	logic	[MSG_BITS-1:0]	port2

	// dut inout:
	wire	[3:0]			port3


	always begin
		 #5 		clk <= ~clk;
	end


	initial begin
		clk <= 1;


		$finish
	end


mod_init #(
	.param1					(),
	.param2					(DEF2)
) mod_mod_init (
	.port1					(port1),
	.clk_i					(clk),

	.port2					(port2),

	.port3					(port3)
);

endmodule