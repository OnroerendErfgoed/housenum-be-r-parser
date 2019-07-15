# -*- coding: utf-8 -*-
import housenumparser
from housenumparser.element import BisLetter
from housenumparser.element import BisNumber
from housenumparser.element import BusLetter
from housenumparser.element import BusNumber
from housenumparser.element import HouseNumber
from housenumparser.element import ReadException


def test_single_number():
    label = '25'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert 1 == len(house_numbers)
    hnr = house_numbers[0]
    assert isinstance(hnr, HouseNumber)
    assert str(hnr) == '25'


def test_list_single_number():
    label = ['25']
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert 1 == len(house_numbers)
    hnr = house_numbers[0]
    assert isinstance(hnr, HouseNumber)
    assert str(hnr) == '25'


def test_single_bis_letter():
    label = '25A'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert len(house_numbers) == 1
    hnr = house_numbers[0]
    assert isinstance(hnr, BisLetter)
    assert str(hnr) == '25A'


def test_single_bis_number():
    label = '25/1'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert len(house_numbers) == 1
    hnr = house_numbers[0]
    assert isinstance(hnr, BisNumber)
    assert str(hnr) == '25/1'


def test_bis_number_underscore():
    label = '111_1'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert len(house_numbers) == 1
    hnr = house_numbers[0]
    assert isinstance(hnr, BisNumber)
    assert str(hnr) == '111/1'


def test_bus_number():
    label = '25 bus 3'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert len(house_numbers) == 1
    hnr = house_numbers[0]
    assert isinstance(hnr, BusNumber)
    assert str(hnr) == '25 bus 3'


def test_bus_letter():
    label = '25 bus A'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert len(house_numbers) == 1
    hnr = house_numbers[0]
    assert isinstance(hnr, BusLetter)
    assert str(hnr) == '25 bus A'


def test_house_number_sequence():
    label = '25,27,29,31'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert len(house_numbers) == 4
    assert str(house_numbers[0]) == '25'
    assert str(house_numbers[1]) == '27'
    assert str(house_numbers[2]) == '29'
    assert str(house_numbers[3]) == '31'


def test_list_house_number_sequence_2():
    label = ['25', '27', '29', '31']
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert len(house_numbers) == 4
    assert str(house_numbers[0]) == '25'
    assert str(house_numbers[1]) == '27'
    assert str(house_numbers[2]) == '29'
    assert str(house_numbers[3]) == '31'


def test_string_house_number_sequence():
    label = '25-31'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert len(house_numbers) == 4
    assert str(house_numbers[0]) == '25'
    assert str(house_numbers[1]) == '27'
    assert str(house_numbers[2]) == '29'
    assert str(house_numbers[3]) == '31'


def test_string_house_number_sequence_2():
    label = '25-32'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert len(house_numbers) == 8
    assert '25' == str(house_numbers[0])
    assert '26' == str(house_numbers[1])
    assert '27' == str(house_numbers[2])
    assert '28' == str(house_numbers[3])
    assert '29' == str(house_numbers[4])
    assert '30' == str(house_numbers[5])
    assert '31' == str(house_numbers[6])
    assert '32' == str(house_numbers[7])


def test_house_number_sequence_special():
    label = '25,26-31'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert len(house_numbers) == 7
    assert '25' == str(house_numbers[0])
    assert '26' == str(house_numbers[1])
    assert '27' == str(house_numbers[2])
    assert '28' == str(house_numbers[3])
    assert '29' == str(house_numbers[4])
    assert '30' == str(house_numbers[5])
    assert '31' == str(house_numbers[6])


def test_combination_house_number_sequences():
    label = '25-31,18-26'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert len(house_numbers) == 9
    assert '25' == str(house_numbers[0])
    assert '27' == str(house_numbers[1])
    assert '29' == str(house_numbers[2])
    assert '31' == str(house_numbers[3])
    assert '18' == str(house_numbers[4])
    assert '20' == str(house_numbers[5])
    assert '22' == str(house_numbers[6])
    assert '24' == str(house_numbers[7])
    assert '26' == str(house_numbers[8])


def test_bus_number_sequence():
    label = '25 bus 3-7'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert len(house_numbers) == 5
    assert '25 bus 3' == str(house_numbers[0])
    assert '25 bus 4' == str(house_numbers[1])
    assert '25 bus 5' == str(house_numbers[2])
    assert '25 bus 6' == str(house_numbers[3])
    assert '25 bus 7' == str(house_numbers[4])


