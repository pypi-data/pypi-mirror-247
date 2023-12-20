"""Test an example."""
from . import main
from viewdom import VDOMNode


def test_readme_() -> None:
    """Ensure the demo matches expected."""
    expected = VDOMNode(tag="div", props={}, children=["Hello World"])
    assert main() == expected
