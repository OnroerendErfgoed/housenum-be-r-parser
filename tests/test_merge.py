# -*- coding: utf-8 -*-
import housenumparser


def test_all_forms():
    label = ('32-36, 25-31, 1A-F, 2/1-10, 4 bus 1-30, 43, 44 bus 1, 45/1, '
             '46A, 33 bus A-C')
    house_numbers = housenumparser.merge(label)
    assert isinstance(house_numbers, list)
    assert 10 == len(house_numbers)
    house_numbers = [str(house_number) for house_number in house_numbers]
    assert '25-31' in house_numbers
    assert '32-36' in house_numbers
    assert '43' in house_numbers
    assert '2/1-10' in house_numbers
    assert '45/1' in house_numbers
    assert '1A-F' in house_numbers
    assert '46A' in house_numbers
    assert '44 bus 1' in house_numbers
    assert '4 bus 1-30' in house_numbers
    assert '33 bus A-C' in house_numbers


def test_house_number_sequences():
    label = ('32, 34, 36, 38, 25, 27, 29, 31, 39, 40, 41, 42, 43, 44, 46, '
             '47, 48, 49, 50, 52, 54')
    house_numbers = housenumparser.merge(label)
    assert isinstance(house_numbers, list)
    assert 5 == len(house_numbers)
    house_numbers = [str(house_number) for house_number in house_numbers]
    assert '25-31' in house_numbers
    assert '32-38' in house_numbers
    assert '39-44' in house_numbers
    assert '46-49' in house_numbers
    assert '50-54' in house_numbers


def test_combination_house_number_sequences():
    label = '25-31, 18-26'
    house_numbers = housenumparser.merge(label)
    assert isinstance(house_numbers, list)
    assert 3 == len(house_numbers)
    house_numbers = [str(house_number) for house_number in house_numbers]
    assert '18-24' in house_numbers
    assert '25-26' in house_numbers
    assert '27-31' in house_numbers


def test_list_combination_house_number_sequences():
    label = ['25-31', '18-26']
    house_numbers = housenumparser.merge(label)
    assert isinstance(house_numbers, list)
    assert 3 == len(house_numbers)
    house_numbers = [str(house_number) for house_number in house_numbers]
    assert '18-24' in house_numbers
    assert '25-26' in house_numbers
    assert '27-31' in house_numbers


def test_bis_number_sequences():
    label = '10/1-3, 10/4, 15/3-7, 15/8-10'
    house_numbers = housenumparser.merge(label)
    assert isinstance(house_numbers, list)
    assert 2 == len(house_numbers)
    house_numbers = [str(house_number) for house_number in house_numbers]
    assert '10/1-4' in house_numbers
    assert '15/3-10' in house_numbers


def test_house_number_no_sequences():
    label = '32, 37'
    house_numbers = housenumparser.merge(label)
    assert isinstance(house_numbers, list)
    assert 2 == len(house_numbers)
    house_numbers = [str(house_number) for house_number in house_numbers]
    assert '32' in house_numbers
    assert '37' in house_numbers
