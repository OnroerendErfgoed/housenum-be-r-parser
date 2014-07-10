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
    :returns: list containing all the data of this housenumber
    '''
    def getDatas(self):
        return self.data

    '''
    :param i: Integer index of the required data
    :returns: Integer or String
    '''
    def getData(self, i):
        return self.data[i]

    def setData(self, i, val):
        self.data[i] = val

    '''
     :param el: A :class: `KVDUtil_HnrElement`
     :returns: integer
        (-1 if self.data < el ; 0 if self.data = el ; 1 if self.data > el)
    '''
    def compareTo(self, el):
        i = 0
        while (i < 9) and (self.data[i] == el.getData(i)):
            i += 1

        if self.data[i] == el.getData(i):
            return 0
        elif self.data[i] < el.getData(i):
            return -1
        else:
            return 1

    '''
     geeft een lijst met alle huisnummers die dit element
     bevat.
     :returns: een list met huisnummers
    '''
    @abc.abstractmethod
    def split():
        pass

    '''
    :returns: boolean
    '''
    @abc.abstractmethod
    def isException(self):
        pass

    '''
     :param el1: A :class: `KVDUtil_HnrElement`
     :param el2: A :class: `KVDUtil_HnrElement`
     :returns: integer (-1 if el1 < el ; 0 if el1 = el ; 1 if el1 > el)
    '''
    def compare(self, el1, el2):
        return el1.compareTo(el2)

'''
 Klasse voor een leesfout in de huisnummerlezer.
'''


class KVDUtil_HnrReadException(KVDUtil_HnrElement):

    def __init__(self, error, input=""):
        self.error = error
        self.input = input
        KVDUtil_HnrElement.__init__(self, -1)

    def isException(self):
        return True

    def setData(self, i, val):
        pass

    def split(self):
        return list(self)

    '''
     :returns: string error message
    '''
    def getMessage(self):
        return self.error + ": '" + self.input + "'"

    def __repr__(self):
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
     :returns: integer het huisnummer van dit element
    '''
    def getHuisnummer(self):
        return self.getData(0)

    '''
     :param nummer: integer het nieuwe huisnummer van dit element
    '''
    def setHuisnummer(self, nummer):
        self.setData(0, nummer)

'''
A simple housenumber. bijv: 13 of 15.
'''


class KVDUtil_HnrHuisnummer(KVDUtil_HnrEnkelElement):

    def __init__(self, nummer):
        KVDUtil_HnrEnkelElement.__init__(self, nummer)

    def __str__(self):
        return str(self.getHuisnummer())

'''
A housenumber with biselement. bijv "3/1" of "21/5"
'''


class KVDUtil_HnrBiselement(KVDUtil_HnrEnkelElement):

    def getBiselement(self):
        return str(self.getData(self.bisIndex))

'''
A housenumber with bisnummer. bijv "3/1" of "21/5"
'''


class KVDUtil_HnrBisnummer(KVDUtil_HnrBiselement):

    def __init__(self, huis, bis):
        self.bisIndex = 1
        KVDUtil_HnrBiselement.__init__(self, huis, bis)

    def __str__(self):
        return self.getHuisnummer() + "/" + self.getBiselement()

    '''
     :returns: integer
    '''
    def getBisnummer(self):
        return self.getBiselement()

'''
A housenumber with busnummer. bijv "3 bus 1" of "53 bus 5"
'''


class KVDUtil_HnrBusnummer(KVDUtil_HnrBiselement):

    def __init__(self, huis, bus):
        self.bisIndex = 3
        KVDUtil_HnrBiselement.__init__(self, huis, -1, -1, bus)

    def __str__(self):
        return self.getHuisnummer() + " bus " + self.getBiselement()

    def getBusnummer(self):
        return self.getBiselement()

'''
A housenumber with busletter. bijv "3 bus A" of "53 bus D"
 '''


class KVDUtil_HnrBusletter(KVDUtil_HnrBiselement):
    def __init__(self, huis, bus):
        self.bisIndex = 4
        KVDUtil_HnrBiselement.__init__(self, huis, -1, -1, -1, bus)

    def __str__(self):
        return self.getHuisnummer() + " bus " + self.getBiselement()

    def getBusletter(self):
        return self.getBiselement()

'''
A housenumber with bisletter. bijv "3A" of "53D"
'''


