import abc
import re
from compiler.ast import flatten

'''
A housenumber element.
This is an abstract superclass for all output of the housenumberreader.
This can be a housenumber, a housenumber series, readingerror, etc.
'''


class KVDUtil_HnrElement():

    '''
    :param h1: Integer first huisnummer.
    :param bisn1: String first bisnummer.
    :param bisl1: String first bisletter.
    :param busn1: String first busnummer.
    :param busl1: String first busletter.
    :param h2: Integer last huisnummer of the series.
    :param bisn2: String last bisnummer of the series.
    :param bisl2: String last bisletter of the series.
    :param busn2: String last busnummer of the series.
    :params busl2: String last busletter of the series.
    '''
    def __init__(
        self, h1, bisn1=-1, bisl1=-1, busn1=-1, busl1=-1,
        h2=-1, bisn2=-1, bisl2=-1, busn2=-1, busl2=-1
    ):
            self.data = [
                h1, bisn1, bisl1, busn1, busl1,
                h2, bisn2, bisl2, busn2, busl2
            ]


    '''
    :param i: Integer index of the required data
    :returns: Integer or String
    '''
    def getData(self, i):
        return self.data[i]


'''
Class for a readingerror in the housenumberreader.
'''


class KVDUtil_HnrReadException(KVDUtil_HnrElement):

    def __init__(self, error, input=""):
        self.error = error
        self.input = input
        KVDUtil_HnrElement.__init__(self, -1)

    def isException(self):
        return True

    def split(self):
        return self

    def __str__(self):
        return self.input


'''
An abstract superclass for housenumbers.
'''


class KVDUtil_HnrEnkelElement(KVDUtil_HnrElement):

    def isException(self):
        return False

    def split(self):
        return [self]

    '''
     :returns: The housenumber attribute of the object.
    '''
    def getHuisnummer(self):
        return self.getData(0)

'''
A simple housenumber. eg: 13 of 15.
'''


class KVDUtil_HnrHuisnummer(KVDUtil_HnrEnkelElement):

    def __init__(self, nummer):
        KVDUtil_HnrEnkelElement.__init__(self, nummer)

    def __str__(self):
        return str(self.getHuisnummer())

'''
A housenumber with biselement. eg: "3/1" of "21/5"
'''


class KVDUtil_HnrBiselement(KVDUtil_HnrEnkelElement):

    def getBiselement(self):
        return str(self.getData(self.bisIndex))

'''
A housenumber with bisnummer. eg: "3/1" of "21/5"
'''


class KVDUtil_HnrBisnummer(KVDUtil_HnrBiselement):

    def __init__(self, huis, bis):
        self.bisIndex = 1
        KVDUtil_HnrBiselement.__init__(self, huis, bis)

    def __str__(self):
        return str(self.getHuisnummer()) + "/" + self.getBiselement()


'''
A housenumber with busnummer. eg: "3 bus 1" of "53 bus 5"
'''


class KVDUtil_HnrBusnummer(KVDUtil_HnrBiselement):

    def __init__(self, huis, bus):
        self.bisIndex = 3
        KVDUtil_HnrBiselement.__init__(self, huis, -1, -1, bus)

    def __str__(self):
        return str(self.getHuisnummer()) + " bus " + self.getBiselement()

'''
A housenumber with busletter. eg: "3 bus A" of "53 bus D"
 '''


class KVDUtil_HnrBusletter(KVDUtil_HnrBiselement):
    def __init__(self, huis, bus):
        self.bisIndex = 4
        KVDUtil_HnrBiselement.__init__(self, huis, -1, -1, -1, bus)

    def __str__(self):
        return str(self.getHuisnummer()) + " bus " + self.getBiselement()

'''
A housenumber with bisletter. eg: "3A" of "53D"
'''


class KVDUtil_HnrBisletter(KVDUtil_HnrBiselement):

    def __init__(self, huis, bis):
        self.bisIndex = 2
        KVDUtil_HnrBiselement.__init__(self, huis, -1, bis)

    def __str__(self):
        return str(self.getHuisnummer()) + self.getBiselement()


