module combine (
  input  logic                 clk_i,
  input  logic                 rst_ni,
  input  logic                 en_i,
  input  logic                 valid_i,
  input  logic                 sof_i,
  input  logic                 eol_i,
  input  img_proc_pkg::sum3_t  a_i,
  input  img_proc_pkg::sum3_t  b_i,
  input  img_proc_regs_pkg::combine_mode_e mode_i,
  output logic                 valid_o,
  output logic                 sof_o,
  output logic                 eol_o,
  output img_proc_pkg::rgb_t   rgb_o
);
  /* verilator lint_off UNUSEDSIGNAL */
  /* verilator lint_off UNUSEDPARAM */
  // TODO(Member 5): Implement combine stage.
  assign valid_o = 1'b0;
  assign sof_o   = 1'b0;
  assign eol_o   = 1'b0;
  assign rgb_o   = '0;
  logic unused;
  assign unused = &{1'b0, clk_i, rst_ni, en_i, valid_i, sof_i, eol_i, a_i, b_i, mode_i};
  /* verilator lint_on UNUSEDPARAM */
  /* verilator lint_on UNUSEDSIGNAL */
endmodule
