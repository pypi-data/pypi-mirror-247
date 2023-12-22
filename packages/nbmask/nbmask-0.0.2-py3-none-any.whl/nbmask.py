""" IPython extension to mask username from cell outputs """

import re
import os
import sys
import shlex

from pathlib import Path

from IPython.display import display
from IPython.utils.capture import capture_output
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic, line_cell_magic

from IPython.core.getipython import get_ipython

SECRETS = set()


def masked_string(text: str):
    """ Utility function to remove username from string """

    patterns = [re.escape(secret) for secret in SECRETS]

    username = os.getenv("USER")

    if username is not None:
        patterns.append(r"\b%s\b" % re.escape(username))

    pattern = "|".join(patterns)

    return re.sub(pattern, "...", text, re.IGNORECASE)


def masked_display(value, p, cycle):
    """ IPython custom display handler """

    text = masked_string(repr(value))
    p.text(text)
    return text


@magics_class
class NBMaskMagics(Magics):

    @line_magic
    def nbmask(self, line, cell=None):
        """ line magic to mask outputs """

        items = shlex.split(line)
        SECRETS.update(items)

    @cell_magic
    def masked(self, line, cell=None):
        """ cell magic to mask outputs """

        cell = cell if cell else line
        shell = get_ipython()

        with capture_output() as c:
            shell.run_cell(cell)

        if c.stderr:
            output = masked_string(c.stderr)
            print(output, file=sys.stderr)

        if c.stdout:
            output = masked_string(c.stdout)
            print(output)

        for output in c.outputs:
            display(output)


def load_ipython_extension(ipython):
    ipython.register_magics(NBMaskMagics)

    text_formatter = ipython.display_formatter.formatters['text/plain']
    text_formatter.for_type(str, masked_display)
    text_formatter.for_type(Path, masked_display)
