# -*- coding: utf-8 -*-
"""
Module which reads a series of house numbers.
 eg: "23 bus 5, 23 bus 6" -> array (Busnummer "23 bus 5", Busnummer "23
 B-6")
 eg: "23", "24 bus 2" -> array (Huisnummer "23", Busnummer "24 bus 2")
 eg: "25-27" -> array (Huisnummerreeks "25, 26-27")
"""
import re

from housenumparser.elements import BadInput
from housenumparser.elements import BisLetter
from housenumparser.elements import BisLetterSequence
from housenumparser.elements import BisNumber
from housenumparser.elements import BisNumberSequence
from housenumparser.elements import BusLetter
from housenumparser.elements import BusLetterSequence
from housenumparser.elements import BusNumber
from housenumparser.elements import BusNumberSequence
from housenumparser.elements import HouseNumber
from housenumparser.elements import HouseNumberSequence
from housenumparser.elements import ReadException


def read_data(data, step=None, on_exc=BadInput.IGNORE):
    """
    Parses a comma-seperated string of house number elements.

    :param data: A :class: `String` with comma-seperated house numbers
    :param step: Amount of house numbers per step. Commonly 1 or 2.
                 Default None.
                 When `None`, it will use 2 if beginning and ending of a
                 series are both even or uneven, 1 otherwise.
    :param on_exc: `housenumparser.reader.BadInput`. Flag on how to
                   treat incorrect data.
                   Default BadInput.IGNORE
    :returns: A list from of the data.
    """
    return read_iterable(str(data).split(","), step=step, on_exc=on_exc)


def read_iterable(inputs, step=None, on_exc=BadInput.IGNORE):
    """
    Parses an iterable of house number element strings.

    :param inputs: A `list`` containing strings of house numbers
        and/or house number series objects.
    :param step: Amount of house numbers per step. Commonly 1 or 2.
                 Default None.
                 When `None`, it will use 2 if beginning and ending of a
                 series are both even or uneven, 1 otherwise.
    :param on_exc: `housenumparser.reader.BadInput`. Flag on how to
                   treat incorrect data.
                   Default BadInput.IGNORE
    :returns: A list of :class: `Element`.
    """
    result = list()
    for data in inputs:
        data = data.strip()
        parsed_element = read_element(data, step=step, on_exc=on_exc)
        if parsed_element is not None:
            result.append(parsed_element)
    return result


def read_element(data, step=None, on_exc=BadInput.IGNORE):
    """
    Parses a single house number element string.

    :param data: A String representating a house number.
    :param step: Amount of house numbers per step. Commonly 1 or 2.
                 Default None.
                 When `None`, it will use 2 if beginning and ending of a
                 series are both even or uneven, 1 otherwise.
    :param on_exc: `housenumparser.reader.BadInput`. Flag on how to
                   treat incorrect data.
                   Default BadInput.IGNORE
    :returns: A :class: `Element` OR an exception in case of incorrect data.
    """
    element_classes = [BusNumberSequence, BusLetterSequence, BisNumberSequence,
                       BisLetterSequence, BusNumber, BusLetter, BisNumber,
                       BisLetter, HouseNumberSequence, HouseNumber]
    data = re.sub(r'\s', '', data)
    for element_class in element_classes:
        match = element_class.regex.match(data)
        if match:
            args = [int(group) if group.isdigit() else group
                    for group in match.groups()]
            kwargs = {}
            if element_class == HouseNumberSequence:
                kwargs['step'] = step
            element = element_class(*args, **kwargs)
            return element
    if on_exc == BadInput.RAISE:
        raise ValueError("Could not parse/understand input: {}".format(data))
    elif on_exc == BadInput.DROP:
        return None
    elif on_exc in (BadInput.IGNORE, BadInput.KEEP_ORIGINAL):
        return ReadException("Could not parse/understand", data=data,
                             on_exc=on_exc)
