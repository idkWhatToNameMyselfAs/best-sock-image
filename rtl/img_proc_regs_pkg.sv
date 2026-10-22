package img_proc_regs_pkg;
  /* verilator lint_off UNUSEDPARAM */
  localparam logic [7:0] IdAddr          = 8'h00;
  localparam logic [7:0] VersionAddr     = 8'h04;
  localparam logic [7:0] CtrlAddr        = 8'h08;
  localparam logic [7:0] StatusAddr      = 8'h0C;
  localparam logic [7:0] IrqEnableAddr   = 8'h10;
  localparam logic [7:0] ColorAddr       = 8'h14;
  localparam logic [7:0] CombineAddr     = 8'h18;
  localparam logic [7:0] K1ShiftAddr     = 8'h1C;
  localparam logic [7:0] K1Row0Addr      = 8'h20;
  localparam logic [7:0] K1Row1Addr      = 8'h24;
  localparam logic [7:0] K1Row2Addr      = 8'h28;
  localparam logic [7:0] K2ShiftAddr     = 8'h2C;
  localparam logic [7:0] K2Row0Addr      = 8'h30;
  localparam logic [7:0] K2Row1Addr      = 8'h34;
  localparam logic [7:0] K2Row2Addr      = 8'h38;
  localparam logic [7:0] FrameCountAddr  = 8'h40;
  localparam logic [7:0] LatencyAddr     = 8'h44;
  localparam logic [7:0] FrameCyclesAddr = 8'h48;
  localparam logic [7:0] StallCyclesAddr = 8'h4C;
  localparam logic [7:0] ScratchAddr     = 8'h50;

  localparam logic [31:0] IdReset         = 32'h494D_4750;
  localparam logic [31:0] VersionReset    = 32'h0000_0100;
  localparam logic [31:0] CtrlReset       = 32'h0000_0000;
  localparam logic [31:0] StatusReset     = 32'h0000_0000;
  localparam logic [31:0] IrqEnableReset  = 32'h0000_0000;
  localparam logic [31:0] ColorReset      = 32'h0000_0000;
  localparam logic [31:0] CombineReset    = 32'h0000_0000;
  localparam logic [31:0] K1ShiftReset    = 32'h0000_0000;
  localparam logic [31:0] K1Row0Reset     = 32'h0000_0000;
  localparam logic [31:0] K1Row1Reset     = 32'h0000_0100;
  localparam logic [31:0] K1Row2Reset     = 32'h0000_0000;
  localparam logic [31:0] K2ShiftReset    = 32'h0000_0000;
  localparam logic [31:0] K2Row0Reset     = 32'h0000_0000;
  localparam logic [31:0] K2Row1Reset     = 32'h0000_0000;
  localparam logic [31:0] K2Row2Reset     = 32'h0000_0000;
  localparam logic [31:0] FrameCountReset = 32'h0000_0000;
  localparam logic [31:0] LatencyReset    = 32'h0000_0000;
  localparam logic [31:0] FrameCyclesReset= 32'h0000_0000;
  localparam logic [31:0] StallCyclesReset= 32'h0000_0000;
  localparam logic [31:0] ScratchReset    = 32'h0000_0000;

  typedef enum logic [1:0] {
    CombinePass   = 2'd0,
    CombineAbs    = 2'd1,
    CombineAbsSum = 2'd2,
    CombineSqrt   = 2'd3
  } combine_mode_e;

  typedef struct packed {
    logic [29:0] reserved;
    logic        soft_reset;
    logic        enable;
  } ctrl_reg_t;

  typedef struct packed {
    logic [24:0] reserved;
    logic [2:0]  state;
    logic        eol_err;
    logic        sof_err;
    logic        frame_done;
    logic        busy;
  } status_reg_t;

  typedef struct packed {
    logic [30:0] reserved;
    logic        gray;
  } color_reg_t;

  typedef struct packed {
    logic [26:0]     reserved_hi;
    logic            invert;
    logic [1:0]      reserved_lo;
    combine_mode_e   mode;
  } combine_reg_t;

  typedef struct packed {
    logic [10:0] reserved;
    logic [4:0]  c2;
    logic [2:0]  rsv1;
    logic [4:0]  c1;
    logic [2:0]  rsv0;
    logic [4:0]  c0;
  } kernel_row_reg_t;
  /* verilator lint_on UNUSEDPARAM */
endpackage
