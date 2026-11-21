"""CLI: python -m waformat [--to-md] [file]"""
import argparse
import sys

from .core import md_to_wa, wa_to_md


def main(argv=None):
    parser = argparse.ArgumentParser(prog="waformat",
                                     description="Convert Markdown to WhatsApp formatting (or back with --to-md).")
    parser.add_argument("file", nargs="?", help="Input file (default: stdin)")
    parser.add_argument("--to-md", action="store_true", help="Convert WhatsApp formatting to Markdown")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    args = parser.parse_args(argv)

    if args.file:
        with open(args.file, encoding="utf-8") as handle:
            text = handle.read()
    else:
        text = sys.stdin.read()
    result = wa_to_md(text) if args.to_md else md_to_wa(text)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(result)
    else:
        sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
