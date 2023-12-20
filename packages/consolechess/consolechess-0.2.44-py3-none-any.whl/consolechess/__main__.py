"""Play a game of chess in Python module mode, i.e. `python -m chess`."""

from importlib.util import find_spec
from sys import argv

from . import asciiconsole

RICH_AVAILABLE = find_spec("rich") is not None

if RICH_AVAILABLE:
    from . import console

TEXTUAL_AVAILABLE = find_spec("textual") is not None

if TEXTUAL_AVAILABLE:
    from . import tui


def main() -> None:
    """Start chess."""
    args = " ".join(argv)
    if (
        "ascii" in args
        or "-a" in args
        or (not RICH_AVAILABLE and not TEXTUAL_AVAILABLE)
    ):
        asciiconsole.main()
    elif RICH_AVAILABLE and (
        " console" in args or "-c" in args or not TEXTUAL_AVAILABLE
    ):
        console.main()
    elif TEXTUAL_AVAILABLE:
        tui.main()
    else:
        asciiconsole.main()


if __name__ == "__main__":
    main()
