module axis_skid #(
  parameter int unsigned Width = 26
) (
  input  logic             clk_i,
  input  logic             rst_ni,
  input  logic [Width-1:0] s_data_i,
  input  logic             s_valid_i,
  output logic             s_ready_o,
  output logic [Width-1:0] m_data_o,
  output logic             m_valid_o,
  input  logic             m_ready_i
);
  /* verilator lint_off UNUSEDSIGNAL */
  /* verilator lint_off UNUSEDPARAM */
  // TODO(Member 3): Implement AXI-stream skid buffer.
  assign s_ready_o = 1'b0;
  assign m_data_o  = '0;
  assign m_valid_o = 1'b0;
  logic unused;
  assign unused = &{1'b0, clk_i, rst_ni, s_data_i, s_valid_i, m_ready_i};
  /* verilator lint_on UNUSEDPARAM */
  /* verilator lint_on UNUSEDSIGNAL */
endmodule
