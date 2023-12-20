# cython: profile=True

'''
Python equivalents of various excel functions
'''

# source: https://github.com/dgorissen/pycel/blob/master/src/pycel/excellib.py

from __future__ import absolute_import, division

import itertools
import math

import numpy as np
import scipy.optimize
import datetime
import random
from math import log, ceil
from decimal import Decimal, ROUND_UP, ROUND_HALF_UP
from calendar import monthrange
from dateutil.relativedelta import relativedelta

# from openpyxl.compat import unicode
unicode = str

from SusteenExToPy.utils import *
from SusteenExToPy.Range import RangeCore as Range
from SusteenExToPy.ExcelError import *
from functools import reduce

######################################################################################
# A dictionary that maps excel function names onto python equivalents. You should
# only add an entry to this map if the python name is different to the excel name
# (which it may need to be to  prevent conflicts with existing python functions
# with that name, e.g., max).

# So if excel defines a function foobar(), all you have to do is add a function
# called foobar to this module.  You only need to add it to the function map,
# if you want to use a different name in the python code.

# Note: some functions (if, pi, atan2, and, or, array, ...) are already taken care of
# in the FunctionNode code, so adding them here will have no effect.
FUNCTION_MAP = {
    "ln":"xlog",
    "min":"xmin",
    "min":"xmin",
    "max":"xmax",
    "sum":"xsum",
    "gammaln":"lgamma",
    "round": "xround"
}

IND_FUN = [
    "SUM",
    "MIN",
    "IF",
    "TAN",
    "ATAN2",
    "ARRAY",
    "ARRAYROW",
    "AND",
    "OR",
    "ALL",
    "VALUE",
    "LOG",
    "MAX",
    "SUMPRODUCT",
    "IRR",
    "MIN",
    "SUM",
    "CHOOSE",
    "SUMIF",
    "AVERAGE",
    "RIGHT",
    "INDEX",
    "LOOKUP",
    "LINEST1",
    "LINEST2",
    "NPV",
    "MATCH",
    "MOD",
    "COS",
    "PI_2",
    "COUNT",
    "COUNTA",
    "COUNTIF",
    "COUNTIFS",
    "EXP",
    "FLOOR",
    "MATCH",
    "MROUND",
    "LOOKUP",
    "INDEX",
    "AVERAGE",
    "SUMIFS",
    "ROUND",
    "ROWS",
    "COLUMNS",
    "MID",
    "DATE",
    "YEARFRAC",
    "ISNA",
    "ISBLANK",
    "ISTEXT",
    "OFFSET",
    "PRODUCT",
    "SUMPRODUCT",
    "IFERROR",
    "XIRR",
    "VENTILATION",
    "HLOOKUP",
    "VLOOKUP",
    "VDB",
    "SLN",
    "XNPV",
    "PMT",
    "ROUNDDOWN"
    "ROUNDUP",
    "ROUNDX",
    "POWER",
    "SQRT",
    "TODAY",
    "YEAR",
    "MONTH",
    "EOMONTH",
    "RANDBETWEEN",
    "RAND",
]

CELL_CHARACTER_LIMIT = 32767
EXCEL_EPOCH = datetime.datetime.strptime("1900-01-01", '%Y-%m-%d').date()

######################################################################################
# List of excel equivalent functions
# TODO: needs unit testing


def value(text):
    # make the distinction for naca numbers
    if text.find('.') > 0:
        return float(text)
    elif text.endswith('%'):
        text = text.replace('%', '')
        return float(text) / 100
    else:
        return int(text)


def xlog(a):
    try:
        if isinstance(a,(list,tuple,np.ndarray)):
            return [log(x) for x in flatten(a)]
        else:
            #print a
            return log(a)
    except:
        return TypeError("Not real number")


def xmax(*args): # Excel reference: https://support.office.com/en-us/article/MAX-function-e0012414-9ac8-4b34-9a47-73e662c08098
    # ignore non numeric cells and boolean cells
    values = extract_numeric_values(*args)

    # however, if no non numeric cells, return zero (is what excel does)
    if len(values) < 1:
        return 0
    else:
        return max(values)


def xmin(*args): # Excel reference: https://support.office.com/en-us/article/MIN-function-61635d12-920f-4ce2-a70f-96f202dcc152
    # ignore non numeric cells and boolean cells
    values = extract_numeric_values(*args)

    # however, if no non numeric cells, return zero (is what excel does)
    if len(values) < 1:
        return 0
    else:
        return min(values)


def xsum(*args): # Excel reference: https://support.office.com/en-us/article/SUM-function-043e1c7d-7726-4e80-8f32-07b23e057f89
    # ignore non numeric cells and boolean cells

    values = extract_numeric_values(*args)

    # however, if no non numeric cells, return zero (is what excel does)
    if len(values) < 1:
        return 0
    else:
        return sum(values)


def choose(index_num, *values): # Excel reference: https://support.office.com/en-us/article/CHOOSE-function-fc5c184f-cb62-4ec7-a46e-38653b98f5bc

    index = int(index_num)

    if index <= 0 or index > 254:
        return ExcelError('#VALUE!', '%s must be between 1 and 254' % str(index_num))
    elif index > len(values):
        return ExcelError('#VALUE!', '%s must not be larger than the number of values: %s' % (str(index_num), len(values)))
    else:
        return values[index - 1]


def sumif(range, criteria, sum_range = None): # Excel reference: https://support.office.com/en-us/article/SUMIF-function-169b8c99-c05c-4483-a712-1697a653039b

    # WARNING:
    # - wildcards not supported
    # - doesn't really follow 2nd remark about sum_range length
    # print(sum_range.values)
    if not isinstance(range, Range):
        return TypeError('%s must be a Range' % str(range))

    if isinstance(criteria, Range) and not isinstance(criteria , (str, bool)): # ugly...
        return 0

    indexes = find_corresponding_index(range.values, criteria)

    if sum_range:
        if not isinstance(sum_range, Range):
            return TypeError('%s must be a Range' % str(sum_range))

        newrange = []
        for val in sum_range.values:
            # print("val", val)
            if val is None:
                newrange.append(0)
            else:
                newrange.append(val)

        # print("newrng", newrange)
        def f(x):
            return newrange[x] if x < sum_range.length else 0
        # print(map(f, indexes))
        return sum(map(f, indexes))

    else:
        return sum([range.values[x] for x in indexes])


def sumifs(*args):
    # Excel reference: https://support.office.com/en-us/article/
    #   sumifs-function-c9e748f5-7ea7-455d-9406-611cebce642b

    nb_criteria = (len(args)-1) / 2

    args = list(args)

    # input checks
    if nb_criteria == 0:
        return TypeError('At least one criteria and criteria range should be provided.')
    if int(nb_criteria) != nb_criteria:
        return TypeError('Number of criteria an criteria ranges should be equal.')
    nb_criteria = int(nb_criteria)

    # separate arguments
    sum_range = args[0]
    criteria_ranges = args[1::2]
    criteria = args[2::2]
    index = list(range(0, len(sum_range)))

    for i in range(nb_criteria):

        criteria_range = criteria_ranges[i]
        criterion = str(criteria[i])

        index_tmp = find_corresponding_index(criteria_range.values, criterion)
        index = np.intersect1d(index, index_tmp)

    sum_select = [sum_range.values[i] for i in index]
    try:
        res = sum(sum_select)
    except:
        res = 0

    return res


def average(*args): # Excel reference: https://support.office.com/en-us/article/AVERAGE-function-047bac88-d466-426c-a32b-8f33eb960cf6
    # ignore non numeric cells and boolean cells
    values = extract_numeric_values(*args)

    return sum(values) / len(values)


def right(text,n):
    #TODO: hack to deal with naca section numbers
    if isinstance(text, unicode) or isinstance(text,str):
        return text[-n:]
    else:
        # TODO: get rid of the decimal
        return str(int(text))[-n:]


def index(my_range, row, col = None): # Excel reference: https://support.office.com/en-us/article/INDEX-function-a5dcf0dd-996d-40a4-a822-b56b061328bd

    for i in [my_range, row, col]:
        if isinstance(i, ExcelError) or i in ErrorCodes:
            return i

    row = int(row) if row is not None else row
    col = int(col) if col is not None else col

    if isinstance(my_range, Range):
        cells = my_range.addresses
        # print(cells)
        nr = my_range.nrows
        nc = my_range.ncols
    else:
        cells, nr, nc = my_range
        # print(cells)
        if nr > 1 or nc > 1:
            a = np.array(cells)
            cells = a.flatten().tolist()
    # print(cells)
    nr = int(nr)
    nc = int(nc)

    if type(cells) != list:
        return ExcelError('#VALUE!', '%s must be a list' % str(cells))

    if row is not None and not is_number(row):
        return ExcelError('#VALUE!', '%s must be a number' % str(row))

    if row == 0 and col == 0:
        return ExcelError('#VALUE!', 'No index asked for Range')

    if col is None and nr == 1 and row <= nc:
        # special case where index is matched on row, and the second row input can be used as a col
        col = row
        row = None

    if row is not None and row > nr:
        return ExcelError('#VALUE!', 'Index %i out of range' % row)

    if nr == 1:
        col = row if col is None else col
        return cells[int(col) - 1]

    if nc == 1:
        # print(cells[int(row) - 1])
        return cells[int(row) - 1]

    else: # could be optimised
        if col is None or row is None:
            return ExcelError('#VALUE!', 'Range is 2 dimensional, can not reach value with 1 arg as None')

        if not is_number(col):
            return ExcelError('#VALUE!', '%s must be a number' % str(col))

        if col > nc:
            return ExcelError('#VALUE!', 'Index %i out of range' % col)

        indices = list(range(len(cells)))

        if row == 0: # get column
            filtered_indices = [x for x in indices if x % nc == col - 1]
            filtered_cells = [cells[i] for i in filtered_indices]

            return filtered_cells

        elif col == 0: # get row
            filtered_indices = [x for x in indices if int(x / nc) == row - 1]
            filtered_cells = [cells[i] for i in filtered_indices]

            return filtered_cells

        else:
            return cells[(row - 1)* nc + (col - 1)]


def lookup(value, lookup_range, result_range = None): # Excel reference: https://support.office.com/en-us/article/LOOKUP-function-446d94af-663b-451d-8251-369d5e3864cb

    # TODO
    if not isinstance(value,(int,float)):
        return Exception("Non numeric lookups (%s) not supported" % value)

    # TODO: note, may return the last equal value

    # index of the last numeric value
    lastnum = -1
    for i,v in enumerate(lookup_range.values):
        if isinstance(v,(int,float)):
            if v > value:
                break
            else:
                lastnum = i

    output_range = result_range.values if result_range is not None else lookup_range.values

    if lastnum < 0:
        return ExcelError('#VALUE!', 'No numeric data found in the lookup range')
    else:
        if i == 0:
            return ExcelError('#VALUE!', 'All values in the lookup range are bigger than %s' % value)
        else:
            if i >= len(lookup_range)-1:
                # return the biggest number smaller than value
                return output_range[lastnum]
            else:
                return output_range[i-1]


# NEEDS TEST
def linest1(*args, **kwargs): # Excel reference: https://support.office.com/en-us/article/LINEST-function-84d7d0d9-6e50-4101-977a-fa7abf772b6d

    Y = extract_numeric_values(args[0])
    X = extract_numeric_values(args[1])
    # print(Y)
    # print(Y)
    if len(args) == 3:
        const = args[2]
        if isinstance(const,str):
            const = (const.lower() == "true")
    else:
        const = True

    degree = kwargs.get('degree',1)

    # build the vandermonde matrix
    A = np.vander(X, degree+1)

    if not const:
        # force the intercept to zero
        A[:,-1] = np.zeros((1,len(X)))

    # perform the fit
    (coefs, residuals, rank, sing_vals) = np.linalg.lstsq(A, Y, rcond=None)

    return coefs[0]

