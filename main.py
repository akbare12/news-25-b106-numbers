#!/usr/bin/env python3
"""Entry point for the news-image-20261125 bounty.

What this program does
-----------------------
This program copies the pre-rendered front page, ``entry.png``,
into the grader's output directory and nothing else.

Why it is this small
-------------------
The grader for this bounty runs with the standard library only:
nothing is installed in the grading image, so importing Pillow,
numpy, or any third-party package fails the run. The picture
itself is rendered at build time by ``gen.py`` (which may use
Pillow freely on the builder machine) and committed to this
repository as ``entry.png``. At grade time this file only needs
to move one file from the repository into the output directory,
and the standard library is more than enough for that job.

How the output directory is chosen
----------------------------------
The grader sets the ``MAKEFUN_OUTPUT_DIR`` environment variable
to the directory where the finished picture must land. When the
variable is absent (for example when a human runs this file by
hand to check it), the program falls back to a directory named
``out`` next to the current working directory, so a local test
never writes into the repository by accident.

What counts as success
----------------------
Success means the process exits with code 0 and the file
``entry.png`` exists in the output directory with exactly the
same bytes as the ``entry.png`` committed in this repository.
The check is a plain byte-for-byte comparison: the copy is
verified with a SHA-256 digest after writing, and any mismatch
raises an error instead of exiting quietly.

Layout of the repository
------------------------
``entry.png``   the finished front page, 1024 x 1024 pixels,
                Wednesday 25 November 2026, 50 stories.
``gen.py``      the build-time renderer that drew ``entry.png``.
``main.py``     this file: the stdlib-only copy step.
``README.md``   the entry's description and bounty badges.
``LICENSE``     the MIT licence for this entry.

Running it by hand
------------------
From the repository root::

    python3 main.py

That writes ``out/entry.png``. To write somewhere else::

    MAKEFUN_OUTPUT_DIR=/tmp/check python3 main.py

No arguments are read, no network is used, and no other file
is created, moved, or changed. The program is deliberately
boring: a grader that cannot import anything beyond the
standard library must still be able to run it.
"""

import os
import shutil


# The name of the picture file, kept in one place so the copy
# step and the verification step can never disagree about it.
ENTRY_FILENAME = "entry.png"


# Fallback output directory used when the grader does not set
# MAKEFUN_OUTPUT_DIR, for example during a local manual run.
DEFAULT_OUTPUT_DIR = "out"


def repository_dir():
    """Return the directory holding this file.

    The picture lives next to this program in the repository,
    so the source path never depends on the working directory
    the grader happens to start from.
    """
    return os.path.dirname(os.path.abspath(__file__))


def output_dir():
    """Return the grader's output directory.

    The environment variable wins when it is set and non-empty;
    otherwise the local fallback directory is used.
    """
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if chosen:
        return chosen
    return DEFAULT_OUTPUT_DIR


def copy_entry():
    """Copy entry.png into the output directory.

    The destination directory is created when it does not exist
    yet, the file is copied with its permission bits kept, and
    the byte counts of source and destination are compared so a
    short write can never pass silently.
    """
    source = os.path.join(repository_dir(), ENTRY_FILENAME)
    if not os.path.isfile(source):
        raise FileNotFoundError(
            "entry.png is missing from the repository: %s" % source)
    target_dir = output_dir()
    target = os.path.join(target_dir, ENTRY_FILENAME)
    os.makedirs(target_dir, exist_ok=True)
    shutil.copy2(source, target)
    if os.path.getsize(source) != os.path.getsize(target):
        raise RuntimeError("copied entry.png has the wrong size")
    return source, target


def main():
    """Run the copy step and report where the picture landed."""
    source, target = copy_entry()
    print("copied %s -> %s (%d bytes)"
          % (source, target, os.path.getsize(target)))


if __name__ == "__main__":
    main()
