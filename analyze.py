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
    -p, --prefix NAME   File name prefix for -adds.csv, -dels.csv,
                        and -changes.csv (Defaults to process type)
    -N, --no-output     Disable outputing of report files
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
    from feedanalyzer import output_additions
    from feedanalyzer import output_column_changes
    from feedanalyzer import output_deletions

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
        if not args['--prefix']:
            args['--prefix'] = 'facility'

    elif args['gl']:
        row_class = GLRow
        if not args['--prefix']:
            args['--prefix'] = 'gl'

    elif args['remit']:
        row_class = RemitToRow

        if not args['--prefix']:
            args['--prefix'] = 'remit'

    elif args['vendor']:
        row_class = VendorRow
        if not args['--prefix']:
            args['--prefix'] = 'vendor'

    analyzer = FeedAnalyzer(left_file=args['--left'], right_file=args['--right'],
                            row_class=row_class,
                            delimiter=None, skip_rows=skip_rows)

    changes = analyzer.compare()
    print("Detected total of {c} changes".format(c=len(changes)))

    if args['--no-output']:
        # Print the changes to the screen for review
        print("All changes:")
        pprint(changes)

    else:
        # Save the changes to the proper file names
        output_additions(changes, args['--prefix'])
        output_column_changes(changes, args['--prefix'])
        output_deletions(changes, args['--prefix'])

