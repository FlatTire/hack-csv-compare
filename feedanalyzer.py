import csv
import logging


__version__ = '0.0-nata'


class DuplicateRowsError(Exception):
    """Describes failure where indentical hash found in >1 rows"""
    pass


class DataRow(object):
    """Data structure to describe a CSV/TDF row

    Attributes:
        hash (str): Unique identifier for a row
        values (list): Columns within a row
    """
    def __init__(self, *args):
        self.values = args

    def diff_columns(self, other):
        for idx, value in enumerate(self.values):
            if self.values[idx] != other.values[idx]:
                yield idx, self.values[idx], other.values[idx]

    def __eq__(self, other):
        return self.values == other.values

    def __getattr__(self, item):
        field_index = self.headers[item]
        return self.values[field_index]

    @property
    def hash(self):
        raise Exception("Generic {c} does not have a hash".format(
            c=self.__class__.__name__))


class FacilityRow(DataRow):
    headers = {
        'name': 0,
        'addr1': 1,
    }

    @property
    def hash(self):
        return self.values[0].lower()


class GLRow(DataRow):
    @property
    def hash(self):
        return (self.values[0] + self.values[1]).lower()


class VendorRow(DataRow):
    @property
    def hash(self):
        return self.values[0].lower()


class DataChange(object):
    pass


class Addition(DataChange):
    def __init__(self, new_row):
        self.new_row = new_row


class Deletion(DataChange):
    def __init__(self, old_row):
        self.old_row = old_row


class ColumnChange(DataChange):
    def __init__(self, field_name, left, right):
        self.field_name = field_name
        self.left = left
        self.right = right

    def __repr__(self):
        return "{field}: '{left}' -> '{right}'".format(
            field=self.field_name,
            left=getattr(self.left, self.field_name),
            right=getattr(self.right, self.field_name)
        )


def index_file(file_path, row_class, delimiter="\t", skip_rows=1):
    """Reads a structured file and returns the data in a nice data structure

    Args:
        file_path (str): String path to an input file
        row_class (cls): Class to 'typecast' data rows as
        delimiter (str): Column delimiter within file
        skip_rows (int): Number of rows to skip reading (ex. headers)
    Return:
        dict
    """
    data = {}
    duplicates = []
    with open(file_path, 'r') as input_file:
        reader = csv.reader(input_file, delimiter=delimiter)

        for row in reader:
            if skip_rows > 0:
                skip_rows -= 1
                logging.debug("Skipping row...")
                continue

            datarow = row_class(*row)
            if datarow.hash in data:
                # This is a duplicate
                duplicates.append(datarow.hash)

            data[datarow.hash] = datarow

    if len(duplicates):
        # Duplicates detected, bail now
        for duplicate_hash in duplicates:
            logging.error("Duplicate: '{key}'".format(key=duplicate_hash))

        raise DuplicateRowsError("Cannot continue with duplicates")

    return data
