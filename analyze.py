"""
Utility for comparing poorly-managed feed data files and determining changes

Usage:
    analyze.py facility [options]
    analyze.py gl [options]
    analyze.py vendor [options]
    analyze.py remit [options]

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
    from feedanalyzer import FeedAnalyzer
    from feedanalyzer import FacilityRow
    from feedanalyzer import GLRow
    from feedanalyzer import RemitToRow
    from feedanalyzer import VendorRow

    args = docopt(__doc__, version=__version__)
    skip_rows = 1
    if args['--no-header']:
        skip_rows = 0
    elif args['--skip-rows']:
        skip_rows = int(args['--skip-rows'])

    # Sanity check number of rows to skip
    if skip_rows < 0:
        raise Exception("Cannot skip < 0 rows")

    # Sanity check our file names are set
    if not args['--left']:
        raise Exception("No --left specified")
    elif not args['--right']:
        raise Exception("No --right specified")

    # Determine what row class to utilize
    if args['facility']:
        row_class = FacilityRow
    elif args['gl']:
        row_class = GLRow
    elif args['remit']:
        row_class = RemitToRow
    elif args['vendor']:
        row_class = VendorRow

    analyzer = FeedAnalyzer(left_file=args['--left'], right_file=args['--right'],
                            row_class=row_class,
                            delimiter=None, skip_rows=skip_rows)
    changes = analyzer.compare()
    print("All changes:")
    pprint(changes)
