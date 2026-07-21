from tools.narration import strip_markup, speak_math, speak_figures

def test_strip_markup_removes_emphasis_and_refs():
    assert strip_markup("*hi* and **bold** {{fig:x}}") == "hi and bold"

def test_speak_math_ohms_law():
    assert speak_math("by $E = IR$ here") == "by E equals I R here"

def test_speak_math_symbols():
    assert speak_math("$c = f\\lambda$") == "c equals f lambda"
    assert speak_math("$\\Delta f \\approx f v / c$") == "delta f approximately f v over c"

def test_speak_figures_inserts_description():
    out = speak_figures("see {{fig:tank}} now", {"tank": ("4", "a spark-gap tank circuit")})
    assert out == "see (Figure 4. a spark-gap tank circuit.) now"