def linest2(*args, **kwargs): # Excel reference: https://support.office.com/en-us/article/LINEST-function-84d7d0d9-6e50-4101-977a-fa7abf772b6d
    # dd=args[0]
    # print(dd)
    # print(extract_numeric_values(dd))


    # Y = list(args[0].values())
    # X = list(args[1].values())
    Y = extract_numeric_values(args[0])
    X = extract_numeric_values(args[1])
    # print(Y)
    if len(args) == 3:
        const = args[2]
        if isinstance(const,str):
            const = (const.lower() == "true")
    else:
        const = True

    degree = kwargs.get('degree',1)

    # build the vandermonde matrix
    A = np.vander(X, degree+1)

    if not const:
        # force the intercept to zero
        A[:,-1] = np.zeros((1,len(X)))

    # perform the fit
    (coefs, residuals, rank, sing_vals) = np.linalg.lstsq(A, Y, rcond=None)

    return coefs[1]


def npv(rate, *values): # Excel reference: https://support.office.com/en-us/article/NPV-function-8672cb67-2576-4d07-b67b-ac28acf2a568
    cashflow = list(flatten_list(list(values)))

    if is_not_number_input(rate):
        return numeric_error(rate, 'rate')

    if is_not_number_input(cashflow):
        return numeric_error(cashflow, 'values')

    if isinstance(cashflow, Range):
        cashflow = cashflow.values

    return sum([float(x)*(1+rate)**-(i+1) for (i,x) in enumerate(cashflow)])


def rows(array):
    """
    Function to find the number of rows in an array.
    Excel reference: https://support.office.com/en-ie/article/rows-function-b592593e-3fc2-47f2-bec1-bda493811597

    :param array: the array of which the rows should be counted.
    :return: the number of rows.
    """

    if isinstance(array, (float, int)):
        rows = 1  # special case for A1:A1 type ranges which for some reason only return an int/float
    elif array is None:
        rows = 1  # some A1:A1 ranges return None (issue with ref cell)
    else:
        rows = len(array.values)

    return rows


def columns(array):
    """
    Function to find the number of columns in an array.
    Excel reference: https://support.office.com/en-us/article/columns-function-4e8e7b4e-e603-43e8-b177-956088fa48ca

    :param array: the array of which the columns should be counted.
    :return: the number of columns.
    """

    return rows(array)


def match(lookup_value, lookup_range, match_type=1): # Excel reference: https://support.office.com/en-us/article/MATCH-function-e8dffd45-c762-47d6-bf89-533f4a37673a

    if not isinstance(lookup_range, Range):
        return ExcelError('#VALUE!', 'Lookup_range is not a Range')

    def type_convert(value):
        if type(value) == str:
            value = value.lower()
        elif type(value) == int:
            value = float(value)
        elif value is None:
            value = 0

        return value;
    def type_convert_float(value):
        if is_number(value):
            value = float(value)
        else:
            value = None

        return value

    lookup_value = type_convert(lookup_value)

    range_values = [x for x in lookup_range.values if x is not None] # filter None values to avoid asc/desc order errors
    range_length = len(range_values)

    if match_type == 1:
        # Verify ascending sort

        posMax = -1
        for i in range(range_length):
            current = type_convert(range_values[i])

            if i < range_length - 1:
                if current > type_convert(range_values[i + 1]):
                    return ExcelError('#VALUE!', 'for match_type 1, lookup_range must be sorted ascending')
            if current <= lookup_value:
                posMax = i
        if posMax == -1:
            return ExcelError('#VALUE!','no result in lookup_range for match_type 1')
        return posMax +1 #Excel starts at 1

    elif match_type == 0:
        # No string wildcard
        try:
            if is_number(lookup_value):
                lookup_value = float(lookup_value)
                output = [type_convert_float(x) for x in range_values].index(lookup_value) + 1
            else:
                output = [str(x).lower() for x in range_values].index(lookup_value) + 1
            return output
        except:
            return ExcelError('#VALUE!', '%s not found' % lookup_value)

    elif match_type == -1:
        # Verify descending sort
        posMin = -1
        for i in range((range_length)):
            current = type_convert(range_values[i])

            if i is not range_length-1 and current < type_convert(range_values[i+1]):
               return ExcelError('#VALUE!','for match_type -1, lookup_range must be sorted descending')
            if current >= lookup_value:
               posMin = i
        if posMin == -1:
            return ExcelError('#VALUE!', 'no result in lookup_range for match_type -1')
        return posMin +1 #Excel starts at 1


def mod(nb, q): # Excel Reference: https://support.office.com/en-us/article/MOD-function-9b6cd169-b6ee-406a-a97b-edf2a9dc24f3
    if not isinstance(nb, int):
        return ExcelError('#VALUE!', '%s is not an integer' % str(nb))
    elif not isinstance(q, int):
        return ExcelError('#VALUE!', '%s is not an integer' % str(q))
    else:
        return nb % q

def mround(number, significance):
    if not is_number(number):
        return ExcelError('#VALUE!', '%s is not a number' % str(number))
    if not is_number(significance):
        return ExcelError('#VALUE!', '%s is not a number' % str(significance))

    return round(number / significance, 0) * significance


def eomonth(start_date, months): # Excel reference: https://support.office.com/en-us/article/eomonth-function-7314ffa1-2bc9-4005-9d66-f49db127d628
    if not is_number(start_date):
        return ExcelError('#VALUE!', 'start_date %s must be a number' % str(start_date))
    if start_date < 0:
        return ExcelError('#VALUE!', 'start_date %s must be positive' % str(start_date))

    if not is_number(months):
        return ExcelError('#VALUE!', 'months %s must be a number' % str(months))

    y1, m1, d1 = date_from_int(start_date)
    start_date_d = datetime.date(year=y1, month=m1, day=d1)
    end_date_d = start_date_d + relativedelta(months=int(months))
    y2 = end_date_d.year
    m2 = end_date_d.month
    d2 = monthrange(y2, m2)[1]
    res = int(int_from_date(datetime.date(y2, m2, d2)))

    return res


def year(serial_number): # Excel reference: https://support.office.com/en-us/article/year-function-c64f017a-1354-490d-981f-578e8ec8d3b9
    if not is_number(serial_number):
        return ExcelError('#VALUE!', 'start_date %s must be a number' % str(serial_number))
    if serial_number < 0:
        return ExcelError('#VALUE!', 'start_date %s must be positive' % str(serial_number))

    y1, m1, d1 = date_from_int(serial_number)

    return y1


def month(serial_number): # Excel reference: https://support.office.com/en-us/article/month-function-579a2881-199b-48b2-ab90-ddba0eba86e8
    if not is_number(serial_number):
        return ExcelError('#VALUE!', 'start_date %s must be a number' % str(serial_number))
    if serial_number < 0:
        return ExcelError('#VALUE!', 'start_date %s must be positive' % str(serial_number))

    y1, m1, d1 = date_from_int(serial_number)

    return m1

def cos(serial_number):
    if not is_number(serial_number):
        return ExcelError('#VALUE!', 'start_date %s must be a number' % str(serial_number))
    return math.cos(serial_number)

def pi_2(*arg):

    return math.pi

def count(*args): # Excel reference: https://support.office.com/en-us/article/COUNT-function-a59cd7fc-b623-4d93-87a4-d23bf411294c
    l = list(args)

    total = 0

    for arg in l:
        if isinstance(arg, Range):
            total += len([x for x in arg.values if is_number(x) and type(x) is not bool]) # count inside a list
        elif is_number(arg): # int() is used for text representation of numbers
            total += 1

    return total


def counta(range):
    if isinstance(range, ExcelError) or range in ErrorCodes:
        if range.value == '#NULL':
            return 0
        else:
            return range # return the Excel Error
            # raise Exception('ExcelError other than #NULL passed to excellib.counta()')
    else:
        return len([x for x in range.values if x != None])


def countif(range, criteria): # Excel reference: https://support.office.com/en-us/article/COUNTIF-function-e0de10c6-f885-4e71-abb4-1f464816df34

    # WARNING:
    # - wildcards not supported
    # - support of strings with >, <, <=, =>, <> not provided

    valid = find_corresponding_index(range.values, criteria)

    return len(valid)


def countifs(*args): # Excel reference: https://support.office.com/en-us/article/COUNTIFS-function-dda3dc6e-f74e-4aee-88bc-aa8c2a866842

    arg_list = list(args)
    l = len(arg_list)

    if l % 2 != 0:
        return ExcelError('#VALUE!', 'excellib.countifs() must have a pair number of arguments, here %d' % l)


    if l >= 2:
        indexes = find_corresponding_index(args[0].values, args[1]) # find indexes that match first layer of countif

        remaining_ranges = [elem for i, elem in enumerate(arg_list[2:]) if i % 2 == 0] # get only ranges
        remaining_criteria = [elem for i, elem in enumerate(arg_list[2:]) if i % 2 == 1] # get only criteria

        # verif that all Ranges are associated COULDNT MAKE THIS WORK CORRECTLY BECAUSE OF RECURSION
        # association_type = None

        # temp = [args[0]] + remaining_ranges

        # for index, range in enumerate(temp): # THIS IS SHIT, but works ok
        #     if type(range) == Range and index < len(temp) - 1:
        #         asso_type = range.is_associated(temp[index + 1])

        #         print 'asso', asso_type
        #         if association_type is None:
        #             association_type = asso_type
        #         elif associated_type != asso_type:
        #             association_type = None
        #             break

        # print 'ASSO', association_type

        # if association_type is None:
        #     return ValueError('All items must be Ranges and associated')

        filtered_remaining_ranges = []

        for range in remaining_ranges: # filter items in remaining_ranges that match valid indexes from first countif layer
            filtered_remaining_cells = []
            filtered_remaining_range = []

            for index, item in enumerate(range.values):
                if index in indexes:
                    filtered_remaining_cells.append(range.addresses[index]) # reconstructing cells from indexes
                    filtered_remaining_range.append(item) # reconstructing values from indexes

            # WARNING HERE
            filtered_remaining_ranges.append(Range(filtered_remaining_cells, filtered_remaining_range))

        new_tuple = ()

        for index, range in enumerate(filtered_remaining_ranges): # rebuild the tuple that will be the argument of next layer
            new_tuple += (range, remaining_criteria[index])

        return min(countifs(*new_tuple), len(indexes)) # only consider the minimum number across all layer responses

    else:
        return float('inf')

def exp(number):
    if not is_number(number):
        return ExcelError('#VALUE!', '%s is not a number' % str(number))
    return math.exp(number)
    

def floor(number, significance=None):
    if not is_number(number):
        return ExcelError('#VALUE!', '%s is not a number' % str(number))
    # print(number)
    fracn = len(str(math.modf(number)[0]))-2

    # print(fracn)
    # print(len(str(frac(0))))
    # number=round(number,fracn)
    # significance=Decimal(significance)
    if significance is None:
        return math.floor(number)
    elif not is_number(significance):
        return ExcelError('#VALUE!', '%s is not a number' % str(significance))
    else:
        fracs = len(str(math.modf(significance)[0])) - 2
        dec = max(fracn, fracs)
        # print(dec)

        significance=round(significance,fracs)
        # print(fracs)
        # print(number, significance)
        # print('floor', round(number/significance,dec))
        # print(math.modf(round(number/significance,dec))[0])
        if math.modf(round(number/significance,dec))[0]==0:
            # print(int(round(number/significance,dec)))
            return number
        else:
            return math.floor(round(number/significance,dec))*significance


