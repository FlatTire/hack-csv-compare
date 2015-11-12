# CSV Comparison Helper

## Usage
### Basic Usage

```sh
$ python analyze.py vendor --left oldfile.tdf --right newfile.tdf
```

The above command will save three new files to your current working directory:

- `vendor-adds.csv` *CSV report of all new lines*
- `vendor-dels.csv` *Key name of all rows that have been deleted*
- `vendor-updates.csv` *CSV report of the key+fields that have changed*

### Help Dialog

```sh
$ python analyze.py --help
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
```

### Development
- Requires >= Python3.4
- Must have [pip](https://en.wikipedia.org/wiki/Pip_%28package_manager%29)
installed
- Must have [docopt](http://docopt.org/) Python module installed

    ```sh
    pip install docopt
    # or
    pip install -r requirements.txt
    ```
