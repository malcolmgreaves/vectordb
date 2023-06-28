"""Test vectordb."""

import vectordb


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(vectordb.__name__, str)