def xround(number, num_digits = 0): # Excel reference: https://support.office.com/en-us/article/ROUND-function-c018c5d8-40fb-4053-90b1-b3e7f61a213c

    if not is_number(number):
        return ExcelError('#VALUE!', '%s is not a number' % str(number))
    if not is_number(num_digits):
        return ExcelError('#VALUE!', '%s is not a number' % str(num_digits))

    number = float(number) # if you don't Spreadsheet.dump/load, you might end up with Long numbers, which Decimal doesn't accept

    if num_digits >= 0: # round to the right side of the point
        return float(Decimal(repr(number)).quantize(Decimal(repr(pow(10, -num_digits))), rounding=ROUND_HALF_UP))
        # see https://docs.python.org/2/library/functions.html#round
        # and https://gist.github.com/ejamesc/cedc886c5f36e2d075c5

    else:
        return round(number, num_digits)

def rounddown(number, num_digits = 0): # Excel reference: https://support.office.com/en-us/article/ROUNDUP-function-f8bc9b23-e795-47db-8703-db171d0c42a7

    if not is_number(number):
        return ExcelError('#VALUE!', '%s is not a number' % str(number))
    if not is_number(num_digits):
        return ExcelError('#VALUE!', '%s is not a number' % str(num_digits))

    number = float(number) # if you don't Spreadsheet.dump/load, you might end up with Long numbers, which Decimal doesn't accept

    if num_digits >= 0: # round to the right side of the point
        stepper = 10 ** num_digits
        # print(number)
        # print(math.trunc(stepper * number)/stepper)
        # print(Decimal(number).quantize(Decimal('0.000')))
        # print(Decimal(number).quantize(Decimal('0.0000'),rounding=ROUND_UP))
        return float(math.trunc(stepper * number)/stepper)
        # see https://docs.python.org/2/library/functions.html#round
        # and https://gist.github.com/ejamesc/cedc886c5f36e2d075c5

    else:
        return floor(number / pow(10, -num_digits)) * pow(10, -num_digits)


def roundup(number, num_digits = 0): # Excel reference: https://support.office.com/en-us/article/ROUNDUP-function-f8bc9b23-e795-47db-8703-db171d0c42a7

    if not is_number(number):
        return ExcelError('#VALUE!', '%s is not a number' % str(number))
    if not is_number(num_digits):
        return ExcelError('#VALUE!', '%s is not a number' % str(num_digits))

    number = float(number) # if you don't Spreadsheet.dump/load, you might end up with Long numbers, which Decimal doesn't accept

    if num_digits >= 0: # round to the right side of the point
        return float(Decimal(repr(number)).quantize(Decimal(repr(pow(10, -num_digits))), rounding=ROUND_UP))
        # see https://docs.python.org/2/library/functions.html#round
        # and https://gist.github.com/ejamesc/cedc886c5f36e2d075c5

    else:
        return ceil(number / pow(10, -num_digits)) * pow(10, -num_digits)


def roundx(number, roundtype):
    if number is None:
        number = 0
    if not is_number(number):
        return ExcelError('#VALUE!', '%s is not a number' % str(number))
    if roundtype not in [-1, 0, 1]:
        return ExcelError('#VALUE!', '%s is not a number' % str(roundtype))

    bijlagex = [9.5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                      22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 44,
                      48, 52, 56, 60, 65, 70, 75, 80, 85, 90, 95, 100]

    if number == 0:
        return 0

    digits = int(math.floor(math.log(number, math.e) / math.log(10, math.e)))

    tmpnum = number / 10 ** (digits - 1)

    if tmpnum < 10 or tmpnum >= 100:
        return ExcelError('#VALUE!', '%s is not rounded properly' % str(roundtype))

    for i, n in enumerate(bijlagex):
        if roundtype == -1:
            if tmpnum == n:
                pos = i
                break
            if n > tmpnum:
                newnum = n
                pos = i - 1
                break
        elif roundtype == 1:

            # if tmpnum == n:
            #     pos = i
            #     break
            if n > tmpnum:
                pos = i
                break

        elif roundtype == 0:
            if tmpnum == n:
                pos = i
                break

            elif n > tmpnum:
                if (tmpnum - bijlagex[i - 1]) >= (bijlagex[i] - tmpnum):
                    pos = i

                else:
                    pos = i - 1
                break

    newnum = bijlagex[pos] * 10 ** (digits - 1)
    return newnum


def mid(text, start_num, num_chars): # Excel reference: https://support.office.com/en-us/article/MID-MIDB-functions-d5f9e25c-d7d6-472e-b568-4ecb12433028

    text = str(text)

    if len(text) > CELL_CHARACTER_LIMIT:
        return ExcelError('#VALUE!', 'text is too long. Is %s needs to be %s or less.' % (len(text), CELL_CHARACTER_LIMIT))

    if type(start_num) != int:
        return ExcelError('#VALUE!', '%s is not an integer' % str(start_num))
    if type(num_chars) != int:
        return ExcelError('#VALUE!', '%s is not an integer' % str(num_chars))

    if start_num < 1:
        return ExcelError('#VALUE!', '%s is < 1' % str(start_num))
    if num_chars < 0:
        return ExcelError('#VALUE!', '%s is < 0' % str(num_chars))

    return text[(start_num - 1): (start_num - 1 + num_chars)]


def date(year, month, day): # Excel reference: https://support.office.com/en-us/article/DATE-function-e36c0c8c-4104-49da-ab83-82328b832349

    if type(year) != int:
        return ExcelError('#VALUE!', '%s is not an integer' % str(year))

    if type(month) != int:
        return ExcelError('#VALUE!', '%s is not an integer' % str(month))

    if type(day) != int:
        return ExcelError('#VALUE!', '%s is not an integer' % str(day))

    if year < 0 or year > 9999:
        return ExcelError('#VALUE!', 'Year must be between 1 and 9999, instead %s' % str(year))

    if year < 1900:
        year = 1900 + year

    year, month, day = normalize_year(year, month, day) # taking into account negative month and day values

    date_0 = datetime.datetime(1900, 1, 1)
    date = datetime.datetime(year, month, day)

    result = (datetime.datetime(year, month, day) - date_0).days + 2

    if result <= 0:
        return ExcelError('#VALUE!', 'Date result is negative')
    else:
        return result


def yearfrac(start_date, end_date, basis=0):
    """
    Function to calculate the fraction of the year between two dates

    Excel reference: https://support.office.com/en-us/article/YEARFRAC-function-3844141e-c76d-4143-82b6-208454ddc6a8

    :param values: the payments of which at least one has to be negative.
    :param dates: the dates as excel dates (e.g. 43571 for 16/04/2019).
    :param guess: an initial guess which is required by Excel but isn't used by this function.
    :return: a float being the IRR.
    """

    def actual_nb_days_ISDA(start, end): # needed to separate days_in_leap_year from days_not_leap_year
        y1, m1, d1 = start
        y2, m2, d2 = end

        days_in_leap_year = 0
        days_not_in_leap_year = 0

        year_range = list(range(y1, y2 + 1))

        for y in year_range:

            if y == y1 and y == y2:
                nb_days = date(y2, m2, d2) - date(y1, m1, d1)
            elif y == y1:
                nb_days = date(y1 + 1, 1, 1) - date(y1, m1, d1)
            elif y == y2:
                nb_days = date(y2, m2, d2) - date(y2, 1, 1)
            else:
                nb_days = 366 if is_leap_year(y) else 365

            if is_leap_year(y):
                days_in_leap_year += nb_days
            else:
                days_not_in_leap_year += nb_days

        return (days_not_in_leap_year, days_in_leap_year)

    def actual_nb_days_AFB_alter(start, end):  # http://svn.finmath.net/finmath%20lib/trunk/src/main/java/net/finmath/time/daycount/DayCountConvention_ACT_ACT_YEARFRAC.java
        y1, m1, d1 = start
        y2, m2, d2 = end

        delta = date(*end) - date(*start)

        if delta <= 366:
            if is_leap_year(y1) and is_leap_year(y2):
                denom = 366
            elif is_leap_year(y1) and date(y1, m1, d1) <= date(y1, 2, 29):
                denom = 366
            elif is_leap_year(y2) and date(y2, m2, d2) >= date(y2, 2, 29):
                denom = 366
            else:
                denom = 365
        else:
            year_range = list(range(y1, y2 + 1))
            nb = 0

            for y in year_range:
                nb += 366 if is_leap_year(y) else 365

            denom = nb / len(year_range)

        return delta / denom

    if not is_number(start_date):
        return ExcelError('#VALUE!', 'start_date %s must be a number' % str(start_date))
    if not is_number(end_date):
        return ExcelError('#VALUE!', 'end_date %s must be number' % str(end_date))
    if start_date < 0:
        return ExcelError('#VALUE!', 'start_date %s must be positive' % str(start_date))
    if end_date < 0:
        return ExcelError('#VALUE!', 'end_date %s must be positive' % str(end_date))
    if not isinstance(basis, (int, float)):
        return ExcelError('#VALUE!', 'basis %s must be numeric' % str(basis))
    basis = int(basis)  # parse potential float to int
    if basis < 0 or basis > 4:
        return ExcelError('#NUM!', 'basis %s must be between 0 and 4' % str(basis))

    if start_date > end_date:  # switch dates if start_date > end_date
        temp = end_date
        end_date = start_date
        start_date = temp

    y1, m1, d1 = date_from_int(start_date)
    y2, m2, d2 = date_from_int(end_date)

    if basis == 0:  # US 30/360
        d2 = 30 if d2 == 31 and (d1 == 31 or d1 == 30) else min(d2, 31)
        d1 = 30 if d1 == 31 else d1

        count = 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)
        result = count / 360

    elif basis == 1:  # Actual/actual
        result = actual_nb_days_AFB_alter((y1, m1, d1), (y2, m2, d2))

    elif basis == 2:  # Actual/360
        result = (end_date - start_date) / 360

    elif basis == 3:  # Actual/365
        result = (end_date - start_date) / 365

    elif basis == 4:  # Eurobond 30/360
        d2 = 30 if d2 == 31 else d2
        d1 = 30 if d1 == 31 else d1

        count = 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)
        result = count / 360

    else:
        return ExcelError('#VALUE!', '%d must be 0, 1, 2, 3 or 4' % basis)


    return result


def isna(value):
    # This function might need more solid testing
    try:
        eval(value)
        return False
    except:
        return True


def isblank(value):
    return value is None


def istext(value):
    return type(value) == str


def offset(reference, rows, cols, height=None, width=None): # Excel reference: https://support.office.com/en-us/article/OFFSET-function-c8de19ae-dd79-4b9b-a14e-b4d906d11b66
    # This function accepts a list of addresses
    # Maybe think of passing a Range as first argument
    # x=Range(reference)
    # print(x)
    for i in [reference, rows, cols, height, width]:
        if isinstance(i, ExcelError) or i in ErrorCodes:
            return i

    rows = int(rows)
    cols = int(cols)

    # get first cell address of reference
    if is_range(reference):
        ref = resolve_range(reference, should_flatten = True)[0][0]
    else:
        ref = reference
    ref_sheet = ''
    end_address = ''

    if '!' in ref:
        ref_sheet = ref.split('!')[0] + '!'
        ref_cell = ref.split('!')[1]
    else:
        ref_cell = ref

    found = re.search(CELL_REF_RE, ref)
    new_col = col2num(found.group(1)) + cols
    new_row = int(found.group(2)) + rows

    if new_row <= 0 or new_col <= 0:
        return ExcelError('#VALUE!', 'Offset is out of bounds')

    start_address = str(num2col(new_col)) + str(new_row)

    if (height is not None and width is not None):
        if type(height) != int:
            return ExcelError('#VALUE!', '%d must not be integer' % height)
        if type(width) != int:
            return ExcelError('#VALUE!', '%d must not be integer' % width)

        if height > 0:
            end_row = new_row + height - 1
        else:
            return ExcelError('#VALUE!', '%d must be strictly positive' % height)
        if width > 0:
            end_col = new_col + width - 1
        else:
            return ExcelError('#VALUE!', '%d must be strictly positive' % width)

        end_address = ':' + str(num2col(end_col)) + str(end_row)
    elif height and not width or not height and width:
        return ExcelError('Height and width must be passed together')
    # print(cellmap)
    return ref_sheet + start_address + end_address