class KVDUtil_HnrBisletter(KVDUtil_HnrBiselement):

    def __init__(self, huis, bis):
        self.bisIndex = 2
        KVDUtil_HnrBiselement.__init__(self, huis, -1, bis)

    def __str__(self):
        return self.getHuisnummer() + self.getBiselement()

    def getBisletter(self):
        return self.getBiselement()

'''
Abstract class of all series of housenumbers.
'''


class KVDUtil_HnrReeksElement(KVDUtil_HnrEnkelElement):

    def getBegin(self):
        return self.getData(self.beginIndex)

    def setBegin(self, val):
        return self.setData(self.beginIndex, val)

    def getEinde(self):
        return self.getData(self.eindeIndex)

    def setEinde(self, val):
        return self.setData(self.eindeIndex, val)


'''
A series of housenumbers.
bijv "33, 35, 37" -> "33-37"
bijv "33, 34, 35, 36" -> "33-36"
bijv "32, 33, 34, 35, 36"-> "32, 33-36"
'''


class KVDUtil_HnrHuisnummerReeks(KVDUtil_HnrReeksElement):

    '''
     :param begin: Integer first housenumber of the series.
     :param einde: Integer last housenumber of the series.
    '''
    def __init__(self, begin, einde):
        self.beginIndex = 0
        self.eindeIndex = 5
        KVDUtil_HnrReeksElement.__init__(self, begin, -1, -1, -1, -1, einde)

    def __str__(self):
            return str(self.getBegin()) + "-" + str(self.getEinde())

    def isVolgReeks(self):
        pass

    def isSpringReeks(self):
        pass

    def setSprong(self, val):
        pass

    def split(self):
        r = list()
        begin = int(self.getBegin())
        einde = int(self.getEinde())
        if (begin - einde) % 2 == 0:
            jump = 2
        else:
            jump = 1
        i = begin
        while i <= einde:
            r.append(KVDUtil_HnrHuisnummer(str(i)))
            i += jump
        return r


'''
A series of bisnummers.
  bijv "33/1, 32/2, 33/3" -> "33/1-3"
'''


class KVDUtil_HnrBisnummerReeks(KVDUtil_HnrReeksElement):

    '''
     :param huis: Integer housenumber.
     :param begin: Integer the first bisnummer of the series.
     :param einde: Integer the last bisnummer of the series
    '''
    def __init__(self, huis, begin, einde):
        self.beginIndex = 1
        self.eindeIndex = 6
        KVDUtil_HnrReeksElement.__init__(
            self, huis, begin, -1, -1, -1, huis, einde)

    def __str__(self):
        return str(self.getHuisnummer()) + "/"
        + str(self.getBegin()) + "-" + str(self.getEinde())

    def split(self):
        r = list()
        i = self.getBegin()
        while i <= self.getEinde():
            r.append(KVDUtil_HnrBisnummer(self.getHuisnummer(), i))
            i += 1
        return r


'''
Een reeks van bisletters.
'''


class KVDUtil_HnrBisletterReeks(KVDUtil_HnrReeksElement):

    '''
    :param huis: Integer housenumber
    :param begin: Integer the first number of the series.
    :param einde: Integer the last number of the series.
    '''
    def __init__(self, huis, begin, einde):
        self.beginIndex = 2
        self.eindeIndex = 7
        KVDUtil_HnrReeksElement.__init__(
            self, huis, -1, begin, -1, -1, huis, -1, einde)

    def __str__(self):
        return self.getHuisnummer() + self.getBegin() + "-" + self.getEinde()

    def split(self):
        r = list()
        i = ord(self.getBegin())
        while i <= ord(self.getEinde()):
            r.append(KVDUtil_HnrBisletter(self.getHuisnummer(), chr(i)))
            i += 1
        return r


'''
 Een reeks van busnummers.
    bijv "33 bus 1, 32 bus 2, 33 bus 3" -> "33 bus 1-3"
'''


class KVDUtil_HnrBusnummerReeks(KVDUtil_HnrReeksElement):

    '''
    :param huis: Integer housenumber.
    :param begin: Integer the first number of the series.
    :param einde: Integer the last number of the series.
    '''
    def __init__(self, huis, begin, einde):
        self.beginIndex = 3
        self.eindeIndex = 8
        KVDUtil_HnrReeksElement.__init__(
            self, huis, -1, -1, begin, -1, huis, -1, -1, einde)

    def __str__(self):
        return str(self.getHuisnummer()) + " bus "
        + str(self.getBegin()) + "-" + str(self.getEinde())

    '''
    :returns: A list of :class: `KVDUtil_HnrBusnummer`.
    '''
    def split(self):
        r = list()
        i = self.getBegin()
        while i <= self.getEinde():
            r.append(KVDUtil_HnrBusnummer(self.getHuisnummer(), i))
        return r


