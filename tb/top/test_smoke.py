import numpy as np
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

from tb.lib import bmp, golden, regmap
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


@cocotb.test(timeout_time=100, timeout_unit="ms")
async def test_id_and_version_reads(dut):
    cocotb.start_soon(Clock(dut.aclk, 10, unit="ns").start())
    await _reset(dut)
    bus = RegBus(dut, dut.aclk)
    rid, err0 = await bus.read(regmap.ADDR["ID"])
    ver, err1 = await bus.read(regmap.ADDR["VERSION"])
    assert err0 == 0 and err1 == 0
    assert rid == 0x494D4750
    assert ver == 0x00000100


@cocotb.test(timeout_time=2000, timeout_unit="ms")
async def test_passthrough_frame(dut):
    cocotb.start_soon(Clock(dut.aclk, 10, unit="ns").start())
    await _reset(dut)
    bus = RegBus(dut, dut.aclk)
    assert await bus.write(regmap.ADDR["CTRL"], 1) == 0

    rng = np.random.default_rng(2026)
    img = rng.integers(0, 256, size=(256, 256, 3), dtype=np.uint8)
    exp = golden.run(img, golden.cfg_from_regs({}))

    src = AxisSource(dut, dut.aclk, "s_axis")
    sink = AxisSink(dut, dut.aclk, "m_axis", ready_prob=0.7, seed=7)
    sink.start()

    words = list(bmp.to_stream(img))
    await src.send(words)
    got_words = await sink.wait_for(len(words), timeout_cycles=1200000)

    got_img = bmp.from_stream(got_words)
    assert np.array_equal(got_img, exp)
    for i, (_d, tuser, tlast) in enumerate(got_words):
        assert tuser == int(i == 0)
        assert tlast == int((i + 1) % 256 == 0)
