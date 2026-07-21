import json, pathlib
from tools.figreg import load, validate

def test_validate_flags_protected_source(tmp_path):
    reg = {"x": {"id":"x","chapter":6,"number":"6.1","caption":"c",
                 "kind":"archival-PD","source":"1974 Handbook","file":"figures/archival/x.png"}}
    errs = validate(reg)
    assert any("1974" in e or "protected" in e.lower() for e in errs)

def test_validate_accepts_original(tmp_path):
    reg = {"x": {"id":"x","chapter":1,"number":"1.1","caption":"c",
                 "kind":"original","source":"authored","file":"figures/x.svg"}}
    assert validate(reg) == []
