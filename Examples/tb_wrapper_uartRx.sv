`timescale 1ns/1ps

/*
* testbench for wrapper_uartRx
* 
* company:
* author/engineer:	Mr. TB
* creation date:	2020-05-27
* project name:
* tool versions:
*/

module tb_wrapper_uartRx;

	// dut inputs
	logic			clk;
	logic			rst_n;
	logic			uart_rxd;

	// dut outputs
	logic	[7:0]		symbol;
	logic			newSymbol;



	always begin
		 #5 		clk <= ~clk;
	end


	initial begin
		clk <= 1;


		$finish
	end


wrapper_uartRx mod_wrapper_uartRx (
	.clk			(clk),
	.rst_n			(rst_n),
	.uart_rxd_out		(uart_rxd),

	.symbol_o		(symbol),
	.newSymbol_o		(newSymbol)

);

endmodule