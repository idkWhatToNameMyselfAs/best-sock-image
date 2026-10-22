module color_stage (
  input  logic               clk_i,
  input  logic               rst_ni,
  input  logic               en_i,
  input  logic               valid_i,
  input  logic               sof_i,
  input  logic               eol_i,
  input  logic               gray_i,
  input  img_proc_pkg::rgb_t rgb_i,
  output logic               valid_o,
  output logic               sof_o,
  output logic               eol_o,
  output img_proc_pkg::rgb_t rgb_o
);
  /* verilator lint_off UNUSEDSIGNAL */
  /* verilator lint_off UNUSEDPARAM */
  // TODO(Member 5): Implement color stage.
  assign valid_o = 1'b0;
  assign sof_o   = 1'b0;
  assign eol_o   = 1'b0;
  assign rgb_o   = '0;
  logic unused;
  assign unused = &{1'b0, clk_i, rst_ni, en_i, valid_i, sof_i, eol_i, gray_i, rgb_i};
  /* verilator lint_on UNUSEDPARAM */
  /* verilator lint_on UNUSEDSIGNAL */
endmodule
