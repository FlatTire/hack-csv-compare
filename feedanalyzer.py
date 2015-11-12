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
        'FacilityID': 0,
        'VendorID': 1,
    }

    @property
    def hash(self):
        return (self.values[0] + self.values[1]).lower()


class GLRow(DataRow):
    headers = {
        'VendorID': 0,
        'GLAccount': 1,
        'Default': 2,
    }

    @property
    def hash(self):
        return (self.values[0] + self.values[1] + self.values[2]).lower()


class VendorRow(DataRow):
    headers = {
        'VendorID': 0,
        'SupplierName': 1,
        'TaxID': 2,
        'AddressLine1': 3,
        'AddressLine2': 4,
        'City': 5,
        'State': 6,
        'Zip': 7,
        'Phone': 8,
        'PhoneExt': 9,
        'Fax': 10,
        'FaxExt': 11,
        'ApprovedSupplier': 12,
        'ActiveSupplier': 13,
        'SupplierStatus': 14,
        'PHIVendor': 15,

    }

    @property
    def hash(self):
        return self.values[0].lower()


class RemitToRow(DataRow):
    headers = {
        'VendorID': 0,
        'RemitAddressLine1': 1,
        'RemitAddressLine2': 2,
        'RemitCity': 3,
        'RemitState': 4,
        'RemitZip': 5,
        'Default': 6,
        'AddressID': 7,

    }

    @property
    def hash(self):
        return (self.values[0] + self.values[1] + self.values[2] + self.values[3] + self.values[4] + self.values[5] +
                self.values[6] + self.values[7]).lower()


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


class FeedAnalyzer(object):
    DEFAULT_DELIMITER = "\t"
    """Default delimiter to be used if none is specified explicitly"""

    DEFAULT_SKIP_ROWS = 1
    """Default number of rows to skip when reading files (ie. header rows)"""

    @classmethod
    def _find_col_changes(cls, data_left, data_right):
        """Compares two dicts and outputs the changes in columns

        Args:
            data_left (list): List of left files rows
            data_right (list): List of right files rows
        Return:
            list
        """
        column_changes = []
        for key, value in data_right.items():
            break
            if key not in data_left:
                continue

            if value != data_left[key]:
                # Not equal, *some* differences
                logging.debug("Column difference at '{k}'".format(k=key))
                attr_list = data_left[key].find_different_columns(
                    data_right[key])

                for attr in attr_list:
                    logging.warning("{k}: '{l}' -> '{r}'".format(
                        k=attr,
                        l=getattr(data_left[key], attr),
                        r=getattr(data_right[key], attr)))

        return column_changes

    @classmethod
    def _find_row_changes(cls, data_left, data_right):
        """Compares two dicts and outputs the additions and deletions

        Args:
            data_left (list): List of left files rows
            data_right (list): List of right files rows
        Return:
            list
        """
        datachanges = []
        for key, value in data_left.items():
            if key not in data_right:
                # Deleted
                logging.error(
                    "Deletion: '{k}'".format(
                        k=key))
                datachanges.append(Deletion(value))

        for key, value in data_right.items():
            if key not in data_left:
                # Added
                logging.error(
                    "Addition: '{k}'".format(
                        k=key))
                datachanges.append(Addition(value))

        return datachanges


    @classmethod
    def _index_file(cls, file_path, row_class, delimiter, skip_rows):
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

    def __init__(self, left_file, right_file, row_class, delimiter=None,
                 skip_rows=-1):
        """
        Construct new analysis class for drilling into semi-structured files
        to discover differences at the row and/or column level

        :param left_file:
        :type left_file: str
        :param right_file:
        :param row_class:
        :param delimiter:
        :param skip_rows:
        :return:
        """
        self.left_file = left_file
        self.right_file = right_file
        self.row_class = row_class
        self.delimiter = delimiter if delimiter else self.DEFAULT_DELIMITER
        self.skip_rows = skip_rows if skip_rows > -1 else self.DEFAULT_SKIP_ROWS

    def compare(self):
        """Read in files, compare changes, output list of DataChange instances

        Returns:
            list(DataChange): All changes detected between files
        """
        # 1. Read in left file
        data_left = self._index_file(self.left_file, self.row_class,
                                     self.delimiter, self.skip_rows)
        # 2. Read in right file
        data_right = self._index_file(self.right_file, self.row_class,
                                      self.delimiter, self.skip_rows)

        # 3. Init a list for collating all changes detected
        changes = []

        # 4. Find row-level changes related to hash
        changes += self._find_row_changes(data_left, data_right)

        # 5. Find column-level changes related to individual column analysis
        changes += self._find_col_changes(data_left, data_right)

        return changes