'''
 Een reeks van busletters.
    bijv "33 bus A, 32 bus B, 33 bus C" -> "33 bus A-C"
'''


class KVDUtil_HnrBusletterReeks(KVDUtil_HnrReeksElement):
    '''
     :param huis: integer huisnummer
     :param begin: integer het eerste nummer van de reeks
     :param einde: integer het laatste nummer van de reeks
    '''
    def __init__(self, huis, begin, einde):
        self.beginIndex = 4
        self.eindeIndex = 9
        KVDUtil_HnrReeksElement.__init__(
            self, huis, -1, -1, -1, begin, huis, -1, -1, -1, einde)

    def __str__(self):
        return str(self.getHuisnummer()) + " bus "
        + str(self.getBegin()) + "-" + str(self.getEinde())

    '''
     :returns: A list of :class: `KVDUtil_HnrBusletter`
    '''
    def split(self):
        r = list()
        i = self.getBegin()
        while i <= self.getEinde():
            r.append(KVDUtil_HnrBusletter(self.getHuisnummer(), i))
            i += 1
        return r


'''
Klasse die een reeks van huisnummers kan interpreteren en deze rij kan
samenvatten. Bijvoorbeeld:
    "23 bus 5, 23 bus 6" -> Busnummerreeks "23 bus 5-6"
    "23", "24 bus 2" -> Huisnummer "23", Busnummer "24 bus 2"
    "25", "26", "27" -> Huisnummerreeks "25, 26-27"
'''