'''
Abstract class of all series of housenumbers.
'''


class KVDUtil_HnrReeksElement(KVDUtil_HnrEnkelElement):

    def getBegin(self):
        return self.getData(self.beginIndex)

    def getEinde(self):
        return self.getData(self.eindeIndex)
        
    def jump(self):
        if self.spring == '':
            if (int(self.getBegin()) - int(self.getEinde())) % 2 == 0:
                jump = 2
            else:
                jump = 1
        else:
            if self.spring:
                jump = 2
            else:
                jump = 1
        return jump


'''
A series of housenumbers.
eg: "33, 35, 37" -> "33-37"
eg: "33, 34, 35, 36" -> "33-36"
eg: "32, 33, 34, 35, 36"-> "32, 33-36"
'''


class KVDUtil_HnrHuisnummerReeks(KVDUtil_HnrReeksElement):

    '''
     :param begin: First housenumber of the series.
     :param einde: Last housenumber of the series.
    '''
    def __init__(self, begin, einde, spring=''):
        self.beginIndex = 0
        self.eindeIndex = 5
        self.spring = spring
        KVDUtil_HnrReeksElement.__init__(self, begin, -1, -1, -1, -1, einde)

    def __str__(self):
            return str(self.getBegin()) + "-" + str(self.getEinde())

    '''
     :param match: A list of :class: `KVDUtil_HnrHuisnummerReeks`
     :returns: A list of :class: `KVDUtil_HnrHuisnummer`
    '''
    def split(self):
        begin = self.getBegin()
        einde = self.getEinde()
        jump = self.jump()
        res = []
        i = int(begin)
        while i <= int(einde):
            res.append(KVDUtil_HnrHuisnummer(i))
            i += jump
        return res

'''
A series of bisnummers.
  eg: "33/1, 32/2, 33/3" -> "33/1-3"
'''


class KVDUtil_HnrBisnummerReeks(KVDUtil_HnrReeksElement):

    '''
     :param huis: Integer housenumber.
     :param begin: Integer the first bisnummer of the series.
     :param einde: Integer the last bisnummer of the series
    '''
    def __init__(self, huis, begin, einde, spring=''):
        self.beginIndex = 1
        self.eindeIndex = 6
        self.spring = spring
        KVDUtil_HnrReeksElement.__init__(
            self, huis, begin, -1, -1, -1, huis, einde)

    def __str__(self):
        return str(self.getHuisnummer()) + "/" +\
            str(self.getBegin()) + "-" + str(self.getEinde())

    '''
    :param match: A list of :class: `KVDUtil_HnrBisnummerReeks`
    :returns: A list of :class: `KVDUtil_HnrBisnummer`
    '''
    def split(self):
        begin = self.getBegin()
        einde =self.getEinde()
        huis = self.getHuisnummer()
        jump = 1
        res = []
        i = int(begin)
        while i <= int(einde):
            res.append(KVDUtil_HnrBisnummer(huis, i))
            i += jump
        return res

'''
A series of bisletters.
'''


class KVDUtil_HnrBisletterReeks(KVDUtil_HnrReeksElement):

    '''
    :param huis: Integer housenumber
    :param begin: Integer the first number of the series.
    :param einde: Integer the last number of the series.
    '''
    def __init__(self, huis, begin, einde, spring=''):
        self.beginIndex = 2
        self.eindeIndex = 7
        self.spring = spring
        KVDUtil_HnrReeksElement.__init__(
            self, huis, -1, begin, -1, -1, huis, -1, einde)

    def __str__(self):
        return str(self.getHuisnummer()) + self.getBegin() + "-" + self.getEinde()

    '''
    :param match: A list of :class: `KVDUtil_HnrBisletterReeks`
    :returns: A list of :class: `KVDUtil_HnrBisletter`
    '''
    def split(self):
        begin = ord(self.getBegin())
        einde = ord(self.getEinde())
        huis = self.getHuisnummer()
        jump = 1
        res = []
        i = int(begin)
        while i <= int(einde):
            res.append(KVDUtil_HnrBisletter(huis, chr(i)))
            i += jump
        return res

