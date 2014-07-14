import unittest

from housenum_be_r_parser import(
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
    HuisnummerFacade
)


class HuisnummerFacadeTests(unittest.TestCase):
    def setUp(self):
        self.facade = HuisnummerFacade()

    def tearDown(self):
        self.facade = None

    def test_split_een_nummer(self):
        label = '25'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(1, len(huisnummers))
        hnr = huisnummers[0]
        self.assertIsInstance(hnr, Huisnummer)
        self.assertEqual(str(hnr), '25')

    def test_split_nummer_met_letter_bisnummer(self):
        label = '25A'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(len(huisnummers), 1)
        hnr = huisnummers[0]
        self.assertIsInstance(hnr, Bisletter)
        self.assertEqual(str(hnr), '25A')

    def test_split_nummer_met_cijfer_bisnummer(self):
        label = '25/1'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(len(huisnummers), 1)
        hnr = huisnummers[0]
        self.assertIsInstance(hnr, Bisnummer)
        self.assertEqual(str(hnr), '25/1')

    def test_split_huisnummer_met_bisnummer_gescheiden_door_underscore(self):
        label = '111_1'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(len(huisnummers), 1)
        hnr = huisnummers[0]
        self.assertIsInstance(hnr, Bisnummer)
        self.assertEqual(str(hnr), '111/1')

    def test_split_nummer_met_busnummer(self):
        label = '25 bus 3'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(len(huisnummers), 1)
        hnr = huisnummers[0]
        self.assertIsInstance(hnr, Busnummer)
        self.assertEqual(str(hnr), '25 bus 3')

    def test_split_nummer_met_busletter(self):
        label = '25 bus A'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(len(huisnummers), 1)
        hnr = huisnummers[0]
        self.assertIsInstance(hnr, Busletter)
        self.assertEqual(str(hnr), '25 bus A')

    def test_huisnummer_reeks(self):
        label = '25,27,29,31'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(len(huisnummers), 4)
        self.assertEqual(str(huisnummers[0]), '25')
        self.assertEqual(str(huisnummers[1]), '27')
        self.assertEqual(str(huisnummers[2]), '29')
        self.assertEqual(str(huisnummers[3]), '31')

    def test_huisnummer_bereik_even_verschil(self):
        label = '25-31'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(len(huisnummers), 4)
        self.assertEqual(str(huisnummers[0]), '25')
        self.assertEqual(str(huisnummers[1]), '27')
        self.assertEqual(str(huisnummers[2]), '29')
        self.assertEqual(str(huisnummers[3]), '31')

    def test_huisnummer_bereik_oneven_verschil(self):
        label = '25-32'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(len(huisnummers), 8)
        self.assertEqual('25', str(huisnummers[0]))
        self.assertEqual('26', str(huisnummers[1]))
        self.assertEqual('27', str(huisnummers[2]))
        self.assertEqual('28', str(huisnummers[3]))
        self.assertEqual('29', str(huisnummers[4]))
        self.assertEqual('30', str(huisnummers[5]))
        self.assertEqual('31', str(huisnummers[6]))
        self.assertEqual('32', str(huisnummers[7]))

    def test_huisnummer_bereik_speciaal(self):
        label = '25,26-31'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(len(huisnummers), 7)
        self.assertEqual('25', str(huisnummers[0]))
        self.assertEqual('26', str(huisnummers[1]))
        self.assertEqual('27', str(huisnummers[2]))
        self.assertEqual('28', str(huisnummers[3]))
        self.assertEqual('29', str(huisnummers[4]))
        self.assertEqual('30', str(huisnummers[5]))
        self.assertEqual('31', str(huisnummers[6]))

    def test_combinatie_huisnummer_bereiken(self):
        label = '25-31,18-26'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(len(huisnummers), 9)
        self.assertEqual('25', str(huisnummers[0]))
        self.assertEqual('27', str(huisnummers[1]))
        self.assertEqual('29', str(huisnummers[2]))
        self.assertEqual('31', str(huisnummers[3]))
        self.assertEqual('18', str(huisnummers[4]))
        self.assertEqual('20', str(huisnummers[5]))
        self.assertEqual('22', str(huisnummers[6]))
        self.assertEqual('24', str(huisnummers[7]))
        self.assertEqual('26', str(huisnummers[8]))

    def test_busnummer_bereik(self):
        label = '25 bus 3-7'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(len(huisnummers), 5)
        self.assertEqual('25 bus 3', str(huisnummers[0]))
        self.assertEqual('25 bus 4', str(huisnummers[1]))
        self.assertEqual('25 bus 5', str(huisnummers[2]))
        self.assertEqual('25 bus 6', str(huisnummers[3]))
        self.assertEqual('25 bus 7', str(huisnummers[4]))

    def test_alfa_busnummer_bereik(self):
        label = '25 bus C-F'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(len(huisnummers), 4)
        self.assertEqual('25 bus C', str(huisnummers[0]))
        self.assertEqual('25 bus D', str(huisnummers[1]))
        self.assertEqual('25 bus E', str(huisnummers[2]))
        self.assertEqual('25 bus F', str(huisnummers[3]))

    def test_huisnummer_bereik_met_letter_bisnummer(self):
        label = '25C-F'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(len(huisnummers), 4)
        self.assertEqual('25C', str(huisnummers[0]))
        self.assertEqual('25D', str(huisnummers[1]))
        self.assertEqual('25E', str(huisnummers[2]))
        self.assertEqual('25F', str(huisnummers[3]))

    def test_huisnummer_bereik_met_cijfer_bisnummer(self):
        label = '25/3-7'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(5, len(huisnummers))
        self.assertEqual('25/3', str(huisnummers[0]))
        self.assertEqual('25/4', str(huisnummers[1]))
        self.assertEqual('25/5', str(huisnummers[2]))
        self.assertEqual('25/6', str(huisnummers[3]))
        self.assertEqual('25/7', str(huisnummers[4]))

    def test_combinatie_bereiken(self):
        label = '25C-F,28-32,29 bus 2-5'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(11, len(huisnummers))
        self.assertEqual('25C', str(huisnummers[0]))
        self.assertEqual('25D', str(huisnummers[1]))
        self.assertEqual('25E', str(huisnummers[2]))
        self.assertEqual('25F', str(huisnummers[3]))
        self.assertEqual('28', str(huisnummers[4]))
        self.assertEqual('30', str(huisnummers[5]))
        self.assertEqual('32', str(huisnummers[6]))
        self.assertEqual('29 bus 2', str(huisnummers[7]))
        self.assertEqual('29 bus 3', str(huisnummers[8]))
        self.assertEqual('29 bus 4', str(huisnummers[9]))
        self.assertEqual('29 bus 5', str(huisnummers[10]))

    def test_bisnummer_en_huisnummer_bereik(self):
        label = '2A,7-11'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(4, len(huisnummers))
        self.assertEqual('2A', str(huisnummers[0]))
        self.assertEqual('7', str(huisnummers[1]))
        self.assertEqual('9', str(huisnummers[2]))
        self.assertEqual('11', str(huisnummers[3]))

    def test_bogus_input(self):
        label = 'A,1/3,?'
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(3, len(huisnummers))
        self.assertEqual('A', str(huisnummers[0]))
        self.assertEqual('1/3', str(huisnummers[1]))
        self.assertEqual('?', str(huisnummers[2]))

    def test_input_with_spaces(self):
        label = ' A , 1/3 , 5 - 7 '
        huisnummers = self.facade.split(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(4, len(huisnummers))
        self.assertEqual('A', str(huisnummers[0]))
        self.assertEqual('1/3', str(huisnummers[1]))
        self.assertEqual('5', str(huisnummers[2]))
        self.assertEqual('7', str(huisnummers[3]))

    def test_merge_units(self):
        label = '32-36, 25-31, 1A-F, 2/1-10, 4 bus 1-30\
, 43, 44 bus 1, 45/1, 46A'
        huisnummers = self.facade.merge(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(9, len(huisnummers))
        self.assertEqual('25-31', str(huisnummers[0]))
        self.assertEqual('32-36', str(huisnummers[1]))
        self.assertEqual('43', str(huisnummers[2]))
        self.assertEqual('2/1-10', str(huisnummers[3]))
        self.assertEqual('45/1', str(huisnummers[4]))
        self.assertEqual('1A-F', str(huisnummers[5]))
        self.assertEqual('46A', str(huisnummers[6]))
        self.assertEqual('44 bus 1', str(huisnummers[7]))
        self.assertEqual('4 bus 1-30', str(huisnummers[8]))

    def test_merge_huisnummer_reeksen(self):
        label = '32, 34, 36, 38, 25, 27, 29, 31, 39\
, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50'
        huisnummers = self.facade.merge(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(4, len(huisnummers))
        self.assertEqual('25-31', str(huisnummers[0]))
        self.assertEqual('32-50', str(huisnummers[1]))
        self.assertEqual('39-43', str(huisnummers[2]))
        self.assertEqual('47-49', str(huisnummers[3]))

    def test_merge_combinatie_huisnummer_bereiken(self):
        label = '25-31, 18-26'
        huisnummers = self.facade.merge(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(2, len(huisnummers))
        self.assertEqual('18-26', str(huisnummers[0]))
        self.assertEqual('25-31', str(huisnummers[1]))

    def test_merge_bisnummer_bereiken(self):
        label = '10/1-3, 10/4, 15/3-7, 15/8-10'
        huisnummers = self.facade.merge(label)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(2, len(huisnummers))
        self.assertEqual('10/1-4', str(huisnummers[0]))
        self.assertEqual('15/3-10', str(huisnummers[1]))

    def test_split_huisnummers_with_spring_false(self):
        label = '10-12'
        spring = False
        huisnummers = self.facade.split(label, spring)
        self.assertIsInstance(huisnummers, list)
        self.assertEqual(3, len(huisnummers))
        self.assertEqual('10', str(huisnummers[0]))
        self.assertEqual('11', str(huisnummers[1]))
        self.assertEqual('12', str(huisnummers[2]))
