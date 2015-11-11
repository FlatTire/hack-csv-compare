import csv
import logging
from pprint import pprint

FILE1 = "Real1.tdf"
FILE2 = "Real2.tdf"

logging.basicConfig(
    level=logging.DEBUG
)


class DataRow(object):
    @classmethod
    def read(cls, *args):
        return cls(*args)

    def __init__(self, *args):
        raise Exception("Abstract class")


class VendorRow(DataRow):
    def __init__(self, *args):
        pass


class FacilityRow(DataRow):
    def __init__(self, *args):
        self.vendor = args[0]
        self.customer = args[1]


class

class DataRow(object):
    def __init__(self, *args):
        self.V01 = args[0]
        self.V02 = args[1]
        self.V03 = args[2]
        self.V04 = args[3]
        self.V05 = args[4]
        self.V06 = args[5]
        self.V07 = args[6]
        self.V08 = args[7]
        self.V09 = args[8]
        self.V10 = args[9]
        self.V11 = args[10]
        self.V12 = args[11]
        self.V13 = args[12]
        self.V14 = args[13]
        self.V15 = args[14]
        self.V16 = args[15]

    def __eq__(self, right):
        if not self.find_different_columns(right):
            return True
        else:
            return False

    def find_different_columns(self, right):
        col_changes = []
        for attr in ['V01', 'V02', 'V03', 'V04', 'V05', 'V06', 'V07', 'V08', 'V09', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15']:
            if getattr(self, attr) != getattr(right, attr):
                col_changes.append(attr)
        return col_changes


def index_file(file_path):
    data = {}
    headers = []

    with open(file_path, 'r') as input_file:
        reader = csv.reader(input_file, delimiter="\t")
        for row in reader:
            if not headers:
                # We don't have headers yet, save them now
                headers = row
                logging.debug("Found headers: {h}".format(h=repr(headers)))
                continue
            else:
                # This is a data row
                datarow = DataRow(*row)
                data[datarow.V01] = datarow

    return data


def detect_row_changes(left, right):
    for key, value in left.items():
        if key not in right:
            # Deleted
            logging.warn(
                "Deletetion: '{k}'".format(
                    k=key))

    for key, value in right.items():
        if key not in left:
            # Added
            logging.warn(
                "Addition: '{k}'".format(
                    k=key))


def detect_col_changes(left, right):
    for key, value in right.items():
        if key not in left:
            continue

        if value != left[key]:
            # Not equal, *some* differences
            logging.debug("Column difference at '{k}'".format(k=key))
            attr_list = left[key].find_different_columns(right[key])
            for attr in attr_list:
                logging.warn("{k}: '{l}' -> '{r}'".format(
                    k=attr,
                    l=getattr(left[key], attr),
                    r=getattr(right[key], attr)))


data1 = index_file(FILE1)
logging.debug("Found {l} in {f}".format(
    l=len(data1),
    f=FILE1))

data2 = index_file(FILE2)
logging.debug("Found {l} in {f}".format(
    l=len(data2),
    f=FILE2))

###
# Analyze our files for additions & deletions at the row-level
###
detect_row_changes(data1, data2)

###
# Analyze our files for changes at the column level
###
detect_col_changes(data1, data2)
