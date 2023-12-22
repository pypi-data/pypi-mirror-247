from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def create_vardir():
    vardir = Path(Path.cwd(), "var")
    vardir.mkdir(exist_ok=True)
