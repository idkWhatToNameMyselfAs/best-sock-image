package img_proc_pkg;
  import img_proc_regs_pkg::*;
  /* verilator lint_off UNUSEDPARAM */
  localparam int unsigned ImgWidth  = 256;
  localparam int unsigned ImgHeight = 256;
  localparam int unsigned PixW      = 24;
  localparam int unsigned CoefW     = 5;
  localparam int unsigned ShiftW    = 3;
  localparam int unsigned SumW      = 17;

  typedef struct packed {
    logic [7:0] r;
    logic [7:0] g;
    logic [7:0] b;
  } rgb_t;

  typedef rgb_t window_t [2:0][2:0];
  typedef logic signed [CoefW-1:0] coef_t;
  typedef logic signed [2:0][2:0][CoefW-1:0] kernel_t;
  typedef logic signed [SumW-1:0] sum_t;
  typedef logic signed [2:0][SumW-1:0] sum3_t;

  typedef struct packed {
    logic          gray;
    kernel_t       k1;
    logic [2:0]    k1_shift;
    kernel_t       k2;
    logic [2:0]    k2_shift;
    combine_mode_e mode;
    logic          invert;
  } cfg_t;

  typedef enum logic [1:0] {
    FrameIdle    = 2'd0,
    FrameReceive = 2'd1,
    FrameDrain   = 2'd2,
    FrameDone    = 2'd3
  } frame_state_e;
  /* verilator lint_on UNUSEDPARAM */
endpackage
