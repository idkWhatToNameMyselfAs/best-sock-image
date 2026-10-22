from pathlib import Path
import os

import numpy as np
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

from tb.lib import bmp, golden, presets, regmap
from tb.lib.drivers import AxisSink, AxisSource, RegBus


async def _reset(dut):
    dut.aresetn.value = 0
    dut.s_axis_tvalid.value = 0
    dut.reg_we.value = 0
    dut.reg_re.value = 0
    dut.m_axis_tready.value = 0
    for _ in range(5):
        await RisingEdge(dut.aclk)
    dut.aresetn.value = 1
    for _ in range(2):
        await RisingEdge(dut.aclk)


@cocotb.test(timeout_time=3000, timeout_unit="ms")
async def test_demo_image(dut):
    cocotb.start_soon(Clock(dut.aclk, 10, unit="ns").start())
    await _reset(dut)

    demo_img = os.environ["DEMO_IMG"]
    demo_preset = os.environ["DEMO_PRESET"]
    demo_out = Path(os.environ["DEMO_OUT"])
    demo_out.mkdir(parents=True, exist_ok=True)

    preset_fn = presets.PRESETS[demo_preset]
    regs = preset_fn()

    bus = RegBus(dut, dut.aclk)
    for name, value in regs.items():
        await bus.write(regmap.ADDR[name], value)
    await bus.write(regmap.ADDR["CTRL"], 1)

    img = bmp.read_bmp(demo_img)
    cfg = golden.cfg_from_regs(regs)
    gld = golden.run(img, cfg)

    src = AxisSource(dut, dut.aclk, "s_axis")
    sink = AxisSink(dut, dut.aclk, "m_axis", ready_prob=1.0, seed=11)
    sink.start()

    words = list(bmp.to_stream(img))
    await src.send(words)
    got_words = await sink.wait_for(len(words), timeout_cycles=1400000)
    rtl = bmp.from_stream(got_words)

    stem = Path(demo_img).stem
    rtl_path = demo_out / f"{stem}_{demo_preset}_rtl.bmp"
    gld_path = demo_out / f"{stem}_{demo_preset}_golden.bmp"
    side_path = demo_out / f"{stem}_{demo_preset}_side_by_side.bmp"

    bmp.write_bmp(rtl_path, rtl)
    bmp.write_bmp(gld_path, gld)
    side = np.concatenate([rtl, gld], axis=1)
    side_small = np.zeros((256, 256, 3), dtype=np.uint8)
    side_small[:, :128] = side[:, :128]
    side_small[:, 128:] = side[:, 256:384]
    bmp.write_bmp(side_path, side_small)

    assert np.count_nonzero(rtl != gld) == 0
