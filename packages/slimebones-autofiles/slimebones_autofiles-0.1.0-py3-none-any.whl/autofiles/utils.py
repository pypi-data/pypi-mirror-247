from pathlib import Path

from pykit.cls import Static

from autofiles.file_extension import FileExtension, FileExtensionUtils


class AutoUtils(Static):
    @staticmethod
    def generate(
        *,
        name: str,
        extension: FileExtension,
        author: str,
        dir: Path,
        content: str,
    ) -> None:
        if not dir.exists():
            raise ValueError(f"dir {dir} does not exist")
        if not dir.is_dir():
            raise ValueError(f"{dir} is not dir")

        res = ""
        res += FileExtensionUtils.get(extension, author)
        # an additional newline for the separation, despite the fact that the
        # headers should have a default one
        res += "\n"
        res += content
        # additional newline to conform with good file-endings
        res += "\n"

        target_path = Path(dir, f".auto_{name}.{extension.value}")
        with target_path.open("w+") as f:
            f.write(res)

    @staticmethod
    def clean(dir: Path) -> None:
        """
        Removes all .auto_ prefixed files in the given dir and all subdirs.
        """
        if not dir.exists():
            raise ValueError(f"dir {dir} does not exist")
        if not dir.is_dir:
            raise ValueError(f"{dir} is not a directory")

        files = dir.rglob(".auto_*")

        for f in files:
            Path(f).unlink()
