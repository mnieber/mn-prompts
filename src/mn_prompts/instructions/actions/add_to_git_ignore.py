import typing as T
from pathlib import Path


def add_to_git_ignore(project_dir: Path, entries: T.List[str]):
    git_ignore = project_dir / ".gitignore"
    text = git_ignore.read_text() if git_ignore.exists() else ""
    present = {_normalize(line) for line in text.splitlines()}
    new_entries = [entry for entry in entries if _normalize(entry) not in present]
    if not new_entries:
        return

    if text and not text.endswith("\n"):
        text += "\n"
    git_ignore.write_text(text + "".join(f"{entry}\n" for entry in new_entries))


def _normalize(line: str) -> str:
    # E.g. "/instructions/", "instructions/" and "instructions" are the same entry
    return line.strip().strip("/")
