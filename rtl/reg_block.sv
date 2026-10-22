module reg_block (
  input  logic                clk_i,
  input  logic                rst_ni,
  input  logic [7:0]          reg_addr_i,
  input  logic [31:0]         reg_wdata_i,
  input  logic                reg_we_i,
  input  logic                reg_re_i,
  output logic [31:0]         reg_rdata_o,
  output logic                reg_err_o,
  input  logic                cfg_load_i,
  output img_proc_pkg::cfg_t  cfg_o,
  output logic                enable_o,
  output logic                soft_reset_o,
  input  img_proc_pkg::frame_state_e state_i,
  input  logic                busy_i,
  input  logic                frame_done_i,
  input  logic                sof_err_i,
  input  logic                eol_err_i,
  input  logic [31:0]         frame_count_i,
  input  logic [31:0]         latency_i,
  input  logic [31:0]         frame_cycles_i,
  input  logic [31:0]         stall_cycles_i,
  output logic                irq_o
);
  import img_proc_regs_pkg::*;
  /* verilator lint_off UNUSEDSIGNAL */
  /* verilator lint_off UNUSEDPARAM */
  // TODO(Member 3): Complete register block implementation.
  logic [7:0] addr_q;
  logic       re_q;

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      addr_q      <= '0;
      re_q        <= 1'b0;
      reg_rdata_o <= '0;
      reg_err_o   <= 1'b0;
    end else begin
      addr_q <= reg_addr_i;
      re_q   <= reg_re_i;
      if (re_q) begin
        unique case (addr_q)
          IdAddr: begin
            reg_rdata_o <= IdReset;
            reg_err_o   <= 1'b0;
          end
          VersionAddr: begin
            reg_rdata_o <= VersionReset;
            reg_err_o   <= 1'b0;
          end
          default: begin
            reg_rdata_o <= '0;
            reg_err_o   <= 1'b1;
          end
        endcase
      end else begin
        reg_rdata_o <= '0;
        reg_err_o   <= 1'b0;
      end
    end
  end

  assign cfg_o        = '0;
  assign enable_o     = 1'b0;
  assign soft_reset_o = 1'b0;
  assign irq_o        = 1'b0;

  logic unused;
  assign unused = &{1'b0, reg_wdata_i, reg_we_i, cfg_load_i, state_i, busy_i, frame_done_i, sof_err_i,
                    eol_err_i, frame_count_i, latency_i, frame_cycles_i, stall_cycles_i};
  /* verilator lint_on UNUSEDPARAM */
  /* verilator lint_on UNUSEDSIGNAL */
endmodule
