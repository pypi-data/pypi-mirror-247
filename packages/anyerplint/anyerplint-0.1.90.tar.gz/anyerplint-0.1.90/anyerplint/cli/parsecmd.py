import argparse
import glob
import os
import re
from typing import Any

from rich.console import Console

from anyerplint.tnex import parse, translate
from anyerplint.util import open_text_file

console = Console()


def emit(s: str) -> None:
    console.print(s)


def print_recursive_lists(tree: Any, indent: int) -> None:
    first = True
    for el in tree:
        if isinstance(el, list):
            print_recursive_lists(el, indent + 1)
        else:
            t = "[deep_sky_blue1]" + el + "[/]" if first else el
            emit("  " * indent + t)
            first = False


def handle_parse(args: argparse.Namespace) -> None:
    for pat in args.filename:
        if os.path.isdir(pat):
            pat = pat + "/**/*.xml"
        fnames = glob.glob(pat, recursive=True) if "*" in pat else [pat]
        for f in fnames:
            console.rule(f)
            lines = open_text_file(f).readlines()
            for i, line_in in enumerate(lines):
                line = line_in.strip()
                expressions = re.findall("{(.*?)}", line)
                if not expressions:
                    continue
                for exp in expressions:
                    try:
                        parsed = parse(exp)
                        translated = translate(parsed[0])
                    except ValueError:
                        emit("[red]Failed to parse[/]: " + exp)
                        continue

                    if translated != exp:
                        emit(f"L[yellow]{i+1}[/]\t[darkgray]{exp}[/])")
                        emit("=>\t" + translated)
                        print_recursive_lists(parsed[0], 1)


def init_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Declare arguments you need here."""
    parser.add_argument("filename", nargs="+", help="Files to parse")
    parser.set_defaults(func=handle_parse)
    return parser
