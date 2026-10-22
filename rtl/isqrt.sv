module isqrt (
  input  logic        clk_i,
  input  logic        rst_ni,
  input  logic        valid_i,
  input  logic [31:0] rad_i,
  output logic        valid_o,
  output logic [15:0] root_o
);
  /* verilator lint_off UNUSEDSIGNAL */
  /* verilator lint_off UNUSEDPARAM */
  // TODO(Member 5): Implement integer square-root.
  assign valid_o = 1'b0;
  assign root_o  = '0;
  logic unused;
  assign unused = &{1'b0, clk_i, rst_ni, valid_i, rad_i};
  /* verilator lint_on UNUSEDPARAM */
  /* verilator lint_on UNUSEDSIGNAL */
endmodule
