import pathlib
from tools.build_book import build_html


def test_build_html_embeds_figure_toc_and_math():
    figreg = {"sample": {"id":"sample","chapter":1,"number":"1.1","caption":"A sample",
              "kind":"original","source":"authored","file":"tests/fixtures/fig_sample.svg"}}
    html = build_html([pathlib.Path("tests/fixtures/ch_sample.md")], figreg)
    assert '<svg' in html                       # figure (and math) inlined
    assert 'Figure 1.1' in html                 # caption numbered
    assert 'id="ch01"' in html                  # chapter anchor
    assert 'href="#ch01"' in html               # TOC link resolves
    assert 'equals' not in html                 # math is SVG glyphs, NOT the spoken word
    assert 'Meanwhile, Worldwide' in html
    # self-contained: no external RESOURCE fetches (namespace xmlns http URIs are fine)
    assert 'src="http' not in html
    assert '<link ' not in html.lower()
    assert '@import' not in html


def test_txt_strips_markup_and_math():
    from tools.build_book import build_txt
    txt = build_txt([pathlib.Path("tests/fixtures/ch_sample.md")])
    assert "*" not in txt and "{{fig" not in txt
    assert "E equals I R" in txt
    assert "[Figure" in txt