def product(*ranges):

    # values = extract_numeric_values(args)
    range_list = list(ranges)
    # print(range_list)
    if len(range_list) == 0:
        return 0
    vl=[]
    for r in range_list: # if a range has no values (i.e if it's empty)
        # print(r.values)
        # print(r.values)
        # print('check', r.values == 'None')
        for val in r.values:
            if val is None:
                # print('should get here')
                vl.append(0)
        # if r.values is None:
        #     print('should get here')
        #     vl.append(0)
        #     # print("zero")
            else:
                vl.append(val)
    # print(vl)
    return(np.prod(vl))


def sumproduct(*ranges): # Excel reference: https://support.office.com/en-us/article/SUMPRODUCT-function-16753e75-9f68-4874-94ac-4d2145a2fd2e
    range_list = list(ranges)

    for r in range_list: # if a range has no values (i.e if it's empty)
        if len(r.values) == 0:
            return 0

    for range in range_list:
        for item in range.values:
            # If there is an ExcelError inside a Range, sumproduct should output an ExcelError
            if isinstance(item, ExcelError):
                return ExcelError("#N/A", "ExcelErrors are present in the sumproduct items")

    reduce(check_length, range_list) # check that all ranges have the same size

    return reduce(lambda X, Y: X + Y, reduce(lambda x, y: Range.apply_all('multiply', x, y), range_list).values)


def iferror(value, value_if_error): # Excel reference: https://support.office.com/en-us/article/IFERROR-function-c526fd07-caeb-47b8-8bb6-63f3e417f611

    if isinstance(value, ExcelError) or value in ErrorCodes:
        # print("good")
        return value_if_error
    else:
        # print("fout")
        return value


def irr(values, guess = None):
    """
    Function to calculate the internal rate of return (IRR) using payments and periodic dates. It resembles the
    excel function IRR().

    Excel reference: https://support.office.com/en-us/article/IRR-function-64925eaa-9988-495b-b290-3ad0c163c1bc

    :param values: the payments of which at least one has to be negative.
    :param guess: an initial guess which is required by Excel but isn't used by this function.
    :return: a float being the IRR.
    """
    if isinstance(values, Range):
        values = values.values

    if is_not_number_input(values):
        return numeric_error(values, 'values')

    if guess is not None and guess != 0:
        raise ValueError('guess value for excellib.irr() is %s and not 0' % guess)
    else:
        try:
            return np.irr(values)
        except Exception as e:
            return ExcelError('#NUM!', e)


def xirr(values, dates, guess=0):
    """
    Function to calculate the internal rate of return (IRR) using payments and non-periodic dates. It resembles the
    excel function XIRR().

    Excel reference: https://support.office.com/en-ie/article/xirr-function-de1242ec-6477-445b-b11b-a303ad9adc9d

    :param values: the payments of which at least one has to be negative.
    :param dates: the dates as excel dates (e.g. 43571 for 16/04/2019).
    :param guess: an initial guess which is required by Excel but isn't used by this function.
    :return: a float being the IRR.
    """

    if isinstance(values, Range):
        values = values.values

    if all(value < 0 for value in values):
        return 0

    if isinstance(dates, Range):
        dates = dates.values

    if is_not_number_input(values):
        return numeric_error(values, 'values')

    if is_not_number_input(dates):
        return numeric_error(dates, 'dates')

    if guess is not None and guess != 0:
        raise ValueError('guess value for excellib.irr() is %s and not 0' % guess)
    else:
        try:
            try:
                return scipy.optimize.newton(lambda r: xnpv(r, values, dates, lim_rate_low=False, lim_rate_high=True), 0.0)
            except (RuntimeError, FloatingPointError, ExcelError):  # Failed to converge?
                return scipy.optimize.brentq(lambda r: xnpv(r, values, dates, lim_rate_low=False, lim_rate_high=True), -1.0, 1e5)
        except Exception:
            return ExcelError('#NUM', 'IRR did not converge.')

