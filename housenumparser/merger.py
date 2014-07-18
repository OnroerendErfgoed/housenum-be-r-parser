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
class which takes a string of housenumbers and turns them into series.
'''


class Merger():
    '''
    :param input: A list :class: `EnkelElement`.
    :results: A dictionary containing seperated lists of
        :class: `EnkelElement`.
    '''
    def group(self, input):
        result = {
            'huisnummer': [], 'bisnummer': [],
            'bisletter': [], 'busnummer': [], 'busletter': []
        }
        for x in input:
            if x.__class__ == Huisnummer:
                result['huisnummer'].append(int(x.getHuisnummer()))
            elif x.__class__ == Bisnummer:
                result['bisnummer'].append(x)
            elif x.__class__ == Bisletter:
                result['bisletter'].append(x)
            elif x.__class__ == Busnummer:
                result['busnummer'].append(x)
            elif x.__class__ == Busletter:
                result['busletter'].append(x)
        return self.mergeNummers(result)

    def mergeNummers(self, input):
        '''
        :param inputs: A dictionary containing seperated lists of
            :class: `EnkelElement`.
        :returns: A list of :class: `EnkelElement`
            and if possible :class: `ReeksElement`.
        '''
        r = []
        r.append(self.mergeHuisnummers(input['huisnummer']))
        r.append(self.mergeN(input['bisnummer']))
        r.append(self.mergeL(input['bisletter']))
        r.append(self.mergeN(input['busnummer']))
        r.append(self.mergeL(input['busletter']))
        return r

    def mergeHuisnummers(self, input):
        '''
        :param input: List of integers.
        :returns: List of :class: `HuisnummerReeks`(if possible)
            and :class: `Huisnummer`.
        '''
        def loop(input, rest, r):
            for y in [2, 1]:
                while len(input) > 1:
                    begin = input[0]
                    einde = input[0]
                    while einde + y in input:
                        input.remove(einde)
                        einde += y
                    if begin != einde:
                        r.append(HuisnummerReeks(begin, einde))
                        input.remove(einde)
                    elif y == 1:
                        rest.append(einde)
                        input.remove(einde)
                    z = loop(input, rest, r)
                    r = z['r']
                    rest = z['rest']
                if len(input) == 1:
                    rest.append(input[0])
                    input.remove(input[0])
            return {'r': r, 'rest': rest}
        if input == []:
            return []
        input.sort()
        begin = input[0]
        einde = input[0]
        z = loop(input, [], [])
        rest = z['rest']
        r = z['r']
        for x in rest:
            r.append(Huisnummer(x))
        return r

    def mergeN(self, input):
        '''
        :param input: List of :class: `Bisnummer`.
        :returns: List of :class: `BisnummerReeks`(if possible)
            and :class: `Bisnummer`.
        :OR:
        :param input: List of :class: `Busnummer`.
        :returns: List of :class: `BusnummerReeks`(if possible)
            and :class: `Busnummer`.
        '''
        r = {}
        result = []
        z = []
        for x in input:
            huis = int(x.getHuisnummer())
            bis = int(x.getBiselement())
            if huis not in r:
                r[huis] = [bis]
            else:
                r[huis].append(bis)
        z = []
        for y in r:
            begin = r[y][0]
            einde = r[y][0]
            while einde + 1 in r[y]:
                einde += 1
            if begin != einde:
                result.append(self.getReeks(x)(y, begin, einde))
            else:
                result.append(x.__class__(y, r[y][0]))
        return result

    def mergeL(self, input):
        '''
        :param input: List of :class: `Bisletter`.
        :returns: List of :class: `BisletterReeks`(if possible)
            and :class: `Bisletter`.
        :OR:
        :param input: List of :class: `Busnummer`.
        :returns: List of :class: `BusletterReeks`(if possible)
            and :class: `Busletter`.
        '''
        r = {}
        result = []
        z = []
        for x in input:
            huis = int(x.getHuisnummer())
            bus = x.getBiselement()
            if huis not in r:
                r[huis] = [bus]
            else:
                r[huis].append(bus)
        z = []
        for y in r:
            begin = r[y][0]
            einde = r[y][0]
            while chr(ord(einde) + 1) in r[y]:
                einde = chr(ord(einde) + 1)
            if begin != einde:
                result.append(self.getReeks(x)(y, begin, einde))
            else:
                result.append(x.__class__(y, begin))
        return result

    def getReeks(self, input):
        '''
        :param input: A :class: `EnkelElement`
        :results: Matching housenumber series class
        '''
        if input.__class__ == Bisnummer:
            return BisnummerReeks
        if input.__class__ == Busnummer:
            return BusnummerReeks
        if input.__class__ == Busletter:
            return BusletterReeks
        if input.__class__ == Bisletter:
            return BisletterReeks
