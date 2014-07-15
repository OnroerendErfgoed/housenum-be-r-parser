from housenumparser.elements import (
    Huisnummer,
    Bisnummer,
    Busnummer,
    Busletter,
    Bisletter,
    HuisnummerReeks,
    BisnummerReeks,
    BisletterReeks,
    BusnummerReeks,
    BusletterReeks,
    ReadException
)
'''
Klasse die een reeks huisnummers inleest. Bijvoorbeeld:
 eg: "23 bus 5, 23 bus 6" -> array (Busnummer "23 bus 5", Busnummer "23 B-6")
 eg: "23", "24 bus 2" -> array (Huisnummer "23", Busnummer "24 bus 2")
 eg: "25-27" -> array(Huisnummerreeks "25, 26-27")
'''


class Reader():
    '''
    :param input: A :class: `String`.
    :returns: A list from of the input.
    '''
    def readString(self, input, spring, flag):
        return self.readArray(str(input).split(","), spring, flag)

    '''
    :param inputs: A String containing representations of housenumberobjects
        and/or housenumber series objects.
    :returns: A list of :class: `EnkelElement` and/or
        :class: `ReeksElement`.
    '''
    def readArray(self, inputs, spring, flag):
        result = list()
        for input in inputs:
            input = input.strip()
            result.append(self.readNummer(input, spring, flag))
        return result

    '''
    :param input: A list of housenumber representations.
    :returns: A :class: `Element` OR
        an exception in case of incorrect input.
    '''
    def readNummer(self, input, spring, flag):
        if '-' in input:
            if 'bus' in input:
                input = input.split()
                huis = input[0]
                input = input[2].split('-')
                if input[0].isdigit():
                    return BusnummerReeks(huis, input[0], input[1], spring)
                else:
                    return BusletterReeks(huis, input[0], input[1], spring)
            elif '/' in input:
                input = input.split('/')
                huis = input[0]
                input = input[1]
                input = input.split('-')
                return BisnummerReeks(huis, input[0], input[1], spring)
            else:
                input = input.split('-')
                input[0] = input[0].strip()
                input[1] = input[1].strip()
                if input[0].isdigit() and input[1].isdigit():
                    return HuisnummerReeks(input[0], input[1], spring)
                else:
                    einde = input[1]
                    input = input[0]
                    letter = input[-1:]
                    input = input[:-1]
                    return BisletterReeks(input, letter, einde)
        elif '/' in input:
            input = input.split('/')
            return Bisnummer(input[0], input[1])
        elif '_' in input:
            input = input.split('_')
            return Bisnummer(input[0], input[1])
        elif 'bus' in input:
            input = input.split()
            bus = input[2]
            if bus.isdigit():
                return Busnummer(input[0], bus)
            else:
                return Busletter(input[0], bus)
        elif input.isdigit():
            return Huisnummer(input)
        else:
            letter = input[-1:]
            huis = input[:-1]
            if (type(letter) == str) and huis.isdigit():
                return Bisletter(huis, letter)
            else:
                return ReadException(
                    "Could not parse/understand",
                    input,
                    flag)
