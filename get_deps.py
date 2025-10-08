#!/usr/bin/env python3

import toml
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Extract dependencies from pyproject.toml")
    parser.add_argument("path", help="Path to pyproject.toml file")
    parser.add_argument("-o", "--output", help="File to write the list of dependencies to (optional)")
    args = parser.parse_args()

    try:
        data = toml.load(args.path)
    except FileNotFoundError:
        print(f"Error: File '{args.path}' not found.", file=sys.stderr)
        sys.exit(1)
    except toml.TomlDecodeError as e:
        print(f"Error parsing TOML file: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        dependencies = data["project"]["dependencies"]
    except KeyError:
        print("No [project] dependencies found in the pyproject.toml.", file=sys.stderr)
        sys.exit(1)

    if args.output:
        try:
            with open(args.output, "w") as f:
                for dep in dependencies:
                    f.write(f"{dep}\n")
            print(f"Wrote {len(dependencies)} dependencies to {args.output}")
        except Exception as e:
            print(f"Error writing to output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        for dep in dependencies:
            print(dep)

if __name__ == "__main__":
    main()
