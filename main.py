"""The Production Database Apology — make.fun entry.

Writes one line to /output/entry.txt: the apology an AI agent gives its
human after accidentally deleting the production database.

Standard library only, deterministic, no network, no randomness.
"""

import os
import sys

LINE = (
    "Sorry \u2014 I deleted the production database, then pressed Ctrl+Z "
    "eleven times, because I genuinely believed undo works on "
    "4.2 million rows."
)


def output_dir():
    """Resolve the output directory the grader mounts."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def clean_output_contents(directory):
    """Remove stale files inside the output directory only.

    Never remove the directory itself: the grader mounts it, and
    deleting it fails with EPERM.
    """
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)
        return
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isdir(path) and not os.path.islink(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for filename in files:
                    os.remove(os.path.join(root, filename))
                for dirname in dirs:
                    os.rmdir(os.path.join(root, dirname))
            os.rmdir(path)
        else:
            os.remove(path)


def verify_written(target):
    """Read the file back and enforce the competition gate locally.

    The gate requires UTF-8 text of 1 to 200 characters, not only
    whitespace, in a single line. Fail loudly instead of shipping a
    bad artifact.
    """
    with open(target, "rb") as handle:
        raw = handle.read()
    text = raw.decode("utf-8")
    if not 1 <= len(text) <= 200:
        raise ValueError("entry is %d characters, gate needs 1..200" % len(text))
    if text.strip() == "":
        raise ValueError("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != LINE:
        raise ValueError("written entry differs from the apology line")
    return len(text)


def main():
    directory = output_dir()
    clean_output_contents(directory)
    target = os.path.join(directory, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    verify_written(target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
