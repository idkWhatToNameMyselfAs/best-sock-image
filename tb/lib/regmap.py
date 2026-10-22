import re
from pathlib import Path

_LOCALPARAM_RE = re.compile(
    r"localparam\s+logic\s*\[[^\]]+\]\s+([A-Za-z0-9_]+)\s*=\s*([^;]+);"
)


def _camel_to_upper_snake(name: str) -> str:
    out = []
    for i, ch in enumerate(name):
        if i and ch.isupper() and (name[i - 1].islower() or (i + 1 < len(name) and name[i + 1].islower())):
            out.append("_")
        out.append(ch.upper())
    return "".join(out)


def _parse_sv_int(text: str) -> int:
    raw = text.replace("_", "").strip()
    m = re.fullmatch(r"(\d+)'([hdb])([0-9a-fA-FxXzZ]+)", raw)
    if m:
        _, base_ch, digits = m.groups()
        if any(c in "xXzZ" for c in digits):
            return 0
        base = {"h": 16, "d": 10, "b": 2}[base_ch.lower()]
        return int(digits, base)
    return int(raw, 0)


def parse_reg_pkg(path: str | Path):
    text = Path(path).read_text(encoding="utf-8")
    addr = {}
    reset = {}
    for name, value in _LOCALPARAM_RE.findall(text):
        if name.endswith("Addr"):
            key = _camel_to_upper_snake(name[:-4])
            addr[key] = _parse_sv_int(value)
        elif name.endswith("Reset"):
            key = _camel_to_upper_snake(name[:-5])
            reset[key] = _parse_sv_int(value)
    for key in addr:
        reset.setdefault(key, 0)
    return addr, reset


_REPO_ROOT = Path(__file__).resolve().parents[2]
_REGS_PKG = _REPO_ROOT / "rtl" / "img_proc_regs_pkg.sv"
ADDR, RESET = parse_reg_pkg(_REGS_PKG)
