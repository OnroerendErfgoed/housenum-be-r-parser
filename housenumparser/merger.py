# -*- coding: utf-8 -*-
"""
Module which takes a string of house numbers and turns them into series.
"""
import collections

from housenumparser.element import BisLetter
from housenumparser.element import BisLetterSequence
from housenumparser.element import BisNumber
from housenumparser.element import BisNumberSequence
from housenumparser.element import BusLetter
from housenumparser.element import BusLetterSequence
from housenumparser.element import BusNumber
from housenumparser.element import BusNumberSequence
from housenumparser.element import HouseNumber
from housenumparser.element import HouseNumberSequence


def group(data):
    """
    Groups all `SingleElement` objects by their type.

    :param data: A list of :class: `SingleElement`. Supported types:
                 HouseNumber, BisNumber, BisLetter, BusNumber, BusLetter
    :results: A dictionary containing lists of :class: `SingleElement`.
    """
    result = {
        'house_numbers': [],
        'bis_numbers': [],
        'bis_letters': [],
        'bus_numbers': [],
        'bus_letters': []
    }
    for x in data:
        if isinstance(x, HouseNumber):
            result['house_numbers'].append(x)
        elif isinstance(x, BisNumber):
            result['bis_numbers'].append(x)
        elif isinstance(x, BisLetter):
            result['bis_letters'].append(x)
        elif isinstance(x, BusNumber):
            result['bus_numbers'].append(x)
        elif isinstance(x, BusLetter):
            result['bus_letters'].append(x)
    return result


def merge_data(data):
    """
    Merges single elements into sequences where possible.

    The input data is expected to be as returned by the `group` function.

    :param data: A dictionary containing lists of :class: `SingleElement`.
    :returns: A list of :class: `SingleElement` and if possible
              :class: `SequenceElement`.
    """
    merged_data = []
    merged_data.extend(
        merge_numbers([obj.house_number for obj in data['house_numbers']],
                      lambda num: HouseNumber(num),
                      lambda first, last: HouseNumberSequence(first, last),
                      (1, 2))
    )
    # For anything else below here, we must first "group by" the data
    # per house number
    numbers_per_house = collections.defaultdict(list)
    for element in data['bis_numbers']:
        numbers_per_house[element.house_number].append(element.bis_number)
    for house_number, numbers in numbers_per_house.items():
        merged_data.extend(
            merge_numbers(
                numbers, lambda num: BisNumber(house_number, num),
                lambda first, last: BisNumberSequence(house_number, first,
                                                      last),
                (1,))
        )
    numbers_per_house = collections.defaultdict(list)
    for element in data['bus_numbers']:
        numbers_per_house[element.house_number].append(element.bus_number)
    for house_number, numbers in numbers_per_house.items():
        merged_data.extend(
            merge_numbers(
                numbers, lambda num: BusNumber(house_number, num),
                lambda first, last: BusNumberSequence(house_number, first,
                                                      last),
                (1,))
        )
    # Treat letters the same as numbers, use `ord` and `chr` to turn the
    # letters into numbers and back into letters.
    letters_per_house = collections.defaultdict(list)
    for element in data['bis_letters']:
        letters_per_house[element.house_number].append(ord(element.bis_letter))
    for house_number, numbers in letters_per_house.items():
        merged_data.extend(
            merge_numbers(
                numbers, lambda num: BisLetter(house_number, chr(num)),
                lambda first, last: BisLetterSequence(house_number, chr(first),
                                                      chr(last)),
                (1,))
        )
    letters_per_house = collections.defaultdict(list)
    for element in data['bus_letters']:
        letters_per_house[element.house_number].append(ord(element.bus_letter))
    for house_number, numbers in letters_per_house.items():
        merged_data.extend(
            merge_numbers(
                numbers, lambda num: BusLetter(house_number, chr(num)),
                lambda first, last: BusLetterSequence(house_number, chr(first),
                                                      chr(last)),
                (1,))
        )
    return merged_data


def merge_numbers(data, single_result, sequence_result, allowed_steps):
    """
    Takes a list of integers and merges them into sequences.

    The list of ints (data) will be traversed and whenever it finds a single
    value, it will call `single_result` and add the result to a new list.
    For every sequence it finds by traversing over the data, it will call
    `sequence_result` and add that to the new list. When the data is
    traversed entirely, the new list returns.

    To determine whether it's a sequence or not, the next number is previewed
    while traversing, and if the difference between the current number and the
    next number is one of the `allowed_steps` it's a sequence.

    :param data: List of ints.
    :param single_result: Callable, takes 1 parameter. Should return a
                          SingleElement instance.
    :param sequence_result: Callable, takes 2 parameter: first, last. Should
                            return a SequenceElement instance.
    :param allowed_steps: steps allowed between 2 elements to be in a sequence
    :returns: List of :class: `Element`, using Sequences if possible.
    """
    data.sort()
    total_len = len(data)
    data = data + [-1, -1]
    result = []

    start = end = step = None
    index = 0
    while index < total_len:
        first = data[index]
        second = data[index + 1]
        index += 1

        # If no current sequence going on: Start new sequence or single number
        if step is None:
            step = second - first
            if step not in allowed_steps:
                # Add a single house number, no sequence possible
                result.append(single_result(first))
                step = None
                continue
            else:
                # Start a new sequence, store the starting number.
                start = first
        # The next number is still valid for the current sequence.
        if second - first == step:
            end = second
        else:  # This marks the end of the sequence.
            if step == 1 and 2 in allowed_steps and (end - start) % 2 == 0:
                # If 2 steps are allowed, 1-5 is actually 1,3,5 and not
                # 1,2,3,4,5 - So we create 1-4, and treat the 5 as new.
                end = end - step
                index -= 1
            result.append(sequence_result(start, end))
            step = None
    return result
