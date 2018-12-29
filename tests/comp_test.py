import unittest

from main.computer import Computer


class TestStringMethods(unittest.TestCase):

    def test_comp_ships(self):

        comp = Computer()
        comp.setBoard()

        for ship in comp.ships:
            for point in ship:
                self.assertTrue('J' >= point[0] >= 'A' and 10 >= point[1] >= 1)

    def test_comp_guess(self):
        comp = Computer()
        guess_point = comp.point_selection()
        self.assertTrue(9 >= guess_point[0] >= 0 and 10 >= guess_point[1] >= 1)


if __name__ == '__main__':
    unittest.main()