class KVDutil_SequenceReader():

    '''
    var array array van te verzamelen elementen.
    '''
    def __init__(self):
        self.input = int()
        self.pos = list()
        self.result = list()

    '''
    Leest een reeks van huisnummers, die telkens een nummer overslaan.
    :param reeks: A :class: `KVDUtil_HnrHuisnummerReeks` de reeks tot nu toe
    :returns:A :class: `KVDUtil_HnrHuisnummerReeks` de volledige reeks
    '''
    def ReadSpringReeks(self, reeks):
        while (
            (self.next() == "KVDUtil_HnrHuisnummer") and
            (self.content().getHuisnummer() == (reeks.getEinde() + 2))
        ):
            reeks.setEinde(reeks.getEinde() + 2)
        return reeks

    '''
    Leest een reeks van huisnummers, waar de nummers elkaar opvolgen.
    :param reeks: A :class: `KVDUtil_HnrHuisnummerReeks` de reeks tot nu toe
    :returns: A :class: `KVDUtil_HnrHuisnummerReeks` de volledige reeks
    '''
    def ReadVolgReeks(self, reeks):
        while (
            (self.next() == "KVDUtil_HnrHuisnummer") and
            (self.content().getHuisnummer() == (reeks/self.getEinde() + 1))
        ):
                reeks.setEinde(reeks.getEinde() + 1)
        return reeks

    '''
    Leest een reeks van huisnummers
    :param huisnummer: A :class: `KVDUtil_HnrHuisnummer` eerste element
        van de reeks
    :returns: A :class: `KVDUtil_HnrHuisnummerReeks` de volledige reeks
    '''
    def ReadHuisnummerReeks(self, huisnummer):
        reeks = KVDUtil_HnrHuisnummerReeks(
            huisnummer.getHuisnummer(),
            huisnummer.getHuisnummer()
        )

        if(self.next() != "KVDUtil_HnrHuisnummer"):
            return huisnummer
        nummer = self.content().getHuisnummer()
        if(nummer == (reeks.getEinde()+1)):
            reeks.setSprong(false)
            reeks.setEinde(nummer)
            return self.ReadVolgReeks(reeks)
        if (nummer == (reeks.getEinde()+2)):
            reeks.setEinde(nummer)
            return self.ReadSpringReeks(reeks)
        return huisnummer

    '''
    Leest een reeks van bisnummers
    :param bisnummer: A :class: `KVDUtil_HnrBisnummer` eerste nummer
        van de reeks
    :returns: A :class: `KVDUtil_HnrBisnummerReeks` de volledige reeks
    '''
    def ReadBisnummerReeks(self, bisnummer):
        reeks = KVDUtil_HnrBisnummerReeks(
            bisnummer.getHuisnummer(),
            bisnummer.getBisnummer(),
            bisnummer.getBisnummer()
        )
        while(
            (self.next() == "KVDUtil_HnrBisnummer") and
            (self.content().getBisnummer() == (reeks.getEinde() + 1))
        ):
            reeks.setEinde(reeks.getEinde() + 1)
        if(reeks.getBegin() == reeks.getEinde()):
            return bisnummer
        else:
            return reeks

    '''
    Leest een reeks van busnummers
    :param busnummer: A :class: `KVDUtil_HnrBusnummer` eerste nummer
        van de reeks
    :returns: A :class: `KVDUtil_HnrBusnummerReeks` de volledige reeks
    '''
    def ReadBusnummerReeks(self, busnummer):
        reeks = KVDUtil_HnrBusnummerReeks(
            busnummer.getHuisnummer(),
            busnummer.getBusnummer(),
            busnummer.getBusnummer()
        )
        while(
            (self.next() == "KVDUtil_HnrBusnummer") and
            (self.content().getBusnummer() == (reeks.getEinde() + 1))
        ):
            reeks.setEinde(reeks.getEinde() + 1)
        if(reeks.getBegin() == reeks.getEinde()):
            return busnummer
        else:
            return reeks

    '''
    Leest een reeks van busletters
    :param busletter: A :class: `KVDUtil_HnrBusletter` eerste nummer
        van de reeks
    :returns: A :class: `KVDUtil_HnrBusletterReeks` de volledige reeks
    '''
    def ReadBusletterReeks(self, busletter):
        reeks = KVDUtil_HnrBusletterReeks(
            busletter.getHuisletter(),
            busletter.getBusletter(),
            busletter.getBusLetter()
        )
        einde = reeks.getEinde()
        while(
            ((self.next() == "KVDUtil_HnrBusletter") and
                self.content().getBusletter() == (einde + 1))
        ):
            reeks.setEinde(einde)
        if(reeks.getBegin() == reeks.getEinde()):
            return busletter
        else:
            return reeks

    '''
    Leest een reeks van bisletters
    :param bisletter: A :class: `KVDUtil_HnrBisletter` eerste nummer
        van de reeks
    :returns: A :class: `KVDUtil_HnrBisletterReeks` de volledige reeks
    '''
    def ReadBisletterReeks(self, bisletter):
        reeks = KVDUtil_HnrBisletterReeks(
            bisletter.getHuisnummer(),
            bisletter.getBisletter(),
            bisletter.getBisletter()
        )
        einde = reeks.getEinde()
        while(
            (self.next() == "KVDUtil_HnrBisletter") and
            (self.content().getBisletter() == (einde + 1))
        ):
            reeks-setEinde(einde)
        if(reeks.getBegin() == reeks.getEinde()):
            return bisletter
        else:
            return reeks

    def skip(self):
        element = self.content()
        self.next()
        return element

    '''
    Leest een reeks van huisnummers, ongeacht hun type, uit de input array.
    :returns: A :class: `KVDUtil_HnrReeksElement` de volledige reeks
    '''
    def ReadReeks(self):
        x = self.current()
        if x == "KVDUtil_HnrHuisnummer":
            return self.readHuisnummerReeks(self.content())
        elif x == "KVDUtil_HnrBisnummer":
            return self.readBisnummerReeks(self.content())
        elif x == "KVDUtil_HnrBusnummer":
            return self.readBusnummerReeks(self.content())
        elif x == "KVDUtil_HnrBusletter":
            return self.readBusletterReeks(self.content())
        elif x == "KVDUtil_HnrBisletter":
            return self.readBisletterReeks(self.content())
        elif x == "KVDUtil_HnrReadException":
            return self.skip()
        elif x == "":
            return null
        else:
            raise Exception(
                "Invalid type: " + selfcurrent() + " is of type: '"
                + get_class(self.current()) + "'")

    '''
    Leest een array van te verzamelen elementen in.
    :param in: A :class: list de input array
    :returns: A :class: `KVDUtil_HnrReeksElement` de volledige reeks
    '''
    def Read(self, inp):
        self.input = inp
        self.pos = 0
        while(self.current() != ""):
            r = self.readReeks()
            self.store(r)
        return self.result

    '''
    geeft het volgende element in de input array terug
    :returns: A :class: `KVDUtil_HnrElement`
    '''
    def next(self):
        self.pos += 1
        return self.current()

    '''
    geeft het huidige element in de input array terug
    :returns: A :class: `KVDUtil_HnrElement`
    '''
    def current(self):
        if self.pos >= sizeof(self.input):
            return ""
        else:
            return get_class(self.input[self.pos])

    '''
    geeft de inhoud van huidige element in de input array terug
    :returns: string
    '''
    def content(self):
        return self.input[self.pos]

    '''
    slaat het gevormde reeks element op.
    :param content: het resultaat
    '''
    def store(self, content):
        self.result = content


