"""Test an example."""
from . import main


def test_main() -> None:
    """Ensure the demo matches expected."""
    assert main() == ("<h1>My Title</h1>", "<h1>Hello Marie</h1>")
