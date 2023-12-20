#!/usr/bin/python

"""
A script to check which Python functions in a given directory are missing
documentation strings. It merely checks for the presence of a docstring, not
whether it is structured correctly. It also ignores functions that start with
an underscore.
"""
from __future__ import annotations

import os
import sys
from os import path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from builtins import list as List
    from builtins import tuple as Tuple
    from typing import TextIO


def get_python_files(base_directory: str) -> List[str]:
    """Gather all Python files (ending in `.py`) in the given directory and
    subdirectories.

    Parameters
    ----------
    base_directory : :class:`str`
        The path to start looking for files.

    Returns
    -------
    :class:`list`
        A list of full paths to all Python files in the directory.
    """

    result: List[str] = []

    def traverse(directory: str) -> None:
        nonlocal result

        for file in os.listdir(directory):
            full_path = path.join(directory, file)

            if path.isdir(full_path):
                traverse(full_path)
                continue

            if not file.endswith(".py"):
                continue

            result.append(full_path)

    traverse(base_directory)

    return result


def check_file(file_path: str) -> None:
    file = open(file_path, "r")

    line_no = 0
    for line in file:
        line_no += 1
        stripped = line.strip()

        if not stripped.startswith("def "):
            continue

        _, remainder = stripped.split(" ", maxsplit=1)

        if remainder.startswith("_"):
            continue

        try:
            name, remainder = remainder.split("(", maxsplit=1)
        except ValueError:
            name = remainder.split("(", maxsplit=1)[0]
            remainder = ""

        if name.startswith("_"):
            continue

        remainder, line_no = _parse_signature(remainder, line_no, file)

        if not remainder.startswith('"""'):
            print(f"  {line_no}: Missing docstring for {name}")


def _parse_signature(
    remainder: str, line_no: int, file: TextIO
) -> Tuple[str, int]:
    stack = ["("]  # The split above removed the opening parenthesis.
    mapping = {
        ")": "(",
        "]": "[",
        "}": "{",
    }

    while stack:
        for char in remainder:
            if char in mapping:
                if stack[-1] == mapping[char]:
                    _ = stack.pop()
                else:
                    raise ValueError(f"Mismatched {char}")
            elif char in mapping.values():
                stack.append(char)
            else:
                continue

        # Parameters span multiple lines in the function definition.
        try:
            remainder = next(file)
            line_no += 1
        except StopIteration:
            break
        else:
            remainder = remainder.strip()

    return remainder, line_no


def main() -> int:
    """The main entry point for the script.

    Returns
    -------
    :class:`int`
        The exit code.
    """
    if len(sys.argv) < 2:
        script_name = path.basename(__file__)
        print(f"USAGE: {script_name} <DIRECTORY>")
        return 1

    files = get_python_files(sys.argv[1])

    print(
        "DISCLAIMER: The following list may contain false positives. "
        "Please check the files manually."
    )

    for file in files:
        print(file)
        check_file(file)

    return 0


if __name__ == "__main__":
    sys.exit(main())
