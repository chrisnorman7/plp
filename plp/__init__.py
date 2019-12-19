"""Provides the Renderer class."""

from contextlib import redirect_stdout
from io import StringIO

from attr import attrs, attrib, Factory


class UnclosedTag(Exception):
    """A <?python block has not been closed with a matching ?> tag."""


@attrs
class Renderer:
    """Used to render PLP documents."""

    start = attrib(default=Factory(lambda: '<?python'))
    end = attrib(default=Factory(lambda: '?>'))
    filename = attrib(default=Factory(lambda: '<PLP Renderer>'))

    def render(self, string, **kwargs):
        """Render a string, replacing all code inside of a <?python ?> block
        with anything printed by that block. All kwargs are passed to eval."""
        s = ''
        while string.count(self.start):
            start_pos = string.find(self.start)
            s += string[:start_pos]
            code_start_pos = start_pos + len(self.start)
            code_end_pos = string.find(self.end, code_start_pos)
            if code_end_pos == -1:
                lines = string.count('\n', 0, start_pos)
                cols = string.split('\n')[lines].find(self.start) + 1
                lines += 1
                raise UnclosedTag(
                    f'The tag opened on line {lines} column {cols} is '
                    'unclosed.'
                )
            code = string[code_start_pos:code_end_pos]
            c = compile(code, self.filename, 'exec')
            f = StringIO()
            with redirect_stdout(f):
                eval(c, kwargs)
            f.seek(0)
            s += f.read()[:-1]
            string = string[code_end_pos + len(self.end):]
        return s + string
