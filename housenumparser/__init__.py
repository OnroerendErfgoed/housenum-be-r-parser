# -*- coding: utf-8 -*-
from housenumparser import merger
from housenumparser import reader
from housenumparser.element import ReadException


def split(data, step=None, on_exc=ReadException.Action.ERROR_MSG):
    """
    Parses a string of house number series and returns single numbers.
    :param data: String or list of strings of house number and/or house
                 number series representations
    :param step: Amount of house numbers per step. Commonly 1 or 2.
                 Default None.
                 When `None`, it will use 2 if beginning and ending of a
                 series are both even or uneven, 1 otherwise.
    :param on_exc: `housenumparser.elements.BadInput`. Flag on how to
                   treat incorrect data. Default BadInput.IGNORE
    :returns: A list of :class: `SingleElement`
    """
    if isinstance(data, list):
        numbers = reader.read_iterable(data, step=step, on_exc=on_exc)
    else:
        numbers = reader.read_data(data, step=step, on_exc=on_exc)
    return [item for number in numbers for item in number.split()]


def merge(data, on_exc=ReadException.Action.ERROR_MSG):
    """
    Parses a string or list of house number series and returns elements merged
    into sequences if possible.
    :param data: String or list of strings of house number and/or house
                 number series representations
    :param on_exc: `housenumparser.reader.BadInput`. Flag on how to
                   treat incorrect data.
                   Default BadInput.IGNORE
    :returns: A list of :class: `Element`
    """
    numbers = split(data, on_exc=on_exc)
    return merger.merge_data(merger.group(numbers))
