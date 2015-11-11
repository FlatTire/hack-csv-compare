"""
Utility for comparing poorly-managed feed data files and determining changes

Usage:
    analyze.py facility [options]
    analyze.py gl [options]
    analyze.py vendor [options]

Options:
    -l, --left FILE     First file
    -r, --right FILE    Second file
    --skip-rows NUM     Number of rows to skip (ie: headers, default 1)
    -H, --no-header     Do not skip any rows
"""
from feedanalyzer import __version__


if __name__ == '__main__':
    from docopt import docopt
    from pprint import pprint

    args = docopt(__doc__, version=__version__)
    pprint(args)