'''
 Een reeks van busnummers.
    eg: "33 bus 1, 32 bus 2, 33 bus 3" -> "33 bus 1-3"
'''


class KVDUtil_HnrBusnummerReeks(KVDUtil_HnrReeksElement):

    '''
    :param huis: Integer housenumber.
    :param begin: Integer the first number of the series.
    :param einde: Integer the last number of the series.
    '''
    def __init__(self, huis, begin, einde, spring=''):
        self.beginIndex = 3
        self.eindeIndex = 8
        self.spring = spring
        KVDUtil_HnrReeksElement.__init__(
            self, huis, -1, -1, begin, -1, huis, -1, -1, einde)

    def __str__(self):
        return str(self.getHuisnummer()) + " bus " +\
            str(self.getBegin()) + "-" + str(self.getEinde())
            
    '''
    :param match: A list of :class: `KVDUtil_HnrBusnummerReeks`
    :returns: A list of :class: `KVDUtil_HnrBusnummer`
    '''
    def split(self):
        begin = self.getBegin()
        einde =self.getEinde()
        huis = self.getHuisnummer()
        jump = 1
        res = []
        i = int(begin)
        while i <= int(einde):
            res.append(KVDUtil_HnrBusnummer(huis, i))
            i += jump
        return res


'''
A series of busletters.
    eg: "33 bus A, 32 bus B, 33 bus C" -> "33 bus A-C"
'''


class KVDUtil_HnrBusletterReeks(KVDUtil_HnrReeksElement):
    '''
     :param huis: integer huisnummer
     :param begin: integer het eerste nummer van de reeks
     :param einde: integer het laatste nummer van de reeks
    '''
    def __init__(self, huis, begin, einde, spring=''):
        self.beginIndex = 4
        self.eindeIndex = 9
        self.spring = spring
        KVDUtil_HnrReeksElement.__init__(
            self, huis, -1, -1, -1, begin, huis, -1, -1, -1, einde)

    def __str__(self):
        return str(self.getHuisnummer()) + " bus "
        + str(self.getBegin()) + "-" + str(self.getEinde())

    '''
    :param match: A list of :class: `KVDUtil_HnrBisletterReeks`
    :returns: A list of :class: `KVDUtil_HnrBisletter`
    '''
    def split(self):
        begin = ord(self.getBegin())
        einde = ord(self.getEinde())
        huis = self.getHuisnummer()
        jump = 1
        res = []
        i = int(begin)
        while i <= int(einde):
            res.append(KVDUtil_HnrBusletter(huis, chr(i)))
            i += jump
        return res
'''
Klasse die een reeks huisnummers inleest. Bijvoorbeeld:
 eg: "23 bus 5, 23 bus 6" -> array (Busnummer "23 bus 5", Busnummer "23 B-6")
 eg: "23", "24 bus 2" -> array (Huisnummer "23", Busnummer "24 bus 2")
 eg: "25-27" -> array(Huisnummerreeks "25, 26-27")
'''


