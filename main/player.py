class Player():
    def __init__(self):
        self.ships = set()

    def set_ships(self, ships):
        self.ships = ships

    def remove_ship(self, ship):
        self.ships.remove(ship)

    def delete_empty_ships(self):
        for ship in self.ships:
            if not ship:
                self.ships.remove(ship)
                break

    def got_ship_hit(self, point: list):
        for ship in self.ships:
            if point in ship:
                return True
        return False

    def remove_point_from_ship(self, coord: list):
        for ship in self.ships:
            if coord in ship:
                ship.remove(coord)
                break
