from tools.audit_book import check_banned_phrases, check_figure_integrity

def test_banned_phrases_flagged():
    errs = check_banned_phrases("…and little did they know it would grow.")
    assert errs and "little did they know" in errs[0]

def test_banned_phrases_clean():
    assert check_banned_phrases("The lamp is lit and the era closed on a question.") == []

def test_figure_integrity_missing():
    errs = check_figure_integrity(["{{fig:ghost}}"], registry={})
    assert any("ghost" in e for e in errs)

def test_figure_integrity_ok():
    reg = {"tank": {"id":"tank","chapter":1,"number":"1.1","caption":"c","kind":"original","source":"authored","file":"figures/tank.svg"}}
    assert check_figure_integrity(["see {{fig:tank}}"], registry=reg) == []