class KVDutil_HnrReader():

    def __init__(self, flag):
        self.flag = flag

    '''
    :param input: A :class: `String`.
    :param flag: A :class: `Integer` flag voor error handling.
    :returns: A list from of the input.
    '''
    def readString(self, input, spring, flag=1):
        return self.readArray(str(input).split(","), spring, flag)

    '''
    :param inputs: A String containing representations of housenumberobjects
        and/or housenumber series objects.
    :param flag: A :class: `Integer` flag voor error handling.
    :returns: A list of :class: `KVDUtil_HnrEnkelElement` and/or
        :class: `KVDUtil_HnrReeksElement`.
    '''
    def readArray(self, inputs, spring, flag=1):
        result = list()
        for input in inputs:
            input = input.strip()
            element = self.readNummer(input, spring)
            result.append(element)
        return result

    '''
    :param input: A list of housenumber representations.
    :returns: A :class: `KVDUtil_HnrElement` OR
        an exception in case of incorrect input.
    '''
    def readNummer(self, input, spring):
        if '-' in input:
            if 'bus' in input:
                input = input.split()
                huis = input[0]
                input = input[2].split('-')
                if input[0].isdigit():
                    return KVDUtil_HnrBusnummerReeks(huis, input[0], input[1], spring)
                else:
                    return KVDUtil_HnrBusletterReeks(huis, input[0], input[1], spring)
            elif '/' in input:
                input = input.split('/')
                huis = input[0]
                input = input[1]
                input = input.split('-')
                return KVDUtil_HnrBisnummerReeks(huis, input[0], input[1], spring)
            else:
                input = input.split('-')
                input[0] = input[0].strip()
                input[1] = input[1].strip()
                if input[0].isdigit() and input[1].isdigit():
                    return KVDUtil_HnrHuisnummerReeks(input[0], input[1], spring)
                else:
                    einde = input[1]
                    input = input[0]
                    letter = input[-1:]
                    input = input[:-1]
                    return KVDUtil_HnrBisletterReeks(input, letter, einde)
        elif '/' in input:
            input = input.split('/')
            return KVDUtil_HnrBisnummer(input[0], input[1])
        elif '_' in input:
            input = input.split('_')
            return KVDUtil_HnrBisnummer(input[0], input[1])
        elif 'bus' in input:
            input = input.split()
            bus = input[2]
            if bus.isdigit():
                return KVDUtil_HnrBusnummer(input[0], bus)
            else:
                return KVDUtil_HnrBusletter(input[0], bus)
        elif input.isdigit():
            return KVDUtil_HnrHuisnummer(input)
        else:
            letter = input[-1:]
            huis = input[:-1]
            if (type(letter) == str) and huis.isdigit():
                return KVDUtil_HnrBisletter(huis, letter)
            else:
                return KVDUtil_HnrReadException(
                    "Could not parse/understand",
                    input)


'''
class which takes a string of housenumbers and turns them into series.
'''


class KVDutil_HnrSpeedMerger():
    '''
    :param input: A list :class: `KVDUtil_HnrEnkelElement`.
    :results: A dictionary containing seperated lists of
        :class: `KVDUtil_HnrEnkelElement`.
    '''
    def group(self, input):
        result = {
            'huisnummer': [], 'bisnummer': [],
            'bisletter': [], 'busnummer': [], 'busletter': []
        }
        for x in input:
            if x.__class__ == KVDUtil_HnrHuisnummer:
                result['huisnummer'].append(int(x.getHuisnummer()))
            elif x.__class__ == KVDUtil_HnrBisnummer:
                result['bisnummer'].append(x)
            elif x.__class__ == KVDUtil_HnrBisletter:
                result['bisletter'].append(x)
            elif x.__class__ == KVDUtil_HnrBusnummer:
                result['busnummer'].append(x)
            elif x.__class__ == KVDUtil_HnrBusletter:
                result['busletter'].append(x)
        return self.mergeNummers(result)

    '''
    :param inputs: A dictionary containing seperated lists of
        :class: `KVDUtil_HnrEnkelElement`.
    :returns list: A list of :class: `KVDUtil_HnrEnkelElement`
        and if possible :class: `KVDUtil_HnrReeksElement`.
    '''
    def mergeNummers(self, input):
        r = []
        r.append(self.mergeHuisnummers(input['huisnummer']))
        r.append(self.mergeN(input['bisnummer']))
        r.append(self.mergeL(input['bisletter']))
        r.append(self.mergeN(input['busnummer']))
        r.append(self.mergeL(input['busletter']))
        return r

    '''
    :param input: List of integers.
    :returns: List of :class: `KVDUtil_HnrHuisnummerReeks`(if possible)
        and :class: `KVDUtil_HnrHuisnummer`.
    '''
    def mergeHuisnummers(self, input):
        def loop(input, rest, r):
            for y in [2, 1]:
                while len(input) > 1:
                    begin = input[0]
                    einde = input[0]
                    while einde + y in input:
                        input.remove(einde)
                        einde += y
                    if begin != einde:
                        r.append(KVDUtil_HnrHuisnummerReeks(begin, einde))
                        input.remove(einde)
                    elif y == 1 :
                        print 'ja'
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
            r.append(KVDUtil_HnrHuisnummer(x))
        return r

    '''
    :param input: List of :class: `KVDUtil_HnrBisnummer`.
    :returns: List of :class: `KVDUtil_HnrBisnummerReeks`(if possible)
        and :class: `KVDUtil_HnrBisnummer`.
        OR
    :param input: List of :class: `KVDUtil_HnrBusnummer`.
    :returns: List of :class: `KVDUtil_HnrBusnummerReeks`(if possible)
        and :class: `KVDUtil_HnrBusnummer`.
    '''
    def mergeN(self, input):
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

    '''
    :param input: List of :class: `KVDUtil_HnrBisletter`.
    :returns: List of :class: `KVDUtil_HnrBisletterReeks`(if possible)
        and :class: `KVDUtil_HnrBisletter`.
        OR
    :param input: List of :class: `KVDUtil_HnrBusnummer`.
    :returns: List of :class: `KVDUtil_HnrBusletterReeks`(if possible)
        and :class: `KVDUtil_HnrBusletter`.
    '''
    def mergeL(self, input):
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
        print r
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

    '''
    :param input: A :class: `KVDUtil_HnrEnkelElement`
    :results: Matching housenumber series class
    '''
    def getReeks(self, input):
        if input.__class__ == KVDUtil_HnrBisnummer:
            return KVDUtil_HnrBisnummerReeks
        if input.__class__ == KVDUtil_HnrBusnummer:
            return KVDUtil_HnrBusnummerReeks
        if input.__class__ == KVDUtil_HnrBusletter:
            return KVDUtil_HnrBusletterReeks
        if input.__class__ == KVDUtil_HnrBisletter:
            return KVDUtil_HnrBisletterReeks


