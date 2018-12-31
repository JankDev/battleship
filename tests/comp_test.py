import unittest

from main.computer import Computer


class TestStringMethods(unittest.TestCase):

    def test_comp_ships(self):

        comp = Computer()
        comp.set_board()

        for ship in comp.ships:
            for point in ship:
                self.assertTrue(10 > (point[1] and point[0]) >= 0)

    def test_comp_guess(self):
        comp = Computer()
        guess_point = comp.point_selection()
        self.assertTrue(9 >= guess_point[0] >= 0 and 9 >= guess_point[1] >= 0)


if __name__ == '__main__':
    unittest.main()
