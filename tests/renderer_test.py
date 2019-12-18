from pytest import raises

from plp import Renderer, UnclosedTag

broken_code_1 = """<html>
    <head>
        <?python # Incomplete code.
    </head>
</html>
"""

broken_code_2 = """
<html<<?python # Error >"""

working_code_1 = '<?pythonprint(4+2)?>'

working_code_2 = """<html>
    <head>
        <title><?pythonprint("Title")?></title>
    </head>
</html>
"""


def test_init(r):
    assert isinstance(r, Renderer)
    assert r.start == '<?python'
    assert r.end == '?>'
    assert r.filename == '<PLP Renderer>'


def test_broken_code_1(r):
    with raises(UnclosedTag) as exc:
        r.render(broken_code_1)
    assert exc.value.args == (
        'The tag opened on line 3 column 9 is unclosed.',
    )


def test_broken_code_2(r):
    with raises(UnclosedTag) as exc:
        r.render(broken_code_2)
    assert exc.value.args == (
        'The tag opened on line 2 column 7 is unclosed.',
    )


def test_working_code_1(r):
    assert r.render(working_code_1) == '6'


def test_working_code_2(r):
    expected = '<html>\n    <head>\n        <title>Title</title>\n    '
    expected += '</head>\n</html>\n'
    actual = r.render(working_code_2)
    assert actual == expected
