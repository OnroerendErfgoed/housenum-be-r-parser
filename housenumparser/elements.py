
'''
A housenumber element.
This is an abstract superclass for all output of the housenumberreader.
This can be a housenumber, a housenumber series, readingerror, etc.
'''


class Element():

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


class ReadException(Element):

    def __init__(self, error, input="", flag=1):
        self.error = error
        self.input = input
        self.flag = flag
        Element.__init__(self, -1)

    def isException(self):
        return True

    def split(self):
        if self.flag in [1, 2]:
            return self

    def __str__(self):
        if self.flag == 1:
            return self.input
        elif self.flag == 2:
            return self.error


'''
An abstract superclass for housenumbers.
'''


class EnkelElement(Element):

    def isException(self):
        return False

    def split(self):
        return self

    '''
     :returns: The housenumber attribute of the object.
    '''
    def getHuisnummer(self):
        return self.getData(0)

'''
A simple housenumber. eg: 13 of 15.
'''


class Huisnummer(EnkelElement):

    def __init__(self, nummer):
        EnkelElement.__init__(self, nummer)

    def __str__(self):
        return str(self.getHuisnummer())

'''
A housenumber with biselement. eg: "3/1" of "21/5"
'''


class Biselement(EnkelElement):

    def getBiselement(self):
        return str(self.getData(self.bisIndex))

'''
A housenumber with bisnummer. eg: "3/1" of "21/5"
'''


class Bisnummer(Biselement):

    def __init__(self, huis, bis):
        self.bisIndex = 1
        Biselement.__init__(self, huis, bis)

    def __str__(self):
        return str(self.getHuisnummer()) + "/" + self.getBiselement()


'''
A housenumber with busnummer. eg: "3 bus 1" of "53 bus 5"
'''


class Busnummer(Biselement):

    def __init__(self, huis, bus):
        self.bisIndex = 3
        Biselement.__init__(self, huis, -1, -1, bus)

    def __str__(self):
        return str(self.getHuisnummer()) + " bus " + self.getBiselement()

'''
A housenumber with busletter. eg: "3 bus A" of "53 bus D"
 '''


class Busletter(Biselement):
    def __init__(self, huis, bus):
        self.bisIndex = 4
        Biselement.__init__(self, huis, -1, -1, -1, bus)

    def __str__(self):
        return str(self.getHuisnummer()) + " bus " + self.getBiselement()

'''
A housenumber with bisletter. eg: "3A" of "53D"
'''


class Bisletter(Biselement):

    def __init__(self, huis, bis):
        self.bisIndex = 2
        Biselement.__init__(self, huis, -1, bis)

    def __str__(self):
        return str(self.getHuisnummer()) + self.getBiselement()


'''
Abstract class of all series of housenumbers.
'''


class ReeksElement(EnkelElement):

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


class HuisnummerReeks(ReeksElement):

    '''
     :param begin: First housenumber of the series.
     :param einde: Last housenumber of the series.
    '''
    def __init__(self, begin, einde, spring=''):
        self.beginIndex = 0
        self.eindeIndex = 5
        self.spring = spring
        ReeksElement.__init__(self, begin, -1, -1, -1, -1, einde)

    def __str__(self):
            return str(self.getBegin()) + "-" + str(self.getEinde())

    '''
     :param match: A list of :class: `HuisnummerReeks`
     :returns: A list of :class: `Huisnummer`
    '''
    def split(self):
        begin = self.getBegin()
        einde = self.getEinde()
        jump = self.jump()
        res = []
        i = int(begin)
        while i <= int(einde):
            res.append(Huisnummer(i))
            i += jump
        return res

'''
A series of bisnummers.
  eg: "33/1, 32/2, 33/3" -> "33/1-3"
'''