def ventilation(infiltration, natventin, natventout, mechventin, mechventout, ventbuiten, argIin, argIout, combin, combout,
                argIIin, argIIout, T_int_set, T_e, height, boundary_floor, year, A_g, month, tempmech, index):
    u_site = [3.04, 4.15, 2.99, 3.06, 2.97, 2.78, 2.63, 2.51, 2.71, 2.78, 2.83, 2.83]
    theta_e_argII = [0, 13.97, 13, 13.7, 14.56, 15.62, 16.17, 16.9, 15.11, 15.04, 13.43, 0]

    T_e_ref = 293
    rho_a_ref = 1.205
    g = 9.81
    T0 = 273
    n_lea = 0.67
    n_vent = 0.5
    n_comb = 0.5
    n_arg = 0.5

    output = []
    H_path_lea = []
    H_path_vent = []
    C_lea_path = []
    C_VentIn_path = []
    C_VentOut_path = []
    C_ArgIIn_path = []
    C_ArgIOut_path = []
    C_CombIn_path = []
    C_Mech = []
    C_p = [[], [], [], []]
    som_qm = [[], [], []]
    P_z_ref = [[], [], []]
    Pe_min = []
    Pe_max = []
    P_z_path_gem = []
    P_e_path_lea = []
    P_z_path = []
    P_e_path_vent = []
    delta_P = []
    qv_lea = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    qm = []
    qv_ventin = []
    qv_ventout = []
    qv_combin = []
    qv_argIin = []
    qv_argIout = []
    qv_ventmechin = [0, 0, 0]
    qv_ventmechout = []
    qv_combout = []
    qv_argIIin = []
    qv_argIIout = []

    month = int(month)
    # stopcriteria
    tol_som_qm = 0.9
    max_teller = 400  # maximaal aantal iteratieslagen
    sprong = 2

    # initialiseren tellers
    teller = [-1, -1, -1]
    teller_stap2 = [-1, -1, -1]
    teller_stap3 = [-1, -1, -1]

    # bepaling nauwkeurigheid
    qv_nauwkeurigheid = infiltration + ventbuiten + combin - combout + argIin + argIIin

    if qv_nauwkeurigheid > 1000:
        tol_som_qm = tol_som_qm * int(qv_nauwkeurigheid / 1000)
    # else:
    #     tol_som_qm = tol_som_qm

    c_lea = infiltration / (1 ** n_lea)
    # print("c_lea", c_lea)
    c_vent_in_req = natventin / (1 ** n_vent)
    # print("c_vent_in_req", c_vent_in_req)
    c_vent_out_req = abs(natventout / (1 ** n_vent))
    c_comb_in_req = combin / (1 ** n_comb)
    c_argI_in_req = argIin / (1 ** n_arg)
    c_argI_out_req = abs(argIout / (1 ** n_arg))
    # print("ventoreq, combinreq, argin, argout", c_vent_out_req,c_comb_in_req,c_argI_in_req,c_argI_out_req)

    if height < 15 and year < 1992 and boundary_floor == 2:
        domein = 1
    elif height < 15:
        domein = 2
    elif height < 50:
        domein = 3
    else:
        domein = 4

    if domein == 1:
        # H_path_lea[0][0] = 0.5 * height
        # H_path_lea[1][0] = 0.5 * height
        # H_path_lea[2][0] = height
        # H_path_lea[3][0] = 0
        H_path_lea.append([0.5 * height])
        H_path_lea.append([0.5 * height])
        H_path_lea.append([height])
        H_path_lea.append([0])

        # H_path_vent[0][0] = 0.5 * height
        # H_path_vent[1][0] = 0.5 * height
        # H_path_vent[2][0] = 0
        # H_path_vent[3][0] = 0
        H_path_vent.append([0.5 * height])
        H_path_vent.append([0.5 * height])
        H_path_vent.append([0])
        H_path_vent.append([0])

        # C_lea_path[0][0] = 0.35 * c_lea
        # C_lea_path[1][0] = 0.35 * c_lea
        # C_lea_path[2][0] = 0.15 * c_lea
        # C_lea_path[3][0] = 0.15 * c_lea
        C_lea_path.append([0.35 * c_lea])
        C_lea_path.append([0.35 * c_lea])
        C_lea_path.append([0.15 * c_lea])
        C_lea_path.append([0.15 * c_lea])

        # C_VentIn_path[0][0] = 0.5 * c_vent_in_req
        # C_VentIn_path[1][0] = 0.5 * c_vent_in_req
        # C_VentIn_path[2][0] = 0
        # C_VentIn_path[3][0] = 0
        C_VentIn_path.append([0.5 * c_vent_in_req])
        C_VentIn_path.append([0.5 * c_vent_in_req])
        C_VentIn_path.append([0])
        C_VentIn_path.append([0])

        # C_VentOut_path[0][0] = 0.5 * c_vent_out_req
        # C_VentOut_path[1][0] = 0.5 * c_vent_out_req
        # C_VentOut_path[2][0] = 0
        # C_VentOut_path[3][0] = 0
        C_VentOut_path.append([0.5 * c_vent_out_req])
        C_VentOut_path.append([0.5 * c_vent_out_req])
        C_VentOut_path.append([0])
        C_VentOut_path.append([0])

        # C_ArgIIn_path[0][0] = 0.5 * c_argI_in_req
        # C_ArgIIn_path[1][0] = 0.5 * c_argI_in_req
        # C_ArgIIn_path[2][0] = 0
        # C_ArgIIn_path[3][0] = 0
        C_ArgIIn_path.append([0.5 * c_argI_in_req])
        C_ArgIIn_path.append([0.5 * c_argI_in_req])
        C_ArgIIn_path.append([0])
        C_ArgIIn_path.append([0])

        # C_ArgIOut_path[0][0] = 0.5 * c_argI_out_req
        # C_ArgIOut_path[1][0] = 0.5 * c_argI_out_req
        # C_ArgIOut_path[2][0] = 0
        # C_ArgIOut_path[3][0] = 0
        C_ArgIOut_path.append([0.5 * c_argI_out_req])
        C_ArgIOut_path.append([0.5 * c_argI_out_req])
        C_ArgIOut_path.append([0])
        C_ArgIOut_path.append([0])

        # C_CombIn_path[0][0] = 0.5 * c_comb_in_req
        # C_CombIn_path[1][0] = 0.5 * c_comb_in_req
        # C_CombIn_path[2][0] = 0
        # C_CombIn_path[3][0] = 0
        C_CombIn_path.append([0.5 * c_comb_in_req])
        C_CombIn_path.append([0.5 * c_comb_in_req])
        C_CombIn_path.append([0])
        C_CombIn_path.append([0])

        # C_Mech[0] = 1
        C_Mech.append(1)

        aantal_gebouwschildelen = 4
        aantal_zones = 1

    elif domein == 2:
        # H_path_lea[0][0] = 0.5 * height
        # H_path_lea[1][0] = 0.5 * height
        # H_path_lea[2][0] = height
        H_path_lea.append([0.5 * height])
        H_path_lea.append([0.5 * height])
        H_path_lea.append([height])

        # H_path_vent[0][0] = 0.5 * height
        # H_path_vent[1][0] = 0.5 * height
        # H_path_vent[2][0] = 0
        H_path_vent.append([0.5 * height])
        H_path_vent.append([0.5 * height])
        H_path_vent.append([0])

        # C_lea_path[0][0] = 0.4 * c_lea
        # C_lea_path[1][0] = 0.4 * c_lea
        # C_lea_path[2][0] = 0.2 * c_lea
        C_lea_path.append([0.4 * c_lea])
        C_lea_path.append([0.4 * c_lea])
        C_lea_path.append([0.2 * c_lea])

        # C_VentIn_path[0][0] = 0.5 * c_vent_in_req
        # C_VentIn_path[1][0] = 0.5 * c_vent_in_req
        # C_VentIn_path[2][0] = 0
        C_VentIn_path.append([0.5 * c_vent_in_req])
        C_VentIn_path.append([0.5 * c_vent_in_req])
        C_VentIn_path.append([0])

        # C_VentOut_path[0][0] = 0.5 * c_vent_out_req
        # C_VentOut_path[1][0] = 0.5 * c_vent_out_req
        # C_VentOut_path[2][0] = 0
        C_VentOut_path.append([0.5 * c_vent_out_req])
        C_VentOut_path.append([0.5 * c_vent_out_req])
        C_VentOut_path.append([0])

        # C_ArgIIn_path[0][0] = 0.5 * c_argI_in_req
        # C_ArgIIn_path[1][0] = 0.5 * c_argI_in_req
        # C_ArgIIn_path[2][0] = 0
        C_ArgIIn_path.append([0.5 * c_argI_in_req])
        C_ArgIIn_path.append([0.5 * c_argI_in_req])
        C_ArgIIn_path.append([0])

        # C_ArgIOut_path[0][0] = 0.5 * c_argI_out_req
        # C_ArgIOut_path[1][0] = 0.5 * c_argI_out_req
        # C_ArgIOut_path[2][0] = 0
        C_ArgIOut_path.append([0.5 * c_argI_out_req])
        C_ArgIOut_path.append([0.5 * c_argI_out_req])
        C_ArgIOut_path.append([0])

        # C_CombIn_path[0][0] = 0.5 * c_comb_in_req
        # C_CombIn_path[1][0] = 0.5 * c_comb_in_req
        # C_CombIn_path[2][0] = 0
        C_CombIn_path.append([0.5 * c_comb_in_req])
        C_CombIn_path.append([0.5 * c_comb_in_req])
        C_CombIn_path.append([0])

        # C_Mech[0] = 1
        C_Mech.append(1)

        aantal_gebouwschildelen = 3
        aantal_zones = 1

    elif domein == 3:
        # H_path_lea[0][0] = 7.5
        # H_path_lea[1][0] = 7.5
        #
        # H_path_lea[0][1] = 15 + (height - 15) / 2
        # H_path_lea[1][1] = 15 + (height - 15) / 2
        H_path_lea.append([7.5])
        H_path_lea.append([7.5])
        H_path_lea[0].append(15 + (height - 15) / 2)
        H_path_lea[1].append(15 + (height - 15) / 2)

        # H_path_vent[0][0] = 7.5
        # H_path_vent[1][0] = 7.5
        # H_path_vent[0][1] = 15 + (height - 15) / 2
        # H_path_vent[1][1] = 15 + (height - 15) / 2
        H_path_vent.append([7.5])
        H_path_vent.append([7.5])
        H_path_vent[0].append(15 + (height - 15) / 2)
        H_path_vent[1].append(15 + (height - 15) / 2)

        # C_lea_path[0][0] = 0.5 * 15 / height * c_lea
        # C_lea_path[1][0] = 0.5 * 15 / height * c_lea
        # C_lea_path[0][1] = 0.5 * c_lea - C_lea_path[0][0]
        # C_lea_path[1][1] = 0.5 * c_lea - C_lea_path[1][0]
        C_lea_path.append([0.5 * 15 / height * c_lea])
        C_lea_path.append([0.5 * 15 / height * c_lea])
        C_lea_path[0].append(0.5 * c_lea - C_lea_path[0][0])
        C_lea_path[1].append(0.5 * c_lea - C_lea_path[1][0])

        # C_VentIn_path[0][0] = 0.5 * (15 / height) * c_vent_in_req
        # C_VentIn_path[1][0] = 0.5 * (15 / height) * c_vent_in_req
        # C_VentIn_path[0][1] = 0.5 * c_vent_in_req - C_VentIn_path[0][0]
        # C_VentIn_path[1][1] = 0.5 * c_vent_in_req - C_VentIn_path[1][0]
        C_VentIn_path.append([0.5 * (15 / height) * c_vent_in_req])
        C_VentIn_path.append([0.5 * (15 / height) * c_vent_in_req])
        C_VentIn_path[0].append(0.5 * c_vent_in_req - C_VentIn_path[0][0])
        C_VentIn_path[1].append(0.5 * c_vent_in_req - C_VentIn_path[1][0])

        # C_VentOut_path[0][0] = 0.5 * (15 / height) * c_vent_out_req
        # C_VentOut_path[1][0] = 0.5 * (15 / height) * c_vent_out_req
        # C_VentOut_path[0][1] = 0.5 * c_vent_out_req - C_VentOut_path[0][0]
        # C_VentOut_path[1][1] = 0.5 * c_vent_out_req - C_VentOut_path[1][0]
        C_VentOut_path.append([0.5 * (15 / height) * c_vent_out_req])
        C_VentOut_path.append([0.5 * (15 / height) * c_vent_out_req])
        C_VentOut_path[0].append(0.5 * c_vent_out_req - C_VentOut_path[0][0])
        C_VentOut_path[1].append(0.5 * c_vent_out_req - C_VentOut_path[1][0])

        # C_ArgIIn_path[0][0] = 0.5 * (15 / height) * c_argI_in_req
        # C_ArgIIn_path[1][0] = 0.5 * (15 / height) * c_argI_in_req
        # C_ArgIIn_path[0][1] = 0.5 * c_argI_in_req - C_ArgIIn_path[0][0]
        # C_ArgIIn_path[1][1] = 0.5 * c_argI_in_req - C_ArgIIn_path[1][0]
        C_ArgIIn_path.append([0.5 * (15 / height) * c_argI_in_req])
        C_ArgIIn_path.append([0.5 * (15 / height) * c_argI_in_req])
        C_ArgIIn_path[0].append(0.5 * c_argI_in_req - C_ArgIIn_path[0][0])
        C_ArgIIn_path[1].append(0.5 * c_argI_in_req - C_ArgIIn_path[1][0])

        # C_ArgIOut_path[0][0] = 0.5 * (15 / height) * c_argI_out_req
        # C_ArgIOut_path[1][0] = 0.5 * (15 / height) * c_argI_out_req
        # C_ArgIOut_path[0][1] = 0.5 * c_argI_out_req - C_ArgIOut_path[0][0]
        # C_ArgIOut_path[1][1] = 0.5 * c_argI_out_req - C_ArgIOut_path[1][0]
        C_ArgIOut_path.append([0.5 * (15 / height) * c_argI_out_req])
        C_ArgIOut_path.append([0.5 * (15 / height) * c_argI_out_req])
        C_ArgIOut_path[0].append(0.5 * c_argI_out_req - C_ArgIOut_path[0][0])
        C_ArgIOut_path[1].append(0.5 * c_argI_out_req - C_ArgIOut_path[1][0])

        # C_CombIn_path[0][0] = 0.5 * (15 / height) * c_comb_in_req
        # C_CombIn_path[1][0] = 0.5 * (15 / height) * c_comb_in_req
        # C_CombIn_path[0][1] = 0.5 * c_comb_in_req - C_CombIn_path[0][0]
        # C_CombIn_path[1][1] = 0.5 * c_comb_in_req - C_CombIn_path[1][0]
        C_CombIn_path.append([0.5 * (15 / height) * c_comb_in_req])
        C_CombIn_path.append([0.5 * (15 / height) * c_comb_in_req])
        C_CombIn_path[0].append(0.5 * c_comb_in_req - C_CombIn_path[0][0])
        C_CombIn_path[1].append(0.5 * c_comb_in_req - C_CombIn_path[1][0])

        # C_Mech[0] = 15 / height
        # C_Mech[1] = (height - 15) / height
        C_Mech.append(15 / height)
        C_Mech.append((height - 15) / height)

        aantal_gebouwschildelen = 2
        aantal_zones = 2

    elif domein == 4:
        # H_path_lea[0][0] = 7.5
        # H_path_lea[1][0] = 7.5
        # H_path_lea[0][1] = 32.5
        # H_path_lea[1][1] = 32.5
        # H_path_lea[0][2] = 50 + (height - 50) / 2
        # H_path_lea[1][2] = 50 + (height - 50) / 2
        H_path_lea.append([7.5])
        H_path_lea.append([7.5])
        H_path_lea[0].append(32.5)
        H_path_lea[1].append(32.5)
        H_path_lea[0].append(50 + (height - 50) / 2)
        H_path_lea[1].append(50 + (height - 50) / 2)

        # H_path_vent[0][0] = 7.5
        # H_path_vent[1][0] = 7.5
        # H_path_vent[0][1] = 32.5
        # H_path_vent[1][1] = 32.5
        # H_path_vent[0][2] = 50 + (height - 50) / 2
        # H_path_vent[1][2] = 50 + (height - 50) / 2
        H_path_vent.append([7.5])
        H_path_vent.append([7.5])
        H_path_vent[0].append(32.5)
        H_path_vent[1].append(32.5)
        H_path_vent[0].append(50 + (height - 50) / 2)
        H_path_vent[1].append(50 + (height - 50) / 2)

        # C_lea_path[0][0] = 0.5 * 15 / height * c_lea
        # C_lea_path[1][0] = 0.5 * 15 / height * c_lea
        # C_lea_path[0][1] = 0.5 * 35 / height * c_lea
        # C_lea_path[1][1] = 0.5 * 35 / height * c_lea
        # C_lea_path[0][2] = 0.5 * c_lea - C_lea_path[0][0] - C_lea_path[0][1]
        # C_lea_path[1][2] = 0.5 * c_lea - C_lea_path[1][0] - C_lea_path[1][1]
        C_lea_path.append([0.5 * 15 / height * c_lea])
        C_lea_path.append([0.5 * 15 / height * c_lea])
        C_lea_path[0].append(0.5 * 35 / height * c_lea)
        C_lea_path[1].append(0.5 * 35 / height * c_lea)
        C_lea_path[0].append(0.5 * c_lea - C_lea_path[0][0] - C_lea_path[0][1])
        C_lea_path[1].append(0.5 * c_lea - C_lea_path[1][0] - C_lea_path[1][1])

        # C_VentIn_path[0][0] = 0.5 * (15 / height) * c_vent_in_req
        # C_VentIn_path[1][0] = 0.5 * (15 / height) * c_vent_in_req
        # C_VentIn_path[0][1] = 0.5 * (35 / height) * c_vent_in_req
        # C_VentIn_path[1][1] = 0.5 * (35 / height) * c_vent_in_req
        # C_VentIn_path[0][2] = 0.5 * c_vent_in_req - C_VentIn_path[0][0] - C_VentIn_path[0][1]
        # C_VentIn_path[1][2] = 0.5 * c_vent_in_req - C_VentIn_path[1][0] - C_VentIn_path[1][1]
        C_VentIn_path.append([0.5 * (15 / height) * c_vent_in_req])
        C_VentIn_path.append([0.5 * (15 / height) * c_vent_in_req])
        C_VentIn_path[0].append(0.5 * (35 / height) * c_vent_in_req)
        C_VentIn_path[1].append(0.5 * (35 / height) * c_vent_in_req)
        C_VentIn_path[0].append(0.5 * c_vent_in_req - C_VentIn_path[0][0] - C_VentIn_path[0][1])
        C_VentIn_path[1].append(0.5 * c_vent_in_req - C_VentIn_path[1][0] - C_VentIn_path[1][1])

        # C_VentOut_path[0][0] = 0.5 * (15 / height) * c_vent_out_req
        # C_VentOut_path[1][0] = 0.5 * (15 / height) * c_vent_out_req
        # C_VentOut_path[0][1] = 0.5 * (35 / height) * c_vent_out_req
        # C_VentOut_path[1][1] = 0.5 * (35 / height) * c_vent_out_req
        # C_VentOut_path[0][2] = 0.5 * c_vent_out_req - C_VentOut_path[0][0] - C_VentOut_path[0][1]
        # C_VentOut_path[1][2] = 0.5 * c_vent_out_req - C_VentOut_path[1][0] - C_VentOut_path[1][1]
        C_VentOut_path.append([0.5 * (15 / height) * c_vent_out_req])
        C_VentOut_path.append([0.5 * (15 / height) * c_vent_out_req])
        C_VentOut_path[0].append(0.5 * (35 / height) * c_vent_out_req)
        C_VentOut_path[1].append(0.5 * (35 / height) * c_vent_out_req)
        C_VentOut_path[0].append(0.5 * c_vent_out_req - C_VentOut_path[0][0] - C_VentOut_path[0][1])
        C_VentOut_path[1].append(0.5 * c_vent_out_req - C_VentOut_path[1][0] - C_VentOut_path[1][1])

        # C_ArgIIn_path[0][0] = 0.5 * (15 / height) * c_argI_in_req
        # C_ArgIIn_path[1][0] = 0.5 * (15 / height) * c_argI_in_req
        # C_ArgIIn_path[0][1] = 0.5 * (35 / height) * c_argI_in_req
        # C_ArgIIn_path[1][1] = 0.5 * (35 / height) * c_argI_in_req
        # C_ArgIIn_path[0][2] = 0.5 * c_argI_in_req - C_ArgIIn_path[0][0] - C_ArgIIn_path[0][1]
        # C_ArgIIn_path[1][2] = 0.5 * c_argI_in_req - C_ArgIIn_path[1][0] - C_ArgIIn_path[1][1]
        C_ArgIIn_path.append([0.5 * (15 / height) * c_argI_in_req])
        C_ArgIIn_path.append([0.5 * (15 / height) * c_argI_in_req])
        C_ArgIIn_path[0].append(0.5 * (35 / height) * c_argI_in_req)
        C_ArgIIn_path[1].append(0.5 * (35 / height) * c_argI_in_req)
        C_ArgIIn_path[0].append(0.5 * c_argI_in_req - C_ArgIIn_path[0][0] - C_ArgIIn_path[0][1])
        C_ArgIIn_path[1].append(0.5 * c_argI_in_req - C_ArgIIn_path[1][0] - C_ArgIIn_path[1][1])

        # C_ArgIOut_path[0][0] = 0.5 * (15 / height) * c_argI_out_req
        # C_ArgIOut_path[1][0] = 0.5 * (15 / height) * c_argI_out_req
        # C_ArgIOut_path[0][1] = 0.5 * (35 / height) * c_argI_out_req
        # C_ArgIOut_path[1][1] = 0.5 * (35 / height) * c_argI_out_req
        # C_ArgIOut_path[0][2] = 0.5 * c_argI_out_req - C_ArgIOut_path[0][0] - C_ArgIOut_path[0][1]
        # C_ArgIOut_path[1][2] = 0.5 * c_argI_out_req - C_ArgIOut_path[1][0] - C_ArgIOut_path[1][1]
        C_ArgIOut_path.append([0.5 * (15 / height) * c_argI_out_req])
        C_ArgIOut_path.append([0.5 * (15 / height) * c_argI_out_req])
        C_ArgIOut_path[0].append(0.5 * (35 / height) * c_argI_out_req)
        C_ArgIOut_path[1].append(0.5 * (35 / height) * c_argI_out_req)
        C_ArgIOut_path[0].append(0.5 * c_argI_out_req - C_ArgIOut_path[0][0] - C_ArgIOut_path[0][1])
        C_ArgIOut_path[1].append(0.5 * c_argI_out_req - C_ArgIOut_path[1][0] - C_ArgIOut_path[1][1])

        # C_CombIn_path[0][0] = 0.5 * (15 / height) * c_comb_in_req
        # C_CombIn_path[1][0] = 0.5 * (15 / height) * c_comb_in_req
        # C_CombIn_path[0][1] = 0.5 * (35 / height) * c_comb_in_req
        # C_CombIn_path[1][1] = 0.5 * (35 / height) * c_comb_in_req
        # C_CombIn_path[0][2] = 0.5 * c_comb_in_req - C_CombIn_path[0][0] - C_CombIn_path[0][1]
        # C_CombIn_path[1][2] = 0.5 * c_comb_in_req - C_CombIn_path[1][0] - C_CombIn_path[1][1]
        C_CombIn_path.append([0.5 * (15 / height) * c_comb_in_req])
        C_CombIn_path.append([0.5 * (15 / height) * c_comb_in_req])
        C_CombIn_path[0].append(0.5 * (35 / height) * c_comb_in_req)
        C_CombIn_path[1].append(0.5 * (35 / height) * c_comb_in_req)
        C_CombIn_path[0].append(0.5 * c_comb_in_req - C_CombIn_path[0][0] - C_CombIn_path[0][1])
        C_CombIn_path[1].append(0.5 * c_comb_in_req - C_CombIn_path[1][0] - C_CombIn_path[1][1])

        # C_Mech[0] = 15 / height
        # C_Mech[1] = 35 / height
        # C_Mech[2] = (height - 50) / height
        C_Mech.append(15 / height)
        C_Mech.append(35 / height)
        C_Mech.append((height - 50) / height)

        aantal_gebouwschildelen = 2
        aantal_zones = 3

    for i in range(aantal_zones):
        if H_path_lea[0][i] >= 50:
            C_p[0].append(0.8)
            C_p[1].append(-0.7)
            C_p[2].append(-0.7)
            C_p[3].append(0)
        elif H_path_lea[0][i] < 15:
            C_p[0].append(0.25)
            C_p[1].append(-0.5)
            C_p[2].append(-0.6)
            C_p[3].append(-0.2)
        else:
            C_p[0].append(0.45)
            C_p[1].append(-0.5)
            C_p[2].append(-0.6)
            C_p[3].append(0)

    som_qm[1] = 0
    som_qm[2] = 0
    P_z_ref[1] = 0
    P_z_ref[2] = 0
    # print(som_qm)
    # print(P_z_ref)

    rho_a_e = rho_a_ref * T_e_ref / (T_e + T0)
    # luchtdichtheid in de zone (=binnen):
    rho_a_z = rho_a_ref * T_e_ref / (T_int_set + T0)
    # gemiddelde luchtdichtheid:
    rho_a_gem = (rho_a_e + rho_a_z) / 2

    # luchtdichtheid mechanische toevoer
    rho_a_mech = rho_a_ref * T_e_ref / (tempmech + T0)

    # luchtdichtheid zomernachtventilatie
    rho_a_argII = rho_a_ref * T_e_ref / (theta_e_argII[month - 1] + T0)
    # print(aantal_zones, aantal_gebouwschildelen)

    # print(rho_a_e, rho_a_z, rho_a_gem, rho_a_mech, rho_a_argII)

    for k in range(aantal_gebouwschildelen):
        P_e_path_lea.append([])
        P_e_path_vent.append([])
        P_z_path.append([])
        delta_P.append([])
        # qv_lea.append([])
        # C_lea_path.append([])
        qm.append([])
        qv_ventin.append([])
        qv_ventout.append([])
        # qv_ventmechin.append([])
        # qv_ventmechout.append([])
        C_VentIn_path.append([])
        qv_combin.append([])
        # qv_combout.append([])
        C_CombIn_path.append([])
        qv_argIin.append([])
        C_ArgIIn_path.append([])
        C_ArgIOut_path.append([])
        qv_argIout.append([])
        # qv_argIIin.append([])
        # qv_argIIout.append([])
        for j in range(aantal_zones):
            P_e_path_lea[k].append(0)
            P_e_path_vent[k].append(0)
            P_z_path[k].append(0)
            delta_P[k].append(0)
            # qv_lea[k].append(0)
            # C_lea_path[k].append(0)
            qm[k].append(0)
            qv_ventin[k].append(0)
            qv_ventout[k].append(0)
            # qv_ventmechin[k].append(0)
            # qv_ventmechout[k].append(0)
            C_VentIn_path[k].append(0)
            qv_combin[k].append(0)
            # qv_combout[k].append(0)
            C_CombIn_path[k].append(0)
            qv_argIin[k].append(0)
            C_ArgIIn_path[k].append(0)
            C_ArgIOut_path[k].append(0)
            qv_argIout[k].append(0)
            # qv_argIIin[k].append(0)
            # qv_argIIout[k].append(0)

    for j in range(aantal_zones):
        # qv_ventmechin.append([])
        qv_ventmechout.append([])
        qv_combout.append([])
        qv_argIIin.append([])
        qv_argIIout.append([])

    for j in range(aantal_zones):
        P_z_ref[j] = 0
        Pe_min.append(1000)
        Pe_max.append(-1000)
        P_z_path_gem.append(0)

        for k in range(aantal_gebouwschildelen):
            P_e_path_lea[k][j] = rho_a_e * (0.5 * C_p[k][j] * (u_site[month - 1] ** 2) - H_path_lea[k][j] * g)
            # print(P_e_path_lea[k])
            if P_e_path_lea[k][j] > Pe_max[j]:
                Pe_max[j] = P_e_path_lea[k][j]
            if P_e_path_lea[k][j] < Pe_min[j]:
                Pe_min[j] = P_e_path_lea[k][j]
            if H_path_vent[k][j] != 0:
                P_e_path_vent[k][j] = rho_a_e * (0.5 * C_p[k][j] * (u_site[month - 1] ** 2) - H_path_vent[k][j] * g)
                if P_e_path_vent[k][j] > Pe_max[j]:
                    Pe_max[j] = P_e_path_vent[k][j]
                if P_e_path_vent[k][j] < Pe_min[j]:
                    Pe_min[j] = P_e_path_vent[k][j]
            # print(k, Pe_max, Pe_min)
        P_z_path_gem[j] = (Pe_min[j] + Pe_max[j]) / 2
        P_z_ref[j] = P_z_path_gem[j] + rho_a_z * H_path_lea[0][j] * g

        teller[j] = 0
        teller_stap2[j] = 0
        teller_stap3[j] = 0
        bisectiestap = 1
        doorgaan = True

        while doorgaan:
            som_qm[j] = 0

            for k in range(aantal_gebouwschildelen):
                # 1 infiltratie
                P_z_path[k][j] = P_z_ref[j] - rho_a_z * H_path_lea[k][j] * g
                delta_P[k][j] = P_e_path_lea[k][j] - P_z_path[k][j]

                if delta_P[k][j] > 0:
                    qv_lea[k][j] = C_lea_path[k][j] * abs(delta_P[k][j]) ** n_lea
                    qm[k][j] = rho_a_e * qv_lea[k][j]
                else:
                    qv_lea[k][j] = -C_lea_path[k][j] * abs(delta_P[k][j]) ** n_lea
                    qm[k][j] = rho_a_z * qv_lea[k][j]

                som_qm[j] = som_qm[j] + qm[k][j]

                # 2 natuurlijke ventialtie
                P_z_path[k][j] = P_z_ref[j] - rho_a_z * H_path_vent[k][j] * g
                delta_P[k][j] = P_e_path_vent[k][j] - P_z_path[k][j]

                if delta_P[k][j] > 0:
                    qv_ventin[k][j] = C_VentIn_path[k][j] * abs(delta_P[k][j]) ** n_vent
                    qm[k][j] = rho_a_e * qv_ventin[k][j]
                    som_qm[j] = som_qm[j] + qm[k][j]

                    qv_ventin[k][j] = C_VentOut_path[k][j] * abs(delta_P[k][j]) ** n_vent
                    qm[k][j] = rho_a_e * qv_ventin[k][j]
                    som_qm[j] = som_qm[j] + qm[k][j]
                else:
                    qv_ventout[k][j] = -C_VentIn_path[k][j] * abs(delta_P[k][j]) ** n_vent
                    qm[k][j] = rho_a_z * qv_ventout[k][j]
                    som_qm[j] = som_qm[j] + qm[k][j]

                    qv_ventout[k][j] = -C_VentOut_path[k][j] * abs(delta_P[k][j]) ** n_vent
                    qm[k][j] = rho_a_z * qv_ventout[k][j]
                    som_qm[j] = som_qm[j] + qm[k][j]

                # 3 verbrandingslucht ingaand
                P_z_path[k][j] = P_z_ref[j] - rho_a_z * H_path_vent[k][j] * g
                delta_P[k][j] = P_e_path_vent[k][j] - P_z_path[k][j]

                if delta_P[k][j] > 0:
                    qv_combin[k][j] = C_CombIn_path[k][j] * abs(delta_P[k][j]) ** n_comb
                    qm[k][j] = rho_a_e * qv_combin[k][j]
                    som_qm[j] = som_qm[j] + qm[k][j]
                else:
                    qv_combin[k][j] = -C_CombIn_path[k][j] * abs(delta_P[k][j]) ** n_comb
                    qm[k][j] = rho_a_z * qv_combin[k][j]
                    som_qm[j] = som_qm[j] + qm[k][j]

                # spui ingaand
                P_z_path[k][j] = P_z_ref[j] - rho_a_z * H_path_vent[k][j] * g
                delta_P[k][j] = P_e_path_vent[k][j] - P_z_path[k][j]

                if delta_P[k][j] > 0:
                    qv_argIin[k][j] = C_ArgIIn_path[k][j] * abs(delta_P[k][j]) ** n_arg
                    qm[k][j] = rho_a_e * qv_argIin[k][j]
                    som_qm[j] = som_qm[j] + qm[k][j]

                    qv_argIin[k][j] = C_ArgIOut_path[k][j] * abs(delta_P[k][j]) ** n_arg
                    qm[k][j] = rho_a_e * qv_argIin[k][j]
                    som_qm[j] = som_qm[j] + qm[k][j]
                else:
                    qv_argIout[k][j] = -C_ArgIIn_path[k][j] * abs(delta_P[k][j]) ** n_arg
                    qm[k][j] = rho_a_z * qv_argIout[k][j]
                    som_qm[j] = som_qm[j] + qm[k][j]

                    qv_argIout[k][j] = -C_ArgIOut_path[k][j] * abs(delta_P[k][j]) ** n_arg
                    qm[k][j] = rho_a_z * qv_argIout[k][j]
                    som_qm[j] = som_qm[j] + qm[k][j]

            k = 1
            # print(C_Mech[j])
            # print(mechventin)
            # print(C_Mech[j] * mechventin)
            # if mechventin == 0:
            #     qv_ventmechin[j] = 0
            # else:
            qv_ventmechin[j] = (C_Mech[j] * mechventin)
            # print(qv_ventmechin[j])
            if qv_ventmechin[j] > 0:
                qm[k][j] = rho_a_mech * qv_ventmechin[j]
            else:
                qm[k][j] = rho_a_z * qv_ventmechin[j]
            som_qm[j] = som_qm[j] + qm[k][j]

            # 8 mechanische ventilatie uitgaand
            # print("mventout", mechventout)
            # print(C_Mech, C_Mech[j])
            qv_ventmechout[j] = C_Mech[j] * mechventout
            if qv_ventmechout[j] > 0:
                qm[k][j] = rho_a_mech * qv_ventmechout[j]
            else:
                qm[k][j] = rho_a_z * qv_ventmechout[j]
            som_qm[j] = som_qm[j] + qm[k][j]

            # 9 verbrandingslucht uitgaand
            qv_combout[j] = C_Mech[j] * combout
            if qv_combout[j] > 0:
                qm[k][j] = rho_a_e * qv_combout[j]
            else:
                qm[k][j] = rho_a_z * qv_combout[j]
            som_qm[j] = som_qm[j] + qm[k][j]

            # 10 zomernachtventilatie ingaand
            qv_argIIin[j] = C_Mech[j] * argIIin
            if qv_argIIin[j] > 0:
                qm[k][j] = rho_a_argII * qv_argIIin[j]
            else:
                qm[k][j] = rho_a_z * qv_argIIin[j]
            som_qm[j] = som_qm[j] + qm[k][j]

            # 11 zomernachtventilatie uitgaand
            qv_argIIout[j] = C_Mech[j] * argIIout
            if qv_argIIout[j] > 0:
                qm[k][j] = rho_a_argII * qv_argIIout[j]
            else:
                qm[k][j] = rho_a_z * qv_argIIout[j]
            som_qm[j] = som_qm[j] + qm[k][j]

            if som_qm[j] == 0:
                doorgaan = False

            if bisectiestap == 1:
                P_z_ref_a = P_z_ref[j]
                som_qm_a = som_qm[j]
                if abs(som_qm_a) <= tol_som_qm * 1:
                    doorgaan = False
                else:
                    bisectiestap = 2
                    P_z_ref[j] = P_z_ref_a + sprong
            elif bisectiestap == 2:
                P_z_ref_b = P_z_ref[j]
                som_qm_b = som_qm[j]

                teller_stap2[j] = teller_stap2[j] + 1
                if abs(som_qm_b) <= tol_som_qm * 1:
                    doorgaan = False
                else:
                    if math.copysign(1, som_qm_a) != math.copysign(1, som_qm_b):
                        bisectiestap = 3
                        P_z_ref[j] = (P_z_ref_a + P_z_ref_b) / 2
                    else:
                        bisectiestap = 2
                        richting = math.copysign(1, P_z_ref_b - P_z_ref_a) * math.copysign(1, som_qm_b - som_qm_a)
                        if abs(som_qm_a) > abs(som_qm_b):
                            P_z_ref_a = P_z_ref_b
                            som_qm_a = som_qm_b
                        richting = math.copysign(1, som_qm_a) * richting
                        if richting == 0:
                            richting = 1
                        P_z_ref[j] = P_z_ref_a - sprong * richting

            elif bisectiestap == 3:
                P_z_ref_c = P_z_ref[j]
                som_qm_c = som_qm[j]

                teller_stap3[j] = teller_stap3[j] + 1

                if abs(som_qm_c) <= tol_som_qm * 1:
                    doorgaan = False
                else:
                    bisectiestap = 3
                    if math.copysign(1, som_qm_c) == math.copysign(1, som_qm_a):
                        P_z_ref_a = P_z_ref_c
                        som_qm_a = som_qm_c
                    else:
                        P_z_ref_b = P_z_ref_c
                        som_qm_b = som_qm_c
                    P_z_ref[j] = (P_z_ref_a + P_z_ref_b) / 2

            teller[j] = teller[j] + 1
            if teller[j] > max_teller:
                output[0] = "fout"
                output[1] = "fout"
                output[2] = "fout"
                output[3] = "fout"
                output[4] = "fout"
                output[5] = "fout"
                output[6] = "fout"
                output[7] = P_z_ref[0]
                output[8] = P_z_ref[1]
                output[9] = P_z_ref[2]
                output[10] = som_qm[0]
                output[11] = som_qm[1]
                output[12] = som_qm[2]
                output[13] = teller[0]
                output[14] = teller_stap2[0]
                output[15] = teller_stap2[1]
                output[16] = teller_stap2[2]
                output[17] = teller_stap3[0]
                output[18] = teller_stap3[1]
                output[19] = teller_stap3[2]
                break

    # print(Pe_min, Pe_max)
    qv_eff_lea_in = 0
    qv_eff_lea_out = 0
    qv_eff_vent_in = 0
    qv_eff_vent_out = 0
    qv_eff_comb_in = 0
    qv_eff_argI_in = 0
    qv_eff_argI_out = 0

    for j in range(aantal_zones):
        for k in range(aantal_gebouwschildelen):
            # infiltratie
            P_z_path[k][j] = P_z_ref[j] - rho_a_z * H_path_lea[k][j] * g
            delta_P[k][j] = P_e_path_lea[k][j] - P_z_path[k][j]
            qv_lea[k][j] = C_lea_path[k][j] * abs(delta_P[k][j]) ** n_lea

            # infiltratie in
            if delta_P[k][j] > 0:
                qv_eff_lea_in = qv_eff_lea_in + qv_lea[k][j]
            else:
                qv_eff_lea_out = qv_eff_lea_out - qv_lea[k][j]

            # natuurlijke ventilatie
            P_z_path[k][j] = P_z_ref[j] - rho_a_z * H_path_vent[k][j] * g
            delta_P[k][j] = P_e_path_vent[k][j] - P_z_path[k][j]
            if delta_P[k][j] > 0:
                qv_ventin[k][j] = C_VentIn_path[k][j] * abs(delta_P[k][j]) ** n_vent
                qv_eff_vent_in = qv_eff_vent_in + qv_ventin[k][j]

                qv_ventin[k][j] = C_VentOut_path[k][j] * abs(delta_P[k][j]) ** n_vent
                qv_eff_vent_in = qv_eff_vent_in + qv_ventin[k][j]
            else:
                qv_ventout[k][j] = -C_VentIn_path[k][j] * abs(delta_P[k][j]) ** n_vent
                qv_eff_vent_out = qv_eff_vent_out + qv_ventout[k][j]

                qv_ventout[k][j] = -C_VentOut_path[k][j] * abs(delta_P[k][j]) ** n_vent
                qv_eff_vent_out = qv_eff_vent_out + qv_ventout[k][j]

            # verbrandingsluchtventilatie in
            qv_combin[k][j] = C_CombIn_path[k][j] * abs(delta_P[k][j]) ** n_comb
            if delta_P[k][j] > 0:
                qv_eff_comb_in = qv_eff_comb_in + qv_combin[k][j]

            # spuiventilatie
            if delta_P[k][j] > 0:
                qv_argIin[k][j] = C_ArgIIn_path[k][j] * abs(delta_P[k][j]) ** n_arg
                qv_eff_argI_in = qv_eff_argI_in + qv_argIin[k][j]

                qv_argIin[k][j] = C_ArgIOut_path[k][j] * abs(delta_P[k][j]) ** n_arg
                qv_eff_argI_in = qv_eff_argI_in + qv_argIin[k][j]
            else:
                qv_argIout[k][j] = -C_ArgIIn_path[k][j] * abs(delta_P[k][j]) ** n_arg
                qv_eff_argI_out = qv_eff_argI_out + qv_argIout[k][j]

                qv_argIout[k][j] = -C_ArgIOut_path[k][j] * abs(delta_P[k][j]) ** n_arg
                qv_eff_argI_out = qv_eff_argI_out + qv_argIout[k][j]

    # print(qv_lea)
    index = int(index)
    output.append(qv_eff_lea_in)
    output.append(qv_eff_vent_in)
    output.append(qv_eff_argI_in)
    output.append(qv_eff_comb_in)
    output.append(qv_eff_lea_out)
    output.append(qv_eff_vent_out)
    output.append(qv_eff_argI_out)
    output.append(P_z_ref[0])
    output.append(P_z_ref[1])
    output.append(P_z_ref[2])
    output.append(som_qm[0])
    output.append(som_qm[1])
    output.append(som_qm[2])
    output.append(teller[0])
    output.append(teller_stap2[0])
    output.append(teller_stap2[1])
    output.append(teller_stap2[2])
    output.append(teller_stap3[0])
    output.append(teller_stap3[1])
    output.append(teller_stap3[2])
    output.append(qv_lea[0][0])
    output.append(qv_lea[1][0])
    output.append(qv_lea[2][0])
    output.append(qv_ventin[0][0])
    output.append(qv_ventin[1][0])
    output.append(qv_ventout[0][0])
    output.append(qv_ventout[1][0])
    return output[index-1]