'''
Klasse die een reeks huisnummers inleest. Bijvoorbeeld:
    "23 bus 5, 23 bus 6" -> array (Busnummer "23 bus 5", Busnummer "23 B-6")
    "23", "24 bus 2" -> array (Huisnummer "23", Busnummer "24 bus 2")
    "25-27" -> array(Huisnummerreeks "25, 26-27")
'''


class KVDutil_HnrReader():

    def __init__(self, flag):
        self.flag = flag

    '''
    :param input: A :class: `String`.
    :param flag: A :class: `Integer` flag voor error handling.
    :returns: A list from of the input.
    '''
    def readString(self, input, flag=1):
        return self.readArray(str(input).split(","), flag)

    '''
    :param inputs: A String containing representations of housenumberobjects
        and/or housenumber series objects.
    :param flag: A :class: `Integer` flag voor error handling.
    :returns: A list of :class: `KVDUtil_HnrEnkelElement` and/or
        :class: `KVDUtil_HnrReeksElement`.
    '''
    def readArray(self, inputs, flag=1):
        result = list()
        for input in inputs:
            input = input.strip()
            element = self.readNummer(input)
            if element.isException():
                self.handleException(element, result, flag)
            else:
                result.append(element)
        return result

    '''
    :param input: A list of housenumber representations.
    :returns: A :class: `KVDUtil_HnrElement` OR
        an exception in case of incorrect input.
    '''
    def readNummer(self, input):
        if '-' in input:
            if 'bus' in input:
                input = input.split()
                huis = input[0]
                input = input[2].split('-')
                if input[0].isdigit():
                    return KVDUtil_HnrBusnummerReeks(huis, input[0], input[1])
                else:
                    return KVDUtil_HnrBusletterReeks(huis, input[0], input[1])
            elif '/' in input:
                input = input.split('/')
                huis = input[0]
                input = input[1]
                input = input.split('-')
                return KVDUtil_HnrBisnummerReeks(huis, input[0], input[1])
            else:
                input = input.split('-')
                input[0] = input[0].strip()
                input[1] = input[1].strip()
                if input[0].isdigit() and input[1].isdigit():
                    return KVDUtil_HnrHuisnummerReeks(input[0], input[1])
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
            if len(input) == 1:
                return KVDUtil_HnrBisletter('', input)
            else:
                letter = input[-1:]
                input = input[:-1]
                if (type(letter) == str) and input.isdigit():
                    return KVDUtil_HnrBisletter(input, letter)
                else:
                    return KVDUtil_HnrReadException(
                        "Could not parse/understand",
                        input)

    def handleException(self, exception, results=list(), flag=1):
        '''
        switch($flag) {
            case (KVDutil_HnrReader::ERR_EXCEPTIONS): throw new Exception($exception->getMessage()); break;
            case (KVDutil_HnrReader::ERR_IGNORE_INVALID_INPUT): $results[] = $exception; return $results; break;
            case (KVDutil_HnrReader::ERR_REMOVE_INVALID_INPUT): return $results; break;
            default: throw new Exception("Invalid flag for KVDutil_HnrReader. Given ".$flag);
        '''

'''
Class which turns series of housenumbers into seperate housenumber objects.
'''


