import os
import shutil
from pathlib import Path


def test_clean():
    vardir = Path(Path.cwd(), "var")

    for path in [
        Path(vardir, ".auto_test1.js"),
        Path(vardir, ".auto_test2.py"),
        Path(vardir, ".auto_test3.ts"),
    ]:
        with path.open("w+") as f:
            f.write("whocares")

    try:
        os.system(
            "poetry run python"  # noqa: S605
            f" {Path.cwd()}/autofiles/main.py clean var",
        )
        assert not list(Path(vardir).glob(".auto_*"))
    finally:
        shutil.rmtree(vardir)