def test_bus_letter_sequence():
    label = '25 bus C-F'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert len(house_numbers) == 4
    assert '25 bus C' == str(house_numbers[0])
    assert '25 bus D' == str(house_numbers[1])
    assert '25 bus E' == str(house_numbers[2])
    assert '25 bus F' == str(house_numbers[3])


def test_bis_letter_sequence():
    label = '25C-F'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert len(house_numbers) == 4
    assert '25C' == str(house_numbers[0])
    assert '25D' == str(house_numbers[1])
    assert '25E' == str(house_numbers[2])
    assert '25F' == str(house_numbers[3])


def test_bis_letter_sequence_wrong():
    label = '25F-C'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert len(house_numbers) == 1
    assert 'Incorrect range: 25F-C' == str(house_numbers[0])


def test_bis_number_sequence():
    label = '25/3-7'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert 5 == len(house_numbers)
    assert '25/3' == str(house_numbers[0])
    assert '25/4' == str(house_numbers[1])
    assert '25/5' == str(house_numbers[2])
    assert '25/6' == str(house_numbers[3])
    assert '25/7' == str(house_numbers[4])


def test_combination_sequences():
    label = '25C-F,28-32,29 bus 2-5'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert 11 == len(house_numbers)
    assert '25C' == str(house_numbers[0])
    assert '25D' == str(house_numbers[1])
    assert '25E' == str(house_numbers[2])
    assert '25F' == str(house_numbers[3])
    assert '28' == str(house_numbers[4])
    assert '30' == str(house_numbers[5])
    assert '32' == str(house_numbers[6])
    assert '29 bus 2' == str(house_numbers[7])
    assert '29 bus 3' == str(house_numbers[8])
    assert '29 bus 4' == str(house_numbers[9])
    assert '29 bus 5' == str(house_numbers[10])


def test_bis_number_and_house_number_sequence():
    label = '2A,7-11'
    house_numbers = housenumparser.split(label)
    assert isinstance(house_numbers, list)
    assert 4 == len(house_numbers)
    assert '2A' == str(house_numbers[0])
    assert '7' == str(house_numbers[1])
    assert '9' == str(house_numbers[2])
    assert '11' == str(house_numbers[3])


def test_invalid_input_keep_original():
    label = 'A,1/3,?'
    house_numbers = housenumparser.split(
        label, on_exc=ReadException.Action.KEEP_ORIGINAL
    )
    assert isinstance(house_numbers, list)
    assert 3 == len(house_numbers)
    assert 'A' == str(house_numbers[0])
    assert '1/3' == str(house_numbers[1])
    assert '?' == str(house_numbers[2])


def test_invalid_input_ignore_errors():
    house_numbers = housenumparser.split('A,1/3,?',
                                         on_exc=ReadException.Action.ERROR_MSG)
    assert isinstance(house_numbers, list)
    assert 3 == len(house_numbers)
    assert 'Could not parse/understand: A' == str(house_numbers[0])
    assert '1/3' == str(house_numbers[1])
    assert 'Could not parse/understand: ?' == str(house_numbers[2])


def test_bogus_input_drop_errors():
    house_numbers = housenumparser.split('A,1/3,?',
                                         on_exc=ReadException.Action.DROP)
    assert isinstance(house_numbers, list)
    assert 1 == len(house_numbers)
    assert '1/3' == str(house_numbers[0])


def test_input_with_spaces():
    label = ' A , 1/3 , 5 - 7 '
    house_numbers = housenumparser.split(
        label, on_exc=ReadException.Action.KEEP_ORIGINAL
    )
    assert isinstance(house_numbers, list)
    assert 4 == len(house_numbers)
    assert 'A' == str(house_numbers[0])
    assert '1/3' == str(house_numbers[1])
    assert '5' == str(house_numbers[2])
    assert '7' == str(house_numbers[3])


def test_house_numbers_with_step_1():
    label = '10-12'
    house_numbers = housenumparser.split(label, step=1)
    assert isinstance(house_numbers, list)
    assert 3 == len(house_numbers)
    assert '10' == str(house_numbers[0])
    assert '11' == str(house_numbers[1])
    assert '12' == str(house_numbers[2])


def test_house_numbers_with_step_2():
    label = '10-12'
    house_numbers = housenumparser.split(label, step=2)
    assert isinstance(house_numbers, list)
    assert 2 == len(house_numbers)
    assert '10' == str(house_numbers[0])
    assert '12' == str(house_numbers[1])
