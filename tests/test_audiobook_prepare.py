from tools.make_audiobook import spoken_heading, prepare_text

def test_spoken_heading_era_chapter():
    assert spoken_heading("1. The Spark Era (1900–1917)") == \
        "Chapter One. The Spark Era. 1900 to 1917."

def test_spoken_heading_prologue():
    assert spoken_heading("Prologue — Before the Amateurs (1864–1900)") == \
        "Prologue. Before the Amateurs. 1864 to 1900."

def test_prepare_text_speaks_math_and_drops_fig_markup():
    out = prepare_text("The tank obeys $E = IR$ here.\n\n{{fig:x}}\n", {"x": ("1", "a tank")})
    assert "E equals I R" in out
    assert "{{fig" not in out
    assert "Figure 1" in out
