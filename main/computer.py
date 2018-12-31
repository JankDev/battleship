import random

random.seed()

used_random_points = list()
used_points = list()


class Computer:
    def __init__(self):
        self.ships = list()
        used_points.clear()
        used_random_points.clear()

    def place_ship(self, length):
        temp_list = list()
        first = True
        while first or are_points_not_on_board(temp_list) or contains_point(temp_list):
            first = False
            temp_list.clear()
            vertical = bool(random.getrandbits(1))
            horizontal = bool(random.getrandbits(1))

            x = random.randint(0, 9)
            y = random.randint(0, 9)

            temp_list.append((x, y))
            if horizontal:
                if vertical:
                    for j in range(1, length):
                        temp_list.append((x + j, y))

                else:
                    for j in range(1, length):
                        temp_list.append((x - j, y))

            else:
                if vertical:
                    for j in range(1, length):
                        temp_list.append((x, y + j))

                else:
                    for j in range(1, length):
                        temp_list.append((x, y - j))

        for point in temp_list:
            used_points.append(point)
        for point in temp_list:
            add_near_points(point[0], point[1])

        return temp_list

    def set_board(self):
        self.ships.append(self.place_ship(2))
        self.ships.append(self.place_ship(2))
        self.ships.append(self.place_ship(3))
        self.ships.append(self.place_ship(4))
        self.ships.append(self.place_ship(5))

    def point_selection(self):
        random.seed()
        point = []
        first = True

        while point in used_random_points or first:
            point = (random.randint(0, 9), random.randint(0, 9))
            first = False

        used_random_points.append(point)
        return point

    def remove_empty_ships(self):
        for ship in self.ships:
            if not ship:
                self.ships.remove(ship)
                break

    def remove_point_from_ship(self, coord: list):
        for ship in self.ships:
            if coord in ship:
                ship.remove(coord)
                break

    def got_ship_hit(self, point):
        for ship in self.ships:
            if point in ship:
                return True
        return False


def add_near_points(x_coord, y_coord):
    used_points.append((x_coord + 1, y_coord + 1))
    used_points.append((x_coord - 1, y_coord - 1))
    used_points.append((x_coord + 1, y_coord))
    used_points.append((x_coord, y_coord + 1))
    used_points.append((x_coord - 1, y_coord))
    used_points.append((x_coord, y_coord - 1))
    used_points.append((x_coord + 1, y_coord - 1))
    used_points.append((x_coord - 1, y_coord + 1))


def contains_point(temp_list):
    for point in temp_list:
        if point in used_points:
            return True

    return False


def are_points_not_on_board(temp_list):
    for point in temp_list:
        if 9 < point[0] or 9 < point[1] or point[0] < 0 or point[1] < 0:
            return True

    return False
