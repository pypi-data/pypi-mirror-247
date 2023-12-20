"""Simple function component, nothing dynamic, that returns a VDOM."""
from hopscotch import Registry

from .app import Heading  # noqa: F401
from viewdom import html
from viewdom import render


def main() -> str:
    """Main entry point."""
    # At startup
    registry = Registry()
    registry.scan()

    # Per request
    vdom = html("<{Heading} />")
    result = render(vdom, registry=registry)
    return result
