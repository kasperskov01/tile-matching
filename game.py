import random
import pygame

class Game():
    def __init__(self):
        self.grid = [[random.randint(1,5) for y in range(0,10)] for x in range(0,10)]
        self.anim = [[0 for y in range(0,10)] for x in range(0,10)]
        self.points = 0
        self.load_sounds()
        print(self.grid)
        self.just_swapped = False

    def load_sounds(self):
        pygame.mixer.music.load('sounds/rabadab.wav')
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

        self.HUH_SOUND = pygame.mixer.Sound('sounds/huh.wav')
        self.HUH_SOUND.set_volume(0.5)
        # self.HUH_SOUND.set_endevent(HUH_SOUND_END)
        self.HUUH_SOUND = pygame.mixer.Sound('sounds/huuh.wav')
        self.HUUH_SOUND.set_volume(0.5)
        self.HEE_HEE_SOUND = pygame.mixer.Sound('sounds/hee_hee.wav')
        self.HEE_HEE_SOUND.set_volume(1)
        self.BAD_MOVE = pygame.mixer.Sound('sounds/bad_move.wav')
        self.BAD_MOVE.set_volume(1)
        self.AH = pygame.mixer.Sound('sounds/ah.wav')
        self.AH.set_volume(0.5)

    def build_grid(self):
        #import pdb; pdb.set_trace()        
        for x in range(0, len(self.grid)):
            for y in range(0, len(self.grid)):
                if self.grid[x][y] == 0:
                    if y < len(self.grid[x])-1 and not all(self.grid[x][yy] == 0 for yy in range(y, len(self.grid[x]))):
                        # Flyt kolonnen ned
                        while(self.grid[x][y] == 0):
                            self.grid[x][y:] = self.shift_column(self.grid[x][y:], 1)
                            self.anim[x][y:] = [50 for i in range(y,len(self.anim[x]))]
                    # Fyld op med nye tiles
                    num_points = 0
                    for fill in range(0,len(self.grid[x])):
                        if self.grid[x][fill] == 0:
                            num_points += 1
                            print("Added point")
                            self.grid[x][fill] = random.randint(1,5)
                    print("num_points: " + str(num_points))
                    self.add_points(num_points)

    def add_points(self, points):
        self.points += points
        if self.points % 50 == 0:
            self.HEE_HEE_SOUND.play()
            print("play hee hee")
        elif self.points % 10 == 0:
            self.HUUH_SOUND.play()
            print("play huuh")
        else:
            # Afspil lyd
            print("just_swapped: " + str(self.just_swapped))
            if self.just_swapped:
                print("play huh")
                self.just_swapped = False
                self.HUH_SOUND.play()
            else:
                print("play ah")
                self.AH.play()
        print(self.points)

    def shift_column(self, l, n):
        return l[n:] + l[:n]


    def swap_tiles(self, x1, y1, x2, y2):
        #Sørg for, at vi kun kan bytte naboceller.
        if abs(x1-x2) <= 1 and abs(y1-y2) <= 1:
            self.grid[x1][y1], self.grid[x2][y2] = self.grid[x2][y2], self.grid[x1][y1]


    def detect_matches(self, auto = False):
        got_match = False
        for x in range(1, len(self.grid)-1):
            for y in range(0, len(self.grid)):
                #Detect horizontal match
                if self.grid[x][y] == self.grid[x-1][y] and self.grid[x][y] == self.grid[x+1][y]:      
                    got_match = True
                    c = self.grid[x][y]

                    self.grid[x-1][y] = 0
                    self.grid[x][y] = 0
                    self.grid[x+1][y] = 0
                    x1 = x+2
                    while x1 < len(self.grid) and self.grid[x1][y] == c:
                        self.grid[x1][y] = 0
                        x1 += 1                
                    #Hvis vi har fjernet brikker, skal pladen fyldes igen
                    self.build_grid()
            
        for y in range(1, len(self.grid)-1):
            for x in range(0, len(self.grid)):
                #Detect vertical match
                if self.grid[x][y] == self.grid[x][y-1] and self.grid[x][y] == self.grid[x][y+1]:  
                    got_match = True                 
                    c = self.grid[x][y]

                    self.grid[x][y-1] = 0
                    self.grid[x][y] = 0
                    self.grid[x][y+1] = 0
                    y1 = y+2
                    while y1 < len(self.grid) and self.grid[x][y1] == c:
                        self.grid[x][y1] = 0
                        y1 += 1

                    #Hvis vi har fjernet brikker, skal pladen fyldes igen
                    self.build_grid()
        if not got_match and self.just_swapped:
            self.BAD_MOVE.play()