# -*- coding: utf-8 -*-
import re
from enum import Enum


class BadInput(Enum):
    RAISE = 1  # Raises exception on bad input
    IGNORE = 2  # A element with str() error message info will be returned
    KEEP_ORIGINAL = 3  # A element with str() original data will be returned
    DROP = 4  # The error will be ignored, and not exist in the output.


class Element(object):
    """
    A house number element.
    This is an abstract superclass for all output of the housenumparser.reader
    This can be a house number, a house number series, readingerror, etc.
    """

    def __init__(self, first_house_number, first_bis_number=-1,
                 first_bis_letter=-1, first_bus_number=-1, first_bus_letter=-1,
                 last_house_number=-1, last_bis_number=-1, last_bis_letter=-1,
                 last_bus_number=-1, last_bus_letter=-1):
        """
        :param first_house_number: Integer first house_number.
        :param first_bis_number: Integer first bis number.
        :param first_bis_letter: String first bis letter.
        :param first_bus_number: Integer first bus number.
        :param first_bus_letter: String first bus letter.
        :param last_house_number: Integer last house_number of the series.
        :param last_bis_number: String last bis number of the series.
        :param last_bis_letter: String last bis letter of the series.
        :param last_bus_number: String last bus number of the series.
        :param last_bus_letter: String last bus letter of the series.
        """
        self.first_house_number = first_house_number
        self.first_bis_number = first_bis_number
        self.first_bis_letter = first_bis_letter
        self.first_bus_number = first_bus_number
        self.first_bus_letter = first_bus_letter
        self.last_house_number = last_house_number
        self.last_bis_number = last_bis_number
        self.last_bis_letter = last_bis_letter
        self.last_bus_number = last_bus_number
        self.last_bus_letter = last_bus_letter

    @property
    def house_number(self):
        """
        :returns: The house number attribute of the object.
        """
        return self.first_house_number


class ReadException(Element):
    """
    Class for a reading error in housenumparser.reader.
    """

    def __init__(self, error, data="", on_exc=BadInput.IGNORE):
        super(ReadException, self).__init__(None)
        self.error = error
        self.data = data
        self.on_exc = on_exc

    def split(self):
        return [self]

    def __str__(self):
        if self.on_exc == BadInput.KEEP_ORIGINAL:
            return self.data
        if self.on_exc == BadInput.IGNORE:
            return self.error


class SequenceElement(Element):
    """
    Abstract class of all series of house numbers.
    """


class HouseNumberSequence(SequenceElement):
    """
    A series of house numbers.
    eg: "33, 35, 37" -> "33-37"
    eg: "33, 34, 35, 36" -> "33-36"
    eg: "32, 33, 34, 35, 36"-> "32, 33-36"
    """
    regex = re.compile(r'^(\d+)-(\d+)$')

    def __init__(self, first_house_number, last_house_number, step=None):
        """
        :param first_house_number: First house number of the series.
        :param last_house_number: Last house number of the series.
        :param step: Step to take between first and last element.
        """
        self.step = step or self._default_step(first_house_number,
                                               last_house_number)
        super(HouseNumberSequence, self).__init__(
            first_house_number, last_house_number=last_house_number
        )

    def _default_step(self, first, last):
        """
        Calculates the step based on the first and last number

        :param first: first number of the series
        :param last: last number of the series
        :return: 2 if both numbers are even or uneven. 1 if they're different.
        """
        return 2 if first % 2 == last % 2 else 1

    def __str__(self):
        return ('{first_house}-{last_house}'
                .format(first_house=self.first_house_number,
                        last_house=self.last_house_number))

    def split(self):
        """
         :returns: A list of :class: `HouseNumber`
        """
        return [HouseNumber(number) for number
                in range(self.first_house_number, self.last_house_number + 1,
                         self.step)]


class BisNumberSequence(SequenceElement):
    """
    A series of bis numbers.
      eg: "33/1, 32/2, 33/3" -> "33/1-3"
    """
    regex = re.compile(r'^(\d+)[/_](\d+)-(\d+)$')

    def __init__(self, house_number, first_bis_number, last_bis_number):
        """
        :param house_number: Integer house number.
        :param first_bis_number: Integer the first bis number of the series.
        :param last_bis_number: Integer the last bis number of the series
        """
        super(BisNumberSequence, self).__init__(
            house_number, first_bis_number=first_bis_number,
            last_bis_number=last_bis_number
        )

    def __str__(self):
        return ('{house_number}/{first_bis}-{last_bis}'
                .format(house_number=self.house_number,
                        first_bis=self.first_bis_number,
                        last_bis=self.last_bis_number))

    def split(self):
        """
        :returns: A list of :class: `BisNumber`
        """
        return [BisNumber(self.house_number, bis_number) for bis_number
                in range(self.first_bis_number, self.last_bis_number + 1)]


class BisLetterSequence(SequenceElement):
    """
    A series of bis letters.
    """
    regex = re.compile(r'^(\d+)/?([a-zA-Z]+)-([a-zA-Z]+)$')

    def __init__(self, house_number, first_bis_letter, last_bis_letter):
        """
        :param house_number: Integer house number
        :param first_bis_letter: String the first number of the series.
        :param last_bis_letter: String the last number of the series.
        """
        super(BisLetterSequence, self).__init__(
            house_number, first_bis_letter=first_bis_letter,
            last_bis_letter=last_bis_letter
        )

    def __str__(self):
        return ('{house_number}{first_letter}-{last_letter}'
                .format(house_number=self.house_number,
                        first_letter=self.first_bis_letter,
                        last_letter=self.last_bis_letter))

    def split(self):
        """
        :returns: A list of :class: `BisLetter`
        """
        return [BisLetter(self.house_number, chr(i)) for i
                in range(ord(self.first_bis_letter),
                         ord(self.last_bis_letter) + 1)]