def hlookup(lookup_value, table_array, row_index_num, range_lookup = True): # https://support.office.com/en-us/article/VLOOKUP-function-0bbc8083-26fe-4963-8ab8-93a18ad188a1

    if not isinstance(table_array, Range):
        return ExcelError('#VALUE', 'table_array should be a Range')

    if row_index_num > table_array.nrows:
        return ExcelError('#VALUE', 'row_index_num is greater than the number of cols in table_array')
    # tablelst=list(table_array)
    # print(tablelst[0])
    # print(table_array.ncols)
    cols = table_array.ncols
    first_row = list(table_array.values)[0:cols]
    # first_row = table_array.get(1,0)
    # print(first_row)
    # result_row = list(table_array.values)[7:14]
    result_row = list(table_array.values)[(row_index_num-1) * cols:(row_index_num) * cols]
    # print(result_row)
    if not range_lookup:
        if lookup_value not in first_row:
            return ExcelError('#N/A', 'lookup_value not in first row of table_array')
        else:
            i = first_row.index(lookup_value)
            ref = first_row.order[i]
    else:
        i = None
        for j,v in enumerate(first_row):
            # print(v)
            if lookup_value >= v:
                i=j
                # i = first_row.index(v)
                # print('i',i)
                ref = first_row[i]
            else:
                break
        # print(i)
        if i is None:
            # print("true")
            return ExcelError('#N/A', 'lookup_value smaller than all values of table_array')
    # print('ref', ref)
    # print('idef', i)
    # print(result_row[i])
    return result_row[i]

