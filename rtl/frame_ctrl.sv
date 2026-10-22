module frame_ctrl (
  input  logic                   clk_i,
  input  logic                   rst_ni,
  input  logic                   enable_i,
  input  logic                   soft_reset_i,
  input  logic                   in_fire_i,
  input  logic                   in_sof_i,
  input  logic                   in_eol_i,
  input  logic                   out_fire_i,
  input  logic                   out_stall_i,
  output logic                   in_allow_o,
  output logic                   cfg_load_o,
  output img_proc_pkg::frame_state_e state_o,
  output logic                   busy_o,
  output logic                   frame_done_o,
  output logic                   sof_err_o,
  output logic                   eol_err_o,
  output logic [31:0]            frame_count_o,
  output logic [31:0]            latency_o,
  output logic [31:0]            frame_cycles_o,
  output logic [31:0]            stall_cycles_o
);
  /* verilator lint_off UNUSEDSIGNAL */
  /* verilator lint_off UNUSEDPARAM */
  // TODO(Member 3): Implement frame controller.
  assign in_allow_o     = 1'b0;
  assign cfg_load_o     = 1'b0;
  assign state_o        = img_proc_pkg::FrameIdle;
  assign busy_o         = 1'b0;
  assign frame_done_o   = 1'b0;
  assign sof_err_o      = 1'b0;
  assign eol_err_o      = 1'b0;
  assign frame_count_o  = '0;
  assign latency_o      = '0;
  assign frame_cycles_o = '0;
  assign stall_cycles_o = '0;
  logic unused;
  assign unused = &{1'b0, clk_i, rst_ni, enable_i, soft_reset_i, in_fire_i, in_sof_i, in_eol_i,
                    out_fire_i, out_stall_i};
  /* verilator lint_on UNUSEDPARAM */
  /* verilator lint_on UNUSEDSIGNAL */
endmodule