class KVDutil_HnrSpeedSplitter():
    '''
    :param input: A list of :class: `KVDUtil_HnrReeksElement`.
    :returns: A list of :class: `KVDUtil_HnrEnkelElement`.
    '''
    def split(self, input):
        r = []
        for i in input:
            if i.__class__ == KVDUtil_HnrBisnummerReeks:
                r.append(self.splitN(i))
            elif i.__class__ == KVDUtil_HnrBisletterReeks:
                r.append(self.splitL(i))
            elif i.__class__ == KVDUtil_HnrBusnummerReeks:
                r.append(self.splitN(i))
            elif i.__class__ == KVDUtil_HnrBusletterReeks:
                r.append(self.splitL(i))
            elif i.__class__ == KVDUtil_HnrHuisnummerReeks:
                r.append(self.splitHuisnummers(i))
            else:
                r.append(i)
            r = flatten(r)
        return r

    '''
     :param match: A list of :class: `KVDUtil_HnrHuisnummerReeks`
     :returns: A list of :class: `KVDUtil_HnrHuisnummer`
    '''
    def splitHuisnummers(self, match):
        begin = match.getBegin()
        einde = match.getEinde()
        if ((int(begin)-int(einde)) % 2) == 0:
            jump = 2
        else:
            jump = 1
        res = []
        i = int(begin)
        while i <= int(einde):
            res.append(KVDUtil_HnrHuisnummer(i))
            i += jump
        return res

    '''
    :param match: A list of :class: `KVDUtil_HnrBusnummerReeks`
    :returns: A list of :class: `KVDUtil_HnrBusnummer`
        OR
    :param match: A list of :class: `KVDUtil_HnrBisnummerReeks`
    :returns: A list of :class: `KVDUtil_HnrBisnummer`
    '''
    def splitN(self, match):
        begin = match.getBegin()
        einde = match.getEinde()
        huis = match.getHuisnummer()
        jump = 1
        res = []
        i = int(begin)
        while i <= int(einde):
            res.append(self.getClass(match)(huis, i))
            i += jump
        return res

    '''
    :param match: A list of :class: `KVDUtil_HnrBusletterReeks`
    :returns: A list of :class: `KVDUtil_HnrBusletter`
        OR
    :param match: A list of :class: `KVDUtil_HnrBisletterReeks`
    :returns: A list of :class: `KVDUtil_HnrBisletter`
    '''
    def splitL(self, match):
        begin = ord(match.getBegin())
        einde = ord(match.getEinde())
        huis = match.getHuisnummer()
        jump = 1
        res = []
        i = int(begin)
        while i <= int(einde):
            res.append(self.getClass(match)(huis, chr(i)))
            i += jump
        return res

    '''
    :param input: A :class: `KVDUtil_HnrReeksElement`.
    :results: Matching housenumber class
    '''
    def getClass(self, input):
        if input.__class__ == KVDUtil_HnrBisnummerReeks:
            return KVDUtil_HnrBisnummer
        if input.__class__ == KVDUtil_HnrBusnummerReeks:
            return KVDUtil_HnrBusnummer
        if input.__class__ == KVDUtil_HnrBusletterReeks:
            return KVDUtil_HnrBusletter
        if input.__class__ == KVDUtil_HnrBisletterReeks:
            return KVDUtil_HnrBisletter


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
        r = flatten(r)

        return r

    '''
    :param input: List of integers.
    :returns: List of :class: `KVDUtil_HnrHuisnummerReeks`(if possible)
        and :class: `KVDUtil_HnrHuisnummer`.
    '''
    def mergeHuisnummers(self, input):
        r = []
        input.sort()
        while len(input) > 1:
            for y in [1, 2]:
                begin = input[0]
                einde = input[0]
                while einde + y in input:
                    einde += y
                    input.remove(einde)
                if begin != einde:
                    r.append(KVDUtil_HnrHuisnummerReeks(begin, einde))
                    input.remove(begin)
        for x in input:
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
        for x in input:
            huis = x.getHuisnummer()
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
                z.append(x.__class__(y, r[y][0]))
        result.append(z)
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
        for x in input:
            huis = x.getHuisnummer()
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
                z.append(x.__class__(y, begin))
        result.append(z)
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
Deze class dient om huisnummerlabels uit te splitsen
naar de indivduele labels of van individuele labels
terug samen te voegen naar een compactere notatie bv.:
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
        self.sequencer = KVDutil_SequenceReader()
        self.reader = KVDutil_HnrReader(self.flag)
        self.speedsplitter = KVDutil_HnrSpeedSplitter()
        self.speedmerger = KVDutil_HnrSpeedMerger()

    '''
    :param input: string of housenumber and/or
        housenumber series representations
    :returns: A list of :class: `KVDUtil_HnrEnkelElement`
    '''
    def split(self, input):
        nummers = self.stringToNummers(input)
        reeks = self.speedsplitter.split(nummers)
        return reeks

    '''
    :param input: string of housenumber and/or
        housenumber series representations.
    :returns: A list of housenumber and/or housenumber series representations.
    '''
    def stringToNummers(self, input):
        return self.reader.readString(input, self.flag)

    '''
    :param input: A list of housenumber and/or
        housenumber series representations.
    :returns: A list of :class: `KVDUtil_HnrEnkelElement`
    '''
    def merge(self, input):
        reeksen = self.stringToNummers(input)
        nummers = self.speedsplitter.split(reeksen)
        result = self.speedmerger.group(nummers)
        return result
