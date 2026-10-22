# best-sock-image

SystemVerilog image-processing IP scaffold with cocotb verification.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py images
python run.py all
```

## Commands

| Command | Description |
|---|---|
| `python run.py lint` | Verilator lint (`--lint-only -Wall`) per RTL file |
| `python run.py model` | Run Python model tests (`pytest tb/model`) |
| `python run.py test [--sim icarus|verilator] [--waves]` | Run smoke and configured unit tests |
| `python run.py unit <module>` | Run one cocotb unit test module |
| `python run.py demo --img <bmp> --preset <name>` | Produce RTL/golden demo output BMPs |
| `python run.py images` | Generate deterministic test BMPs |
| `python run.py all` | lint + model + test |

## Layout

- `rtl/` synthesizable SystemVerilog only
- `tb/lib` shared Python test utilities
- `tb/top` top-level cocotb tests
- `tb/unit` unit cocotb tests
- `tb/model` pytest model tests
- `tb/sva` assertions and coverage placeholders
- `tools/` utility scripts
- `images/` generated BMPs
- `docs/microarch/` block documentation templates

## Scaffold status

- RTL modules are stubs with TODO ownership tags.
- `reg_block` currently implements only registered ID/VERSION reads.
- `img_proc_top` uses a temporary AXI-stream bypass datapath.

## Owners table

- Combinational: Member 1 `kernel3x3`, Member 5 `color_stage/combine/isqrt/out_stage`, Member 4 verification
- Sequential: Member 3 `reg_block/frame_ctrl/axis_skid/top`, Member 2 `line_window`, Member 6 assertions/coverage

## Workflow

- Spec first.
- One issue/branch/PR at a time.
- Merge requires one approval + passing CI.
- `main` is protected.

## Coding rules

- lowRISC style (`always_ff`/`always_comb`, `_i/_o` ports, `clk_i`, `rst_ni`, `_q` regs, UpperCamelCase params, `_t` types, `_e` enums).
- Top-level AMBA naming is preserved (`aclk`, `aresetn`, `s_axis_*`, `m_axis_*`).
- Verilator lint must be clean for every RTL file.

## GitHub setup

- CI workflow installs Icarus Verilog 12 and Verilator 5.x, then runs lint/model/test.
- Verilator simulation under cocotb 2 requires Verilator **5.036+**.
