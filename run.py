#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from cocotb_tools import check_results
from cocotb_tools.runner import get_runner

REPO = Path(__file__).resolve().parent
RTL_F = REPO / "rtl" / "rtl.f"
UNIT_TESTS: list[str] = []


def _read_sources():
    return [str(REPO / line.strip()) for line in RTL_F.read_text(encoding="utf-8").splitlines() if line.strip()]


def run_lint() -> bool:
    tops = [
        "img_proc_top",
        "axis_skid",
        "color_stage",
        "line_window",
        "kernel3x3",
        "isqrt",
        "combine",
        "out_stage",
        "frame_ctrl",
        "reg_block",
    ]
    ok = True
    for top in tops:
        cmd = ["verilator", "--lint-only", "-Wall", "-f", str(RTL_F), "--top-module", top]
        proc = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
        passed = proc.returncode == 0
        print(f"{top}: {'PASS' if passed else 'FAIL'}")
        if not passed:
            ok = False
            if proc.stdout:
                print(proc.stdout)
            if proc.stderr:
                print(proc.stderr)
    return ok


def run_model() -> bool:
    cmd = [sys.executable, "-m", "pytest", "tb/model", "-q"]
    proc = subprocess.run(cmd, cwd=REPO)
    return proc.returncode == 0


def _run_cocotb(top: str, test_module: str, sim: str, waves: bool, extra_env: dict[str, str] | None = None) -> bool:
    runner = get_runner(sim)
    build_dir = REPO / "sim_build" / sim / top
    env = {"PYTHONPATH": str(REPO)}
    if extra_env:
        env.update(extra_env)
    build_args = []
    if sim == "verilator" and waves:
        build_args.append("--trace")
    runner.build(
        verilog_sources=_read_sources(),
        hdl_toplevel=top,
        build_dir=str(build_dir),
        always=True,
        build_args=build_args,
        timescale=("1ns", "1ps"),
    )
    runner.test(
        hdl_toplevel=top,
        test_module=test_module,
        results_xml="results.xml",
        build_dir=str(build_dir),
        waves=waves,
        extra_env=env,
    )
    res = check_results.get_results(build_dir / "results.xml")
    return res[1] == 0


def run_test(sim: str, waves: bool) -> bool:
    ok = _run_cocotb("img_proc_top", "tb.top.test_smoke", sim, waves)
    for module in UNIT_TESTS:
        ok = _run_cocotb(module, f"tb.unit.test_{module}", sim, waves) and ok
    return ok


def run_unit(sim: str, waves: bool, module: str) -> bool:
    return _run_cocotb(module, f"tb.unit.test_{module}", sim, waves)


def run_demo(sim: str, waves: bool, img: str, preset: str) -> bool:
    out_dir = REPO / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    extra_env = {
        "DEMO_IMG": str(Path(img).resolve()),
        "DEMO_PRESET": preset,
        "DEMO_OUT": str(out_dir.resolve()),
    }
    return _run_cocotb("img_proc_top", "tb.top.test_demo", sim, waves, extra_env=extra_env)


def run_images() -> bool:
    cmd = [sys.executable, str(REPO / "tools" / "make_test_images.py")]
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO)
    proc = subprocess.run(cmd, cwd=REPO, env=env)
    return proc.returncode == 0


def _finish(ok: bool):
    print(f"RESULT: {'PASS' if ok else 'FAIL'}")
    raise SystemExit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("lint")
    sub.add_parser("model")
    t = sub.add_parser("test")
    t.add_argument("--sim", choices=["icarus", "verilator"], default="icarus")
    t.add_argument("--waves", action="store_true")
    u = sub.add_parser("unit")
    u.add_argument("module")
    u.add_argument("--sim", choices=["icarus", "verilator"], default="icarus")
    u.add_argument("--waves", action="store_true")
    d = sub.add_parser("demo")
    d.add_argument("--img", required=True)
    d.add_argument("--preset", required=True)
    d.add_argument("--sim", choices=["icarus", "verilator"], default="icarus")
    d.add_argument("--waves", action="store_true")
    sub.add_parser("images")
    a = sub.add_parser("all")
    a.add_argument("--sim", choices=["icarus", "verilator"], default="icarus")
    a.add_argument("--waves", action="store_true")

    args = ap.parse_args()

    if args.cmd == "lint":
        _finish(run_lint())
    if args.cmd == "model":
        _finish(run_model())
    if args.cmd == "test":
        _finish(run_test(args.sim, args.waves))
    if args.cmd == "unit":
        _finish(run_unit(args.sim, args.waves, args.module))
    if args.cmd == "demo":
        _finish(run_demo(args.sim, args.waves, args.img, args.preset))
    if args.cmd == "images":
        _finish(run_images())
    if args.cmd == "all":
        ok = run_lint()
        ok = run_model() and ok
        ok = run_test(args.sim, args.waves) and ok
        _finish(ok)


if __name__ == "__main__":
    main()
