import argparse
import glob
import os
import re

from rich.console import Console

from anyerplint.recursive_list import RecursiveList
from anyerplint.tnex import Translator, parse
from anyerplint.util import open_text_file

console = Console(highlight=False)


def emit(s: str) -> None:
    console.print(s)


def color(text: str, color: str) -> str:
    return f"[{color}]{text}[/{color}]"


def print_recursive_lists(tree: RecursiveList[str], indent: int) -> None:
    first = True
    for el in tree:
        if isinstance(el, list):
            print_recursive_lists(el, indent + 1)
        else:
            if first:
                col = "deep_sky_blue1"
            elif el.startswith('"') and el.endswith('"'):
                col = "dark_orange"
            elif el.lower().startswith("v,"):
                col = "bright_green"
            elif el.isdecimal():
                col = "bright_yellow"
            else:
                col = None

            t = color(el, col) if col else el
            emit("  " * (indent + (not first)) + t)
            first = False


def color_translation_errors(expr: str) -> str:
    return expr.replace("~(~", "[red]").replace("~)~", "[/red]")


def handle_parse(args: argparse.Namespace) -> None:
    errors_only = args.errors
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
                        translator = Translator()
                        translated = translator.translate(parsed[0])
                    except ValueError:
                        emit("[red]Failed to parse[/]: " + exp)
                        continue

                    if errors_only and not translator.errors:
                        continue

                    if translated != exp:
                        emit(f"L[yellow]{i+1}[/]\t[grey66]{exp}[/]")
                        emit("=>\t" + color_translation_errors(translated))
                        expr = parsed[0]
                        if not isinstance(expr, list):
                            continue
                        print_recursive_lists(expr, 1)
                        emit("")


def init_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Declare arguments you need here."""
    parser.add_argument("filename", nargs="+", help="Files to parse")
    parser.add_argument(
        "--errors", action="store_true", help="Print only expressions with errors"
    )
    parser.set_defaults(func=handle_parse)
    return parser
