"""Getting a doctype into the rendered output is a bit tricky."""
from markupsafe import Markup

from viewdom import html
from viewdom import render


def main() -> str:
    """Main entry point."""
    doctype = Markup("<!DOCTYPE html>\n")
    vdom = html("{doctype}<div>Hello World</div>")

    result = render(vdom)
    return result