'''
This class is used to split housenumberlabels into individual labels 
or to join individual labels into a more compact representation. 
eg:
<code>
    facade = new KVDutil_HuisnummerFacade( );
    huisnummers = facade.split( '15-21' );
    print huisnummers[0]; // 15
    print huisnummers[1]; // 17
    print huisnummers[2]; // 19
    print huisnummers[3]; // 21
    reeksen = facade.merge(huisnummers);
    print reeksen[0]; // 15-21
</code>
'''


class KVDutil_HuisnummerFacade():
    def __init__(self, flag=1):
        self.flag = flag
        self.reader = KVDutil_HnrReader(self.flag)
        self.speedmerger = KVDutil_HnrSpeedMerger()

    '''
    :param input: string of housenumber and/or
        housenumber series representations
    :returns: A list of :class: `KVDUtil_HnrEnkelElement`
    '''
    def split(self, input, spring=''):
        nummers = self.stringToNummers(input, spring)
        reeks = self.splitten(nummers)
        return self.flatten(reeks)

    '''
    :param input: string of housenumber and/or
        housenumber series representations.
    :returns: A list of housenumber and/or housenumber series representations.
    '''
    def stringToNummers(self, input, spring):
        return self.reader.readString(input, spring, self.flag)

    '''
    :param input: A list of :class: `KVDUtil_HnrReeksElement`.
    :returns: A list of :class: `KVDUtil_HnrEnkelElement`.
    '''
    def splitten(self, input):
        r = []
        for i in input:
            r.append(i.split())
        return r

    '''
    :param input: A list of housenumber and/or
        housenumber series representations.
    :returns: A list of :class: `KVDUtil_HnrEnkelElement`
    '''
    def merge(self, input, spring=''):
        reeksen = self.stringToNummers(input, spring)
        nummers = self.splitten(reeksen)
        nummers = self.flatten(nummers)
        result = self.speedmerger.group(nummers)
        for x in self.flatten(result):
            print x
        return self.flatten(result)

    '''
    :param input: A nested list.
    :results: A list containing :class: `KVDUtil_HnrElement`.
    '''
    def flatten(self, input):
        r = []
        for x in input:
            if x .__class__ == list and x != []:
                for y in x:
                    r.append(y)
            else:
                if x != []:
                    r.append(x)
        return r
