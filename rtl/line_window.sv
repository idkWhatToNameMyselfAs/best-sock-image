/* verilator lint_off UNUSEDPARAM */
module line_window #(
  parameter int unsigned DataW  = 24,
  parameter int unsigned Width  = img_proc_pkg::ImgWidth,
  parameter int unsigned Height = img_proc_pkg::ImgHeight
) (
  input  logic                           clk_i,
  input  logic                           rst_ni,
  input  logic                           en_i,
  input  logic                           valid_i,
  input  logic                           sof_i,
  input  logic                           eol_i,
  input  logic [DataW-1:0]               data_i,
  output logic                           valid_o,
  output logic                           sof_o,
  output logic                           eol_o,
  output logic [2:0][2:0][DataW-1:0]     window_o,
  output logic                           draining_o
);
  /* verilator lint_off UNUSEDSIGNAL */
  /* verilator lint_off UNUSEDPARAM */
  // TODO(Member 2): Implement line window buffering.
  assign valid_o    = 1'b0;
  assign sof_o      = 1'b0;
  assign eol_o      = 1'b0;
  assign window_o   = '0;
  assign draining_o = 1'b0;
  logic unused;
  assign unused = &{1'b0, clk_i, rst_ni, en_i, valid_i, sof_i, eol_i, data_i};
  /* verilator lint_on UNUSEDPARAM */
  /* verilator lint_on UNUSEDSIGNAL */
endmodule
/* verilator lint_on UNUSEDPARAM */
