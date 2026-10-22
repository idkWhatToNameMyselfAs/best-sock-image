module img_proc_top (
  input  logic        aclk,
  input  logic        aresetn,
  input  logic [23:0] s_axis_tdata,
  input  logic        s_axis_tuser,
  input  logic        s_axis_tlast,
  input  logic        s_axis_tvalid,
  output logic        s_axis_tready,
  output logic [23:0] m_axis_tdata,
  output logic        m_axis_tuser,
  output logic        m_axis_tlast,
  output logic        m_axis_tvalid,
  input  logic        m_axis_tready,
  input  logic [7:0]  reg_addr,
  input  logic [31:0] reg_wdata,
  input  logic        reg_we,
  input  logic        reg_re,
  output logic [31:0] reg_rdata,
  output logic        reg_err,
  output logic        irq_o
);
  import img_proc_pkg::*;

  cfg_t cfg;
  logic enable;
  logic soft_reset;
  logic in_allow;
  logic cfg_load;
  frame_state_e state;
  logic busy;
  logic frame_done;
  logic sof_err;
  logic eol_err;
  logic [31:0] frame_count;
  logic [31:0] latency;
  logic [31:0] frame_cycles;
  logic [31:0] stall_cycles;

  reg_block u_reg_block (
    .clk_i(aclk),
    .rst_ni(aresetn),
    .reg_addr_i(reg_addr),
    .reg_wdata_i(reg_wdata),
    .reg_we_i(reg_we),
    .reg_re_i(reg_re),
    .reg_rdata_o(reg_rdata),
    .reg_err_o(reg_err),
    .cfg_load_i(cfg_load),
    .cfg_o(cfg),
    .enable_o(enable),
    .soft_reset_o(soft_reset),
    .state_i(state),
    .busy_i(busy),
    .frame_done_i(frame_done),
    .sof_err_i(sof_err),
    .eol_err_i(eol_err),
    .frame_count_i(frame_count),
    .latency_i(latency),
    .frame_cycles_i(frame_cycles),
    .stall_cycles_i(stall_cycles),
    .irq_o(irq_o)
  );

  frame_ctrl u_frame_ctrl (
    .clk_i(aclk),
    .rst_ni(aresetn),
    .enable_i(enable),
    .soft_reset_i(soft_reset),
    .in_fire_i(s_axis_tvalid & s_axis_tready),
    .in_sof_i(s_axis_tuser),
    .in_eol_i(s_axis_tlast),
    .out_fire_i(m_axis_tvalid & m_axis_tready),
    .out_stall_i(m_axis_tvalid & ~m_axis_tready),
    .in_allow_o(in_allow),
    .cfg_load_o(cfg_load),
    .state_o(state),
    .busy_o(busy),
    .frame_done_o(frame_done),
    .sof_err_o(sof_err),
    .eol_err_o(eol_err),
    .frame_count_o(frame_count),
    .latency_o(latency),
    .frame_cycles_o(frame_cycles),
    .stall_cycles_o(stall_cycles)
  );

  // Temporary pixel bypass. Intended chain:
  // axis_skid -> color_stage -> line_window -> kernel3x3 x2 -> combine -> out_stage -> axis_skid
  assign m_axis_tdata  = s_axis_tdata;
  assign m_axis_tuser  = s_axis_tuser;
  assign m_axis_tlast  = s_axis_tlast;
  assign m_axis_tvalid = s_axis_tvalid;
  assign s_axis_tready = m_axis_tready;

  logic unused;
  assign unused = &{1'b0, in_allow, cfg};
endmodule
