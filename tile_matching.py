import pygame
from game import Game

# Setup pygame
pygame.init()
screen_width = 800
screen_height = 620

reset_btn_x = screen_width - 125
reset_btn_y = screen_height - 65
reset_btn_width = 100
reset_btn_height = 40

screen = pygame.display.set_mode((screen_width, screen_height))#, pygame.FULLSCREEN)
myfont = pygame.font.SysFont("monospace", 20)
clock = pygame.time.Clock()

# Initialize game variables
done = False
game = Game()
current_tile = (3,3)

# tile vars
tile_colors = [(0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255)]
tile_offset = [280,530]
tile_size = [50,50]


def draw_game():
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,800,600))
    if current_tile is not None:
        t = abs((pygame.time.get_ticks() % 512) - 256) % 256
        c = (t,t,t)
        pygame.draw.rect(screen, c, pygame.Rect(tile_offset[0] + current_tile[0]*tile_size[0] - 3, tile_offset[1] - (current_tile[1]+1)*tile_size[1] - 3, tile_size[0], tile_size[1]))
    for y in range(0,len(game.grid)):
        for x in range(0,len(game.grid[y])):
            if game.anim[x][y] > 0:
                game.anim[x][y] -= 2
                if game.anim[x][y] == 0:
                    game.detect_matches(True)
            pygame.draw.rect(screen, tile_colors[game.grid[x][y]], pygame.Rect(tile_offset[0] + x*tile_size[0], tile_offset[1] - (y+1)*tile_size[1] - game.anim[x][y], tile_size[0]-5, tile_size[1]-5))

    # Tekst
    # Score
    screen.blit(myfont.render("Du har {} point".format(game.points), 0, (255,255,255)), (50,50))

    # Knapper
    # Reset
    pygame.draw.rect(screen, (255,100,100), pygame.Rect(reset_btn_x, reset_btn_y, reset_btn_width, reset_btn_height))
    screen.blit(myfont.render("Restart", 0, (255,255,255)), (reset_btn_x + 9, reset_btn_y + 8))


def pixels_to_cell(x,y):
    x1 = int((x - tile_offset[0])/tile_size[0])
    y1 = int((-y + tile_offset[1])/tile_size[1])
    return x1,y1

def cell_to_pixels(x,y):
    x1 = int(tile_offset[0] + x * tile_size[0])
    y1 = int(tile_offset[1] - y * tile_size[1])
    return x1,y1

def output_logic(tilstand):
    if tilstand == 1:
        draw_game()
    elif tilstand == 0:
        draw_menu()

def draw_menu():
    pass

tilstand = 1

#Main game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            done = True
        if tilstand == 0:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_s):
                tilstand = 1
        elif tilstand == 1:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_p):
                tilstand = 0



        #Håndtering af input fra mus
        if tilstand == 1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x_cell, y_cell = pixels_to_cell(pos[0],pos[1])
                print(pos, cell_to_pixels(x_cell,y_cell))
                if 0 <= x_cell < len(game.grid) and 0 <= y_cell < len(game.grid[0]):
                    if current_tile is None:
                        current_tile = (x_cell, y_cell)
                    else:
                        game.just_swapped = True
                        game.swap_tiles(x_cell, y_cell, current_tile[0], current_tile[1])

                        #Når der er byttet brikker, kan vi kontrollere om der er lavet et match
                        game.detect_matches()
                        current_tile = None

                if reset_btn_x <= pos[0] < reset_btn_x + reset_btn_width and reset_btn_y <= pos[1] < reset_btn_y + reset_btn_height:
                    print("Reset clicked")
                    game = Game()


    output_logic(tilstand)

    #pygame kommandoer til at vise grafikken og opdatere 60 gange i sekundet.
    pygame.display.flip()
    clock.tick(60)