class BusNumberSequence(SequenceElement):
    """
    A series of bus numbers.
        eg: "33 bus 1, 32 bus 2, 33 bus 3" -> "33 bus 1-3"
    """
    regex = re.compile(r'^(\d+)bus(\d+)-(\d+)$')

    def __init__(self, house_number, first_bus_number, last_bus_number):
        """
        :param house_number: Integer house number.
        :param first_bus_number: Integer the first number of the series.
        :param last_bus_number: Integer the last number of the series.
        """
        super(BusNumberSequence, self).__init__(
            house_number, first_bus_number=first_bus_number,
            last_bus_number=last_bus_number
        )

    def __str__(self):
        return ('{house_number} bus {first_bus}-{last_bus}'
                .format(house_number=self.house_number,
                        first_bus=self.first_bus_number,
                        last_bus=self.last_bus_number))

    def split(self):
        """
        :returns: A list of :class: `BusNumber`
        """
        return [BusNumber(self.house_number, bus_number) for bus_number
                in range(self.first_bus_number, self.last_bus_number + 1)]


class BusLetterSequence(SequenceElement):
    """
    A series of busletters.
        eg: "33 bus A, 32 bus B, 33 bus C" -> "33 bus A-C"
    """
    regex = re.compile(r'^(\d+)bus([a-zA-Z]+)-([a-zA-Z]+)$')

    def __init__(self, house_number, first_bus_letter, last_bus_letter):
        """
        :param house_number: Integer house number
        :param first_bus_letter: String the first number of the series.
        :param last_bus_letter: String the last number of the series.
        """
        super(BusLetterSequence, self).__init__(
            house_number, first_bus_letter=first_bus_letter,
            last_bus_letter=last_bus_letter
        )

    def __str__(self):
        return ('{house_number} bus {first_letter}-{last_letter}'
                .format(house_number=self.house_number,
                        first_letter=self.first_bus_letter,
                        last_letter=self.last_bus_letter))

    def split(self):
        """
        :returns: A list of :class: `BusLetter`
        """
        return [BusLetter(self.house_number, chr(i)) for i
                in range(ord(self.first_bus_letter),
                         ord(self.last_bus_letter) + 1)]


class SingleElement(Element):
    """
    An abstract superclass for house numbers.
    """

    def split(self):
        return [self]


class HouseNumber(SingleElement):
    """
    A simple house number. eg: 13 or 15.
    """
    sequence_class = HouseNumberSequence
    regex = re.compile(r'^(\d+)$')

    def __str__(self):
        return str(self.house_number)


class BisNumber(SingleElement):
    """
    A house number with bis number. eg: "3/1" or "21/5"
    """
    sequence_class = BisNumberSequence
    regex = re.compile(r'^(\d+)[/_](\d+)$')

    def __init__(self, house_number, bis_number):
        super(BisNumber, self).__init__(house_number,
                                        first_bis_number=bis_number)

    @property
    def bis_number(self):
        return self.first_bis_number

    def __str__(self):
        return '{house}/{bis_number}'.format(house=self.house_number,
                                             bis_number=self.bis_number)


class BusNumber(SingleElement):
    """
    A house number with bus number. eg: "3 bus 1" or "53 bus 5"
    """
    sequence_class = BusNumberSequence
    regex = re.compile(r'^(\d+)bus(\d+)$')

    def __init__(self, house_number, bus_number):
        super(BusNumber, self).__init__(house_number,
                                        first_bus_number=bus_number)

    @property
    def bus_number(self):
        return self.first_bus_number

    def __str__(self):
        return '{house} bus {bus_number}'.format(house=self.house_number,
                                                 bus_number=self.bus_number)


class BusLetter(SingleElement):
    """
    A house number with bus letter. eg: "3 bus A" or "53 bus D"
    """
    sequence_class = BusLetterSequence
    regex = re.compile(r'^(\d+)bus([a-zA-Z]+)$')

    def __init__(self, house_number, bus_letter):
        super(BusLetter, self).__init__(house_number,
                                        first_bus_letter=bus_letter)

    @property
    def bus_letter(self):
        return self.first_bus_letter

    def __str__(self):
        return '{house} bus {bus_letter}'.format(house=self.house_number,
                                                 bus_letter=self.bus_letter)


class BisLetter(SingleElement):
    """
    A house number with bis letter. eg: "3A" or "53D"
    """
    sequence_class = BisLetterSequence
    regex = re.compile(r'^(\d+)[/_]?([a-zA-Z]+)$')

    def __init__(self, house_number, bis_letter):
        super(BisLetter, self).__init__(house_number,
                                        first_bis_letter=bis_letter)

    @property
    def bis_letter(self):
        return self.first_bis_letter

    def __str__(self):
        return '{house}{bis_letter}'.format(house=self.house_number,
                                            bis_letter=self.bis_letter)