# def vlookup(lookup_value, table_array, col_index_num, range_lookup = True): # https://support.office.com/en-us/article/VLOOKUP-function-0bbc8083-26fe-4963-8ab8-93a18ad188a1
#
#     if not isinstance(table_array, Range):
#         return ExcelError('#VALUE', 'table_array should be a Range')
#
#     if col_index_num > table_array.ncols:
#         return ExcelError('#VALUE', 'row_index_num is greater than the number of cols in table_array')
#     # tablelst=list(table_array)
#     # print(tablelst[0])
#     # print(table_array.ncols)
#     rows = table_array.nrows
#     first_col = list(table_array.values)[0:rows]
#     # first_row = table_array.get(1,0)
#     # print(first_row)
#     # result_row = list(table_array.values)[7:14]
#     result_col = list(table_array.values)[(col_index_num - 1) * rows:(col_index_num) * rows]
#     # print(result_row)
#     if not range_lookup:
#         if lookup_value not in first_col:
#             return ExcelError('#N/A', 'lookup_value not in first row of table_array')
#         else:
#             i = first_col.index(lookup_value)
#             ref = first_col.order[i]
#     else:
#         i = None
#         for j, v in enumerate(first_col):
#             # print(v)
#             if lookup_value >= v:
#                 i = j
#                 # i = first_row.index(v)
#                 # print('i',i)
#                 ref = first_col[i]
#             else:
#                 break
#         # print(i)
#         if i is None:
#             # print("true")
#             return ExcelError('#N/A', 'lookup_value smaller than all values of table_array')
#     # print('ref', ref)
#     # print('idef', i)
#     # print(result_row[i])
#     return result_col[i]

