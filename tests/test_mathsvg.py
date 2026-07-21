from tools.mathsvg import render

def test_render_returns_inline_svg():
    svg = render("E = IR")
    assert svg.strip().startswith("<svg") and "</svg>" in svg

def test_render_is_self_contained():
    svg = render("c = f\\lambda")
    # namespace decls (xmlns="http://www.w3.org/2000/svg") are fine; external RESOURCE refs are not:
    assert "<image" not in svg
    assert 'xlink:href="http' not in svg and 'href="http' not in svg.replace('xmlns', '')
    assert "@import" not in svg

def test_render_handles_subscripts_and_abs():
    svg = render("f_{IF} = |f_{RF} - f_{LO}|")
    assert svg.strip().startswith("<svg")
