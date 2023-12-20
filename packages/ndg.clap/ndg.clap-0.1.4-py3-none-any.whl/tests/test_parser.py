import pathlib
import unittest
from typing import Annotated

import clap

root = pathlib.Path(__file__).parents[1]
index_html = root.joinpath("docs", "build", "html", "index.html")


def parser_new() -> clap.Parser:
    return clap.Parser(
        brief="A command-line tool for managing Minecraft servers.",
        epilog=f"Read the documentation at: {index_html.resolve()}",
    )


@clap.command(aliases=["say_hello"])
def greet(
    name: str, /, *, times: Annotated[int, clap.Range(1, 10)] = 1
) -> None:
    """Say hello to :param:`name` :param:`times` times.

    Parameters
    ----------
    name : :class:`str`
        The name to greet.

    Other Parameters
    ----------------
    times : :class:`int`, optional
        The number of times to greet the name.
    """
    for _ in range(times):
        print(f"Hello, {name}!")


class TestParser(unittest.TestCase):
    def test_parser(self):
        parser = parser_new()
        self.assertEqual(
            parser.brief, "A command-line tool for managing Minecraft servers."
        )
        self.assertEqual(
            parser.epilog,
            f"Read the documentation at: {index_html.resolve()}",
        )
        self.assertEqual(parser.all_commands, {})
        self.assertTrue("help" in parser.all_options)

    def test_command(self):
        parser = parser_new()
        clap.add_command(parser, greet)
        self.assertTrue(greet.name, "greet")
        self.assertEqual(
            greet.brief, "Say hello to :param:`name` :param:`times` times."
        )
        self.assertEqual(greet.description, "")
        self.assertEqual(greet.aliases, ["say_hello"])
        self.assertTrue("help" in greet.all_options)
        self.assertTrue(greet.parent is parser)
