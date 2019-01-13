import random

import pymongo as mg

myclient = mg.MongoClient("mongodb://localhost:27017/")

mydb = myclient["battleship"]
mycol = mydb["points"]

random.seed()

used_random_points = list()
used_points = list()


class Computer:
    def __init__(self):
        self.ships = list()
        self.hunt_mode = False
        self.player_ships = list()
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

    def get_all_points(self):
        self.ships = [x for y in self.ships for x in y]
        return self.ships

    def point_selection(self):
        random.seed()
        if not self.hunt_mode:
            point = []
            first = True

            while point in used_random_points or first:
                point = (random.randint(0, 9), random.randint(0, 9))
                first = False
        else:
            point = self.hunt_mode_selection()
        used_random_points.append(point)
        return point

    def goto_hunt_mode_selection(self, pointGuess):
        if not self.hunt_mode:
            max_ship = 0
            for ship in self.player_ships:
                if len(ship) > max_ship:
                    max_ship = len(ship)
            mydb["points"].remove({})
            pointsVG = [point for point in [(pointGuess[0], pointGuess[1] + i) for i in range(1, max_ship)] if
                        pointGuess[1] < point[1] <= 9]
            pointsVL = [point for point in [(pointGuess[0], pointGuess[1] + i) for i in range(1, -1 * (max_ship), -1)]
                        if
                        0 <= point[1] < pointGuess[1]]

            pointsHG = [point for point in [(pointGuess[0] + i, pointGuess[1]) for i in range(1, max_ship)] if
                        pointGuess[0] < point[0] <= 9]
            pointsHL = [point for point in [(pointGuess[0] + i, pointGuess[1]) for i in range(1, -1 * (max_ship), -1)]
                        if
                        0 <= point[0] < pointGuess[0]]

            if pointsVG and pointsVG[0] not in used_random_points:
                mydb["points"].insert({"name": "VG", "points": pointsVG})

            if pointsVL and pointsVL[0] not in used_random_points:
                mydb["points"].insert({"name": "VL", "points": pointsVL})

            if pointsHG and pointsHG[0] not in used_random_points:
                mydb["points"].insert({"name": "HG", "points": pointsHG})

            if pointsHL and pointsHL[0] not in used_random_points:
                mydb["points"].insert({"name": "HL", "points": pointsHL})

    def hunt_mode_selection(self):

        self.player_ships = [point for ship in self.player_ships for point in ship]
        if not list(mydb["points"].find({})):
            self.hunt_mode = False
            return self.point_selection()

        points = mydb["points"].find_one({}, {'_id': 0})

        while len(points["points"]) == 0:
            mydb["points"].remove({"name": points["name"]})
            points = mydb["points"].find_one({}, {'_id': 0})
            if not points:
                return self.point_selection()

        point = tuple(points["points"].pop(0))

        mydb["points"].update_one({"name": points["name"]}, {"$set": {"points": points["points"]}})

        if point not in self.player_ships:
            mydb["points"].remove({"name": points["name"]})
        if point in self.player_ships:
            if points["name"] in ["VG", "VL"]:
                mydb["points"].remove({"name": "HG"})
                mydb["points"].remove({"name": "HL"})
            else:
                mydb["points"].remove({"name": "VG"})
                mydb["points"].remove({"name": "VL"})
            used_random_points.append((point[0] + 1, point[1] + 1))
            used_random_points.append((point[0] + 1, point[1] - 1))
            used_random_points.append((point[0] - 1, point[1] + 1))
            used_random_points.append((point[0] - 1, point[1] - 1))
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