def vlookup(lookup_value, table_array, col_index_num, range_lookup = True): # https://support.office.com/en-us/article/VLOOKUP-function-0bbc8083-26fe-4963-8ab8-93a18ad188a1

    if not isinstance(table_array, Range):
        return ExcelError('#VALUE', 'table_array should be a Range')

    if col_index_num > table_array.ncols:
        return ExcelError('#VALUE', 'col_index_num is greater than the number of cols in table_array')

    first_column = table_array.get(0, 1)
    # print(table_array)
    # print(first_column)
    result_column = table_array.get(0, col_index_num)

    if not range_lookup:
        if lookup_value not in first_column.values:
            return ExcelError('#N/A', 'lookup_value not in first column of table_array')
        else:
            i = first_column.values.index(lookup_value)
            ref = first_column.order[i]
    else:
        i = None
        for v in first_column.values:
            if type(v) is str:
                continue
            # print(v)
            # print(type(v))
            if lookup_value >= v:
                i = first_column.values.index(v)
                ref = first_column.order[i]
            else:
                break

        if i is None:
            return ExcelError('#N/A', 'lookup_value smaller than all values of table_array')

    return Range.find_associated_value(ref, result_column)


def sln(cost, salvage, life): # Excel reference: https://support.office.com/en-us/article/SLN-function-cdb666e5-c1c6-40a7-806a-e695edc2f1c8

    for arg in [cost, salvage, life]:
        if isinstance(arg, ExcelError) or arg in ErrorCodes:
            return arg

    return (cost - salvage) / life


def vdb(cost, salvage, life, start_period, end_period, factor = 2, no_switch = False): # Excel reference: https://support.office.com/en-us/article/VDB-function-dde4e207-f3fa-488d-91d2-66d55e861d73

    for arg in [cost, salvage, life, start_period, end_period, factor, no_switch]:
        if isinstance(arg, ExcelError) or arg in ErrorCodes:
            return arg

    for arg in [cost, salvage, life, start_period, end_period, factor]:
        if not isinstance(arg, (float, int)):
            return ExcelError('#VALUE', 'Arg %s should be an int, float or long, instead: %s' % (arg, type(arg)))

    start_period = start_period
    end_period = end_period

    sln_depr = sln(cost, salvage, life)

    depr_rate = factor / life
    acc_depr = 0
    depr = 0

    switch_to_sln = False
    sln_depr = 0

    result = 0

    start_life = 0

    delta_life = life % 1
    if delta_life > 0: # to handle cases when life is not an integer
        end_life = int(life + 1)
    else:
        end_life = int(life)
    periods = list(range(start_life, end_life))

    if int(start_period) != start_period:
        delta_start = abs(int(start_period) - start_period)

        depr = (cost - acc_depr) * depr_rate * delta_start
        acc_depr += depr

        start_life = 1

        periods = [x + 0.5 for x in periods]

    for index, current_year in enumerate(periods):

        if not no_switch: # no_switch = False (Default Case)
            if switch_to_sln:
                depr = sln_depr
            else:
                depr = (cost - acc_depr) * depr_rate
                acc_depr += depr

                temp_sln_depr = sln(cost, salvage, life)

                if depr < temp_sln_depr:
                    switch_to_sln = True
                    fixed_remaining_years = life - current_year - 1
                    fixed_remaining_cost = cost - acc_depr

                     # we need to check future sln: current depr should never be smaller than sln to come
                    sln_depr = sln(fixed_remaining_cost, salvage, fixed_remaining_years)

                    if sln_depr > depr: # if it's the case, we switch to sln earlier than the regular case
                        # cancel what has been done
                        acc_depr -= depr
                        fixed_remaining_years += 1
                        fixed_remaining_cost = cost - acc_depr

                        # recalculate depreciation
                        sln_depr = sln(fixed_remaining_cost, salvage, fixed_remaining_years)
                        depr = sln_depr
                        acc_depr += depr
        else: # no_switch = True
            depr = (cost - acc_depr) * depr_rate
            acc_depr += depr

        delta_start = abs(current_year - start_period)

        if delta_start < 1 and delta_start != 0:
            result += depr * (1 - delta_start)
        elif current_year >= start_period and current_year < end_period:

            delta_end = abs(end_period - current_year)

            if delta_end < 1 and delta_end != 0:
                result += depr * delta_end
            else:
                result += depr

    return result


def xnpv(rate, values, dates, lim_rate_low=True, lim_rate_high=False):  # Excel reference: https://support.office.com/en-us/article/XNPV-function-1b42bbf6-370f-4532-a0eb-d67c16b664b7
    """
    Function to calculate the net present value (NPV) using payments and non-periodic dates. It resembles the excel function XPNV().

    :param rate: the discount rate.
    :param values: the payments of which at least one has to be negative.
    :param dates: the dates as excel dates (e.g. 43571 for 16/04/2019).
    :param lim_rate_low: to limit the rate below 0.
    :param lim_rate_high: to limit the rate above 1000 to avoid overflow errors.
    :return: a float being the NPV.
    """
    if isinstance(values, Range):
        values = values.values

    if isinstance(dates, Range):
        dates = dates.values

    if is_not_number_input(rate):
        return numeric_error(rate, 'rate')

    if is_not_number_input(values):
        return numeric_error(values, 'values')

    if is_not_number_input(dates):
        return numeric_error(dates, 'dates')

    if len(values) != len(dates):
        return ExcelError('#NUM!', '`values` range must be the same length as `dates` range in XNPV, %s != %s' % (len(values), len(dates)))

    if lim_rate_low and rate < 0:
        return ExcelError('#NUM!', '`excel cannot handle a negative `rate`' % (len(values), len(dates)))

    if lim_rate_high and rate > 1000:
        raise ExcelError('#NUM!', '`will result in an overflow error due to high `rate`')

    xnpv = 0
    with np.errstate(all='raise'):
        for v, d in zip(values, dates):
            xnpv += v / np.power(1.0 + rate, (d - dates[0]) / 365)

    return xnpv


def pmt(*args): # Excel reference: https://support.office.com/en-us/article/PMT-function-0214da64-9a63-4996-bc20-214433fa6441
    rate = args[0]
    num_payments = args[1]
    present_value = args[2]
    # WARNING fv & type not used yet - both are assumed to be their defaults (0)
    # fv = args[3]
    # type = args[4]
    return -present_value * rate / (1 - np.power(1 + rate, -num_payments))


# https://support.office.com/en-us/article/POWER-function-D3F2908B-56F4-4C3F-895A-07FB519C362A
def power(number, power):

    if number == power == 0:
        # Really excel?  What were you thinking?
        return ExcelError('#NUM!', 'Number and power cannot both be zero' % str(number))

    if power < 1 and number < 0:
        return ExcelError('#NUM!', '%s must be non-negative' % str(number))

    return np.power(number, power)


# https://support.office.com/en-ie/article/sqrt-function-654975c2-05c4-4831-9a24-2c65e4040fdf
def sqrt(number):
    if number < 0:
        return ExcelError('#NUM!', '%s must be non-negative' % str(index_num))
    return np.sqrt(number)


# https://support.office.com/en-ie/article/today-function-5eb3078d-a82c-4736-8930-2f51a028fdd9
def today():
    reference_date = datetime.datetime.today().date()
    days_since_epoch = reference_date - EXCEL_EPOCH
    # why +2 ?
    # 1 based from 1900-01-01
    # I think it is "inclusive" / to the _end_ of the day.
    # https://support.office.com/en-us/article/date-function-e36c0c8c-4104-49da-ab83-82328b832349
    """Note: Excel stores dates as sequential serial numbers so that they can be used in calculations.
    January 1, 1900 is serial number 1, and January 1, 2008 is serial number 39448 because it is 39,447 days after January 1, 1900.
     You will need to change the number format (Format Cells) in order to display a proper date."""
    return days_since_epoch.days + 2


# https://support.office.com/en-us/article/concat-function-9b1a9a3f-94ff-41af-9736-694cbd6b4ca2
def concat(*args):
    return concatenate(*tuple(flatten(args)))


# https://support.office.com/en-us/article/CONCATENATE-function-8F8AE884-2CA8-4F7A-B093-75D702BEA31D
# Important: In Excel 2016, Excel Mobile, and Excel Online, this function has
# been replaced with the CONCAT function. Although the CONCATENATE function is
# still available for backward compatibility, you should consider using CONCAT
# from now on. This is because CONCATENATE may not be available in future
# versions of Excel.
#
# BE AWARE; there are functional differences between CONACTENATE AND CONCAT
#
def concatenate(*args):
    if tuple(flatten(args)) != args:
        return ExcelError('#VALUE', 'Could not process arguments %s' % (args))

    cat_string = ''.join(str(a) for a in args)

    if len(cat_string) > CELL_CHARACTER_LIMIT:
        return ExcelError('#VALUE', 'Too long. concatentaed string should be no longer than %s but is %s' % (CELL_CHARACTER_LIMIT, len(cat_String)))

    return cat_string


# https://support.office.com/en-us/article/randbetween-function-4cc7f0d1-87dc-4eb7-987f-a469ab381685
def randbetween(bottom, top):
    # instantiating a new random class so repeated calls don't share state
    r = random.Random()
    return r.randint(bottom, top)


# https://support.office.com/en-us/article/rand-function-4cbfa695-8869-4788-8d90-021ea9f5be73
def rand():
    # instantiating a new random class so repeated calls don't share state
    r = random.Random()
    return r.random()



if __name__ == '__main__':
    pass
