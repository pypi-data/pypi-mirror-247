from __future__ import annotations

import argparse
import datetime
import re
from typing import Sequence

__version__ = '2023-12-20'  # ISO 8601 (YYYY-MM-DD)

# note: will miss multiline version strings (but that is unlikely given their length)
VERSION_MATCHER = re.compile(r'^\s*__version__\s*=\s*[\'"](.+)[\'"].*$')


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    return_code = 0
    for filename in args.filenames:
        with open(filename, 'r') as input_file:
            for i, line in enumerate(input_file, start=1):
                date_match = VERSION_MATCHER.match(line)
                if date_match:
                    date_value = date_match.group(1)
                    try:
                        parsed_date = datetime.datetime.strptime(date_value, '%Y-%m-%d')
                        if parsed_date.date() != datetime.datetime.today().date():
                            print(f'{filename}:{i}: ISO 8601 version string found, but it is not today: {line}')
                            return_code = 1
                    except ValueError:
                        print(f'{filename}:{i}: Invalid ISO 8601 version string found: {line}')
                        return_code = 1
                    break

    return return_code


if __name__ == '__main__':
    raise SystemExit(main())
