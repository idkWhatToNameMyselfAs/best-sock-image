module kernel3x3 (
  input  logic                 clk_i,
  input  logic                 rst_ni,
  input  logic                 en_i,
  input  logic                 valid_i,
  input  logic                 sof_i,
  input  logic                 eol_i,
  input  img_proc_pkg::window_t window_i,
  input  img_proc_pkg::kernel_t kernel_i,
  input  logic [2:0]           shift_i,
  output logic                 valid_o,
  output logic                 sof_o,
  output logic                 eol_o,
  output img_proc_pkg::sum3_t  sum_o
);
  /* verilator lint_off UNUSEDSIGNAL */
  /* verilator lint_off UNUSEDPARAM */
  // TODO(Member 1): Implement 3x3 kernel stage.
  assign valid_o = 1'b0;
  assign sof_o   = 1'b0;
  assign eol_o   = 1'b0;
  assign sum_o[0] = '0;
  assign sum_o[1] = '0;
  assign sum_o[2] = '0;
  logic unused;
  assign unused = &{1'b0, clk_i, rst_ni, en_i, valid_i, sof_i, eol_i, window_i, kernel_i, shift_i};
  /* verilator lint_on UNUSEDPARAM */
  /* verilator lint_on UNUSEDSIGNAL */
endmodule