class BisnummerReeks(ReeksElement):

    '''
     :param huis: Integer housenumber.
     :param begin: Integer the first bisnummer of the series.
     :param einde: Integer the last bisnummer of the series
    '''
    def __init__(self, huis, begin, einde, spring=''):
        self.beginIndex = 1
        self.eindeIndex = 6
        self.spring = spring
        ReeksElement.__init__(
            self, huis, begin, -1, -1, -1, huis, einde)

    def __str__(self):
        return str(self.getHuisnummer()) + "/" +\
            str(self.getBegin()) + "-" + str(self.getEinde())

    '''
    :param match: A list of :class: `BisnummerReeks`
    :returns: A list of :class: `Bisnummer`
    '''
    def split(self):
        begin = self.getBegin()
        einde = self.getEinde()
        huis = self.getHuisnummer()
        jump = 1
        res = []
        i = int(begin)
        while i <= int(einde):
            res.append(Bisnummer(huis, i))
            i += jump
        return res

'''
A series of bisletters.
'''


class BisletterReeks(ReeksElement):

    '''
    :param huis: Integer housenumber
    :param begin: Integer the first number of the series.
    :param einde: Integer the last number of the series.
    '''
    def __init__(self, huis, begin, einde, spring=''):
        self.beginIndex = 2
        self.eindeIndex = 7
        self.spring = spring
        ReeksElement.__init__(
            self, huis, -1, begin, -1, -1, huis, -1, einde)

    def __str__(self):
        return str(self.getHuisnummer()) + self.getBegin() + "-"\
            + self.getEinde()

    '''
    :param match: A list of :class: `BisletterReeks`
    :returns: A list of :class: `Bisletter`
    '''
    def split(self):
        begin = ord(self.getBegin())
        einde = ord(self.getEinde())
        huis = self.getHuisnummer()
        jump = 1
        res = []
        i = int(begin)
        while i <= int(einde):
            res.append(Bisletter(huis, chr(i)))
            i += jump
        return res

'''
 Een reeks van busnummers.
    eg: "33 bus 1, 32 bus 2, 33 bus 3" -> "33 bus 1-3"
'''


class BusnummerReeks(ReeksElement):

    '''
    :param huis: Integer housenumber.
    :param begin: Integer the first number of the series.
    :param einde: Integer the last number of the series.
    '''
    def __init__(self, huis, begin, einde, spring=''):
        self.beginIndex = 3
        self.eindeIndex = 8
        self.spring = spring
        ReeksElement.__init__(
            self, huis, -1, -1, begin, -1, huis, -1, -1, einde)

    def __str__(self):
        return str(self.getHuisnummer()) + " bus " +\
            str(self.getBegin()) + "-" + str(self.getEinde())

    '''
    :param match: A list of :class: `BusnummerReeks`
    :returns: A list of :class: `Busnummer`
    '''
    def split(self):
        begin = self.getBegin()
        einde = self.getEinde()
        huis = self.getHuisnummer()
        jump = 1
        res = []
        i = int(begin)
        while i <= int(einde):
            res.append(Busnummer(huis, i))
            i += jump
        return res


'''
A series of busletters.
    eg: "33 bus A, 32 bus B, 33 bus C" -> "33 bus A-C"
'''


class BusletterReeks(ReeksElement):
    '''
     :param huis: integer huisnummer
     :param begin: integer het eerste nummer van de reeks
     :param einde: integer het laatste nummer van de reeks
    '''
    def __init__(self, huis, begin, einde, spring=''):
        self.beginIndex = 4
        self.eindeIndex = 9
        self.spring = spring
        ReeksElement.__init__(
            self, huis, -1, -1, -1, begin, huis, -1, -1, -1, einde)

    def __str__(self):
        return str(self.getHuisnummer()) + " bus "
        + str(self.getBegin()) + "-" + str(self.getEinde())

    '''
    :param match: A list of :class: `BisletterReeks`
    :returns: A list of :class: `Bisletter`
    '''
    def split(self):
        begin = ord(self.getBegin())
        einde = ord(self.getEinde())
        huis = self.getHuisnummer()
        jump = 1
        res = []
        i = int(begin)
        while i <= int(einde):
            res.append(Busletter(huis, chr(i)))
            i += jump
        return res
