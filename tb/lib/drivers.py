from __future__ import annotations

import random

import cocotb
from cocotb.triggers import RisingEdge, ReadOnly, ReadWrite, NextTimeStep


class AxisSource:
    def __init__(self, dut, clk, prefix: str = "s_axis", idle_prob: float = 0.0):
        self.dut = dut
        self.clk = clk
        self.prefix = prefix
        self.idle_prob = idle_prob

    def _sig(self, suffix: str):
        return getattr(self.dut, f"{self.prefix}_{suffix}")

    async def send(self, words):
        tdata = self._sig("tdata")
        tuser = self._sig("tuser")
        tlast = self._sig("tlast")
        tvalid = self._sig("tvalid")
        tready = self._sig("tready")

        for data, user, last in words:
            await ReadWrite()
            while self.idle_prob > 0 and random.random() < self.idle_prob:
                tvalid.value = 0
                await RisingEdge(self.clk)
            tdata.value = int(data)
            tuser.value = int(user)
            tlast.value = int(last)
            tvalid.value = 1
            while True:
                await RisingEdge(self.clk)
                if int(tready.value):
                    break
        tvalid.value = 0


class AxisSink:
    def __init__(self, dut, clk, prefix: str = "m_axis", ready_prob: float = 1.0, seed: int = 1):
        self.dut = dut
        self.clk = clk
        self.prefix = prefix
        self.ready_prob = ready_prob
        self.rng = random.Random(seed)
        self.words = []
        self._task = None

    def _sig(self, suffix: str):
        return getattr(self.dut, f"{self.prefix}_{suffix}")

    async def _run(self):
        tdata = self._sig("tdata")
        tuser = self._sig("tuser")
        tlast = self._sig("tlast")
        tvalid = self._sig("tvalid")
        tready = self._sig("tready")
        prev_payload = None
        while True:
            await RisingEdge(self.clk)
            tready.value = 1 if self.rng.random() < self.ready_prob else 0
            await ReadOnly()
            v = int(tvalid.value)
            r = int(tready.value)
            payload = (int(tdata.value), int(tuser.value), int(tlast.value))
            if v and not r:
                if prev_payload is not None and payload != prev_payload:
                    raise AssertionError("Payload changed while stalled")
                prev_payload = payload
            else:
                prev_payload = None
            if v and r:
                self.words.append(payload)

    def start(self):
        if self._task is None:
            self._task = cocotb.start_soon(self._run())

    async def wait_for(self, count: int, timeout_cycles: int = 200000):
        for _ in range(timeout_cycles):
            if len(self.words) >= count:
                return self.words[:count]
            await RisingEdge(self.clk)
        raise TimeoutError(f"Timeout waiting for {count} words")


class RegBus:
    def __init__(self, dut, clk):
        self.dut = dut
        self.clk = clk

    async def write(self, addr: int, data: int):
        await ReadWrite()
        self.dut.reg_addr.value = addr & 0xFF
        self.dut.reg_wdata.value = data & 0xFFFFFFFF
        self.dut.reg_we.value = 1
        self.dut.reg_re.value = 0
        await RisingEdge(self.clk)
        self.dut.reg_we.value = 0
        await RisingEdge(self.clk)
        return int(self.dut.reg_err.value)

    async def read(self, addr: int):
        await ReadWrite()
        self.dut.reg_addr.value = addr & 0xFF
        self.dut.reg_we.value = 0
        self.dut.reg_re.value = 1
        await RisingEdge(self.clk)
        self.dut.reg_re.value = 0
        await RisingEdge(self.clk)
        await ReadOnly()
        data = int(self.dut.reg_rdata.value)
        err = int(self.dut.reg_err.value)
        await NextTimeStep()
        return data, err
