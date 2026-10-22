import random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ReadOnly


async def _drive(dut, words):
    dut.s_valid_i.value = 0
    idx = 0
    while idx < len(words):
        await RisingEdge(dut.clk_i)
        if int(dut.s_ready_o.value):
            dut.s_data_i.value = words[idx]
            dut.s_valid_i.value = 1
            idx += 1
        else:
            dut.s_valid_i.value = 1
    await RisingEdge(dut.clk_i)
    dut.s_valid_i.value = 0


async def _sink(dut, ready_prob, expected, max_cycles=30000):
    rng = random.Random(123)
    out = []
    stalled_payload = None
    cycles = 0
    while len(out) < len(expected):
        cycles += 1
        if cycles > max_cycles:
            raise AssertionError("Timed out before receiving expected beats")
        await RisingEdge(dut.clk_i)
        dut.m_ready_i.value = 1 if rng.random() < ready_prob else 0
        await ReadOnly()
        v = int(dut.m_valid_o.value)
        r = int(dut.m_ready_i.value)
        payload = int(dut.m_data_o.value)
        if v and not r:
            if stalled_payload is not None:
                assert payload == stalled_payload
            stalled_payload = payload
        else:
            stalled_payload = None
        if v and r:
            out.append(payload)
    return out


async def _run_case(dut, ready_prob):
    words = [random.getrandbits(26) for _ in range(2000)]
    cocotb.start_soon(_drive(dut, words))
    out = await _sink(dut, ready_prob, words)
    assert out == words


@cocotb.test(timeout_time=200, timeout_unit="ms")
async def test_full_throughput(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    dut.rst_ni.value = 0
    dut.s_data_i.value = 0
    dut.s_valid_i.value = 0
    dut.m_ready_i.value = 0
    for _ in range(5):
        await RisingEdge(dut.clk_i)
    dut.rst_ni.value = 1
    await _run_case(dut, ready_prob=1.0)


@cocotb.test(timeout_time=300, timeout_unit="ms")
async def test_random_backpressure(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    dut.rst_ni.value = 0
    dut.s_data_i.value = 0
    dut.s_valid_i.value = 0
    dut.m_ready_i.value = 0
    for _ in range(5):
        await RisingEdge(dut.clk_i)
    dut.rst_ni.value = 1
    await _run_case(dut, ready_prob=0.5)
