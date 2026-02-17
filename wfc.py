import random

# Tile definitions with sockets: [Top, Right, Bottom, Left]
TILE_DATA = {
    "HORIZ": {"sym": "═", "sockets": [0, 1, 0, 1]},
    "VERT":  {"sym": "║", "sockets": [1, 0, 1, 0]},
    "C_TL":  {"sym": "╔", "sockets": [0, 1, 1, 0]},
    "C_TR":  {"sym": "╗", "sockets": [0, 0, 1, 1]},
    "C_BL":  {"sym": "╚", "sockets": [1, 1, 0, 0]},
    "C_BR":  {"sym": "╝", "sockets": [1, 0, 0, 1]},
    "T_DN":  {"sym": "╦", "sockets": [0, 1, 1, 1]},
    "EMPTY": {"sym": "#", "sockets": [0, 0, 0, 0]}
}


class Tile():
    def __init__(self):
        self.collapsed = False
        self.chosen_tile = None
        self.possible_tiles = ['HORIZ', 'VERT', 'C_TL', 'C_TR', 'C_BL', 'C_BR', 'T_DN', 'EMPTY']
        
    def select_random_tile(self):
        print("Selecting random tile")
        total_possibilities = len(self.possible_tiles)
        randomly_selected_tile = self.possible_tiles[random.randint(0, total_possibilities - 1)]
        self.collapsed = True
        self.chosen_tile = randomly_selected_tile
        self.possible_tiles = [self.chosen_tile]
        
        
class Board():
    def __init__(self):
        self.height = 10
        self.width = 10
        self.tilemap = []
        self.neighbor_queue = []
        
        for i in range (0, self.height):
            row_i = []
            for j in range(0, self.width):
                row_i.append(Tile())
            self.tilemap.append(row_i)
    
    def tile_reduction(self, y, x, prevDir, prevElement):
        # prevDir is the direction that the previous tile came from
        # [Top (0), Right (1), Bottom (2), Left (3)]
            # if prevDir is from bottom:
                # We should check the prevTile top connection
                # Find other tiles whose bottom connection match prevTile's top connection
        # prevTile is the typle of prevTile
        
        # We have to check the connection of prevTile opposite to the direction that prevTile previously came from
        toCheck = [2, 3, 0, 1]
        
        possible_tiles = set()
        for prevTile in prevElement.possible_tiles:
            for tile in TILE_DATA:
                if((TILE_DATA[prevTile]["sockets"][toCheck[prevDir]] == TILE_DATA[tile]["sockets"][prevDir]) and tile in self.tilemap[y][x].possible_tiles):
                    possible_tiles.add(tile)
            
        # Successful Reduction
        if(len(possible_tiles) < len(self.tilemap[y][x].possible_tiles)):
            self.tilemap[y][x].possible_tiles = list(possible_tiles)
            return True
        else:
            return False
            
            
    def print_map(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                tile = self.tilemap[i][j]
                if tile.collapsed:
                    print(TILE_DATA[tile.chosen_tile]['sym'], end='')
                else:
                    print('?', end=' ')
            print()
            
    def ripple(self):
        print("ripple")
        while(self.neighbor_queue):
            y, x = self.neighbor_queue.pop(0)
            print("Checking: ", y, x)
            
            if(y-1 >= 0 and not self.tilemap[y-1][x].collapsed):
                # Check the one above
                if(self.tile_reduction(y-1, x, 2, self.tilemap[y][x])):
                    self.neighbor_queue.append((y-1, x))
            if(y+1 <self.height and not self.tilemap[y+1][x].collapsed):
                # Check the one below
                if(self.tile_reduction(y+1, x, 0, self.tilemap[y][x])):
                    self.neighbor_queue.append((y+1, x))
            if(x-1 >= 0 and not self.tilemap[y][x-1].collapsed):
                # Check the one to the left
                if(self.tile_reduction(y, x-1, 1, self.tilemap[y][x])):
                    self.neighbor_queue.append((y, x-1))
            if(x+1 < self.width and not self.tilemap[y][x+1].collapsed):
                # Check the one to the right
                if(self.tile_reduction(y, x+1, 3, self.tilemap[y][x])):
                    self.neighbor_queue.append((y, x+1))
                    
            print("Neighbor queue currently is ", self.neighbor_queue)
            
    def find_lowest_entropy(self):
        min_entropy = 99
        best_y = None
        best_x = None
        for i in range(0, self.height):
            for j in range(0, self.width):
                tile_being_checked = self.tilemap[i][j]
                if(tile_being_checked.collapsed):
                    continue
                if(len(tile_being_checked.possible_tiles) < min_entropy):
                    min_entropy = len(tile_being_checked.possible_tiles)
                    best_y = i
                    best_x = j
        
        return best_y, best_x
        
                    
    def randomized_start(self):
        randomY = random.randint(0, 9)
        randomX = random.randint(0, 9)
        self.tilemap[randomY][randomX].select_random_tile()
        self.neighbor_queue.append((randomY, randomX))
        self.ripple()
    
    def generate_map(self):
        self.randomized_start()
        while True:
            coords = self.find_lowest_entropy()
            if coords is None:
                print("Generation Complete!")
                break
            
            y, x = coords
            # Potential Bug
            if(y==None):
                return
            target_tile = self.tilemap[y][x]
            
            # CONTRADICTION CHECK:
            # If a tile has no valid options left, the map is "broken."
            if len(target_tile.possible_tiles) == 0:
                print(f"Contradiction at {y}, {x}! No valid tiles fit here.")
                return False
            
            target_tile.select_random_tile()
            
            self.neighbor_queue.append((y, x))
            self.ripple()
    
        
def main():
    generated_map = Board()
    generated_map.generate_map()
    generated_map.print_map()
    
    
    
if __name__ == "__main__":
    main()
        
