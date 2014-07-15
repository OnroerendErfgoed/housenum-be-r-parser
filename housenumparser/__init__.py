import abc
import re
from reader import Reader
from merger import Merger
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


class HuisnummerFacade():
    def __init__(self):
        self.reader = Reader()
        self.merger = Merger()

    '''
    :param input: string of housenumber and/or
        housenumber series representations
    :returns: A list of :class: `EnkelElement`
    '''
    def split(self, input, spring='', flag=1):
        nummers = self.stringToNummers(input, spring, flag)
        reeks = self.splitten(nummers)
        return self.flatten(reeks)

    '''
    :param input: string of housenumber and/or
        housenumber series representations.
    :returns: A list of housenumber and/or housenumber series representations.
    '''
    def stringToNummers(self, input, spring, flag):
        return self.reader.readString(input, spring, flag)

    '''
    :param input: A list of :class: `ReeksElement`.
    :returns: A list of :class: `EnkelElement`.
    '''
    def splitten(self, input):
        r = []
        for i in input:
            r.append(i.split())
        return r

    '''
    :param input: A list of housenumber and/or
        housenumber series representations.
    :returns: A list of :class: `EnkelElement`
    '''
    def merge(self, input, spring='', flag=1):
        reeksen = self.stringToNummers(input, spring, flag)
        nummers = self.splitten(reeksen)
        nummers = self.flatten(nummers)
        result = self.merger.group(nummers)
        return self.flatten(result)

    '''
    :param input: A nested list.
    :results: A list containing :class: `Element`.
    '''
    def flatten(self, input):
        r = []
        for x in input:
            if x .__class__ == list and x != []:
                for y in x:
                    if y is not None:
                        r.append(y)
            else:
                if x != [] and x is not None:
                    r.append(x)
        return r
