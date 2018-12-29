class Player():
    def __init__(self, name):
        self.name = name
        self.ships = set()

    def set_ships(self, ships):
        self.ships = ships

    def remove_ship(self, ship):
        self.ships.remove(ship)

    def delete_empty_ships(self):
        for ship in self.ships:
            if not ship:
                self.ships.remove(ship)
