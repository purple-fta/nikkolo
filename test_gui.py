from lib.test_gui import *
import pygame
import pygame.gfxdraw
import math


pygame.init()


# Color theme
COLORS = {
    "BG": (40, 42, 54),
    "FG": (248, 248, 242),
    "LINE": (68, 71, 90),
    "COMM": (98, 114, 164),
    "GREEN": (80, 250, 123),
    "PURPLE": (189, 147, 249),
    "YELLOW": (241, 250, 140),
    "RED": (255, 85, 85),
    "PINK": (255, 121, 198),
}

# Used fonts
font_title = pygame.font.SysFont("jetbrainsmononfm", 25)
font_small = pygame.font.SysFont("jetbrainsmononfm", 14)

CREATE_PROVINCES = 1
SELECT_PROVINCE_TYPE_OPTIONS = 2
SELECT_PROVINCE_IS_SUPPLY_CENTER_OPTIONS = 3
CREATE_TRANSITION = 4
SELECT_SECOND_PROVINCE_FOR_CREATE_TRANSITION = 5
SELECT_PROVINCE_WITH_UNIT = 6
SELECT_UNIT_FOR_CREATE_MOVE = 7
SELECT_PROVINCE_FOR_CREATE_MOVE = 8
APPLYING_MOVES = 8
game_stage = CREATE_PROVINCES

game_manager = GameManager()

map_surface = pygame.image.load("game_maps/image.png")  # Map image

# Initializing the window with map file sizes, but 42px higher for the top section
screen = pygame.display.set_mode((map_surface.get_width(), map_surface.get_height()+42))

map_surface = map_surface.convert()  # Convert map image


# Rect for button. Used to draw the button and calculate the collision with the cursor
button_next_rect = pygame.Rect(map_surface.get_width()-160, 5, 100, 30)

clock = pygame.time.Clock()

type_of_province_to_created = ProvinceType.land.value
is_supply_center_of_province_to_created = False
coordinate_of_province_to_created = None

selected_provinces_for_create_transition = None

selected_unit_for_create_move = None
selected_province_for_create_move = None

provinces = []

def init_map():
    provinces.append(GuiProvince("0", ProvinceType.land.value, (80, 100), False))
    provinces.append(GuiProvince("1", ProvinceType.land.value, (330, 100), False))
    provinces.append(GuiProvince("2", ProvinceType.land.value, (80, 250), False))
    provinces.append(GuiProvince("3", ProvinceType.land.value, (330, 250), False))
    provinces.append(GuiProvince("4", ProvinceType.land.value, (160, 350), False))
    provinces.append(GuiProvince("5", ProvinceType.land.value, (70, 440), False))
    provinces.append(GuiProvince("6", ProvinceType.land.value, (240, 410), False))
    provinces.append(GuiProvince("7", ProvinceType.land.value, (520, 230), False))
    provinces.append(GuiProvince("8", ProvinceType.land.value, (435, 385), False))

    game_manager.add_province(provinces[0], [provinces[1], provinces[2]])
    game_manager.add_province(provinces[1], [provinces[2], provinces[3], provinces[7]])
    game_manager.add_province(provinces[2], [provinces[3], provinces[4]])
    game_manager.add_province(provinces[3], [provinces[2], provinces[4], provinces[7]])
    game_manager.add_province(provinces[4], [provinces[5], provinces[6]])
    game_manager.add_province(provinces[5], [provinces[6]])
    game_manager.add_province(provinces[6], [provinces[3], provinces[8]])
    game_manager.add_province(provinces[7], [provinces[8]])
    game_manager.add_province(provinces[8], [provinces[3]])

    u1 = Unit(provinces[3])
    u2 = Unit(provinces[4])
    u3 = Unit(provinces[5])
    u4 = Unit(provinces[6])

    game_manager.add_unit(u1)
    game_manager.add_unit(u2)
    game_manager.add_unit(u3)
    game_manager.add_unit(u4)

    m1 = Move(u1, provinces[6])
    game_manager.add_move(m1)
    game_manager.add_move(SupportMove(u2, provinces[6], m1))
    game_manager.add_move(SupportHold(u3, provinces[6], u4))

def print_fps():
    """
        Draw FPS on the screen
    """
    pygame.draw.rect(screen, COLORS["BG"], (screen.get_width()-55, 0, 55, 35))
    screen.blit(font_small.render(str(round(clock.get_fps(), 2)), True, COLORS["FG"]), (screen.get_width()-50, 5))

def print_title(text: str):
    pygame.draw.rect(screen, COLORS["BG"], (0, 0, map_surface.get_width()-160, 40))
    screen.blit(font_title.render(text, True, COLORS["FG"]), (5, 5))

def print_map():
    screen.blit(map_surface, (0, 41))

def print_button_next():
    pygame.draw.rect(screen, COLORS["GREEN"], button_next_rect, border_radius=12)   
    screen.blit(font_title.render("ДАЛЕЕ", True, COLORS["BG"]), (map_surface.get_width()-148, 3))

def print_provinces_on_map():
    for province in game_manager.provinces_graph:
        pygame.draw.circle(screen, COLORS["COMM"], province.coordinates, 5)
        province_type_string = ""
        if province.province_type == ProvinceType.land.value:
            province_type_string = ProvinceType.land.name
        if province.province_type == ProvinceType.coast.value:
            province_type_string = ProvinceType.coast.name
        if province.province_type == ProvinceType.water.value:
            province_type_string = ProvinceType.water.name
        print_choose_province_options(province.coordinates, f"{province.name}, {province_type_string}, {province.is_supply_center}") # {province.protection}")

def print_transitions_on_map():
    for first_province in game_manager.provinces_graph:
        for second_province in game_manager.provinces_graph[first_province]:
            pygame.draw.aaline(screen, COLORS["YELLOW"], first_province.coordinates, second_province.coordinates)

def print_units_on_map():
    for unit in game_manager.units:
        pygame.draw.circle(screen, COLORS["RED"], unit.location.coordinates, 10)

def print_moves_on_map():
    colors = {
        Move: COLORS["RED"],
        SupportMove: COLORS["YELLOW"],
        SupportHold: COLORS["GREEN"],
    }

    for move in game_manager.moves:
        pygame.draw.aaline(screen, colors[type(move)], move.unit.location.coordinates, move.target.coordinates)

def change_game_stage(new_game_stage):
    global game_stage

    game_stage = new_game_stage

def get_collide_province(coordinates):
    for province in game_manager.provinces_graph:
        if math.sqrt( (province.coordinates[0]-coordinates[0])**2 + (province.coordinates[1]-coordinates[1])**2 ) < 15:
            return province

def get_collide_unit(coordinates):
    for unit in game_manager.units:
        if math.sqrt( (unit.location.coordinates[0]-coordinates[0])**2 + (unit.location.coordinates[1]-coordinates[1])**2 ) < 15:
            return unit

def event_processing():
    global type_of_province_to_created, is_supply_center_of_province_to_created, coordinate_of_province_to_created, \
           selected_provinces_for_create_transition, selected_unit_for_create_move, selected_province_for_create_move

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the left mouse button is pressed
            if event.button == 1:
                # If next button pressed
                if button_next_rect.collidepoint(event.pos):
                    if game_stage == CREATE_PROVINCES:
                        change_game_stage(CREATE_TRANSITION)
                        print_title("Выберете соседнии провинции")
                    elif game_stage == CREATE_TRANSITION:
                        change_game_stage(SELECT_PROVINCE_WITH_UNIT)
                        print_title("Выберете провинции с армией")
                    elif game_stage == SELECT_PROVINCE_WITH_UNIT:
                        change_game_stage(SELECT_UNIT_FOR_CREATE_MOVE)
                        print_title("Создайте ходы")
                    elif game_stage == SELECT_UNIT_FOR_CREATE_MOVE or game_stage == SELECT_PROVINCE_FOR_CREATE_MOVE:
                        change_game_stage(SELECT_UNIT_FOR_CREATE_MOVE)
                        game_manager.applying_moves()
                        print_map()
                        print_provinces_on_map()
                        print_moves_on_map()
                        #print_transitions_on_map()
                        print_units_on_map()
                        
                
                # If clicked in the map area
                elif pygame.Rect(0, 41, map_surface.get_width(), map_surface.get_height()).collidepoint(event.pos):

                    if game_stage == CREATE_PROVINCES:
                        change_game_stage(SELECT_PROVINCE_TYPE_OPTIONS)
                        pygame.draw.circle(screen, COLORS["COMM"], event.pos, 5)
                        coordinate_of_province_to_created = event.pos

                    if game_stage == SELECT_PROVINCE_TYPE_OPTIONS:
                        print(coordinate_of_province_to_created)
                        print_choose_province_options(coordinate_of_province_to_created, "1-land 2-coast 3-water")

                    if game_stage == CREATE_TRANSITION:
                        selected_provinces_for_create_transition = get_collide_province(event.pos)
                        pygame.gfxdraw.aacircle(screen, selected_provinces_for_create_transition.coordinates[0], selected_provinces_for_create_transition.coordinates[1], 5, COLORS["PINK"])
                        change_game_stage(SELECT_SECOND_PROVINCE_FOR_CREATE_TRANSITION)

                    elif game_stage == SELECT_SECOND_PROVINCE_FOR_CREATE_TRANSITION:
                        game_manager.add_transition(selected_provinces_for_create_transition, get_collide_province(event.pos))
                        pygame.draw.aaline(screen, COLORS["YELLOW"], selected_provinces_for_create_transition.coordinates, get_collide_province(event.pos).coordinates)
                        change_game_stage(CREATE_TRANSITION)
                        selected_provinces_for_create_transition = None

                    elif game_stage == SELECT_PROVINCE_WITH_UNIT:
                        game_manager.add_unit(Unit(get_collide_province(event.pos)))
                        pygame.draw.circle(screen, COLORS["RED"], get_collide_province(event.pos).coordinates, 10)
                    
                    elif game_stage == SELECT_UNIT_FOR_CREATE_MOVE:
                        selected_unit_for_create_move = get_collide_unit(event.pos)
                        pygame.draw.circle(screen, COLORS["PINK"], get_collide_province(event.pos).coordinates, 15)
                        change_game_stage(SELECT_PROVINCE_FOR_CREATE_MOVE)
                    
                    elif game_stage == SELECT_PROVINCE_FOR_CREATE_MOVE:
                        selected_province_for_create_move = get_collide_province(event.pos)

                        game_manager.add_move(Move(selected_unit_for_create_move, selected_province_for_create_move))

                        print_map()
                        
                        selected_unit_for_create_move = None
                        selected_province_for_create_move = None

                        print_provinces_on_map()
                        #print_transitions_on_map()
                        print_units_on_map()
                        print_moves_on_map()

                        change_game_stage(SELECT_UNIT_FOR_CREATE_MOVE)


        if event.type == pygame.KEYDOWN:
            if game_stage == SELECT_PROVINCE_TYPE_OPTIONS:
                if event.key == pygame.K_1:
                    type_of_province_to_created = ProvinceType.land.value
                elif event.key == pygame.K_2:
                    type_of_province_to_created = ProvinceType.coast.value
                elif event.key == pygame.K_3:
                    type_of_province_to_created = ProvinceType.water.value
                
                change_game_stage(SELECT_PROVINCE_IS_SUPPLY_CENTER_OPTIONS)

                print_map()
                print_provinces_on_map()
                pygame.draw.circle(screen, COLORS["COMM"], coordinate_of_province_to_created, 5)
                print_choose_province_options(coordinate_of_province_to_created, "1-SC 2-not SC")
            
            elif game_stage == SELECT_PROVINCE_IS_SUPPLY_CENTER_OPTIONS:
                if event.key == pygame.K_1:
                    is_supply_center_of_province_to_created = True
                elif event.key == pygame.K_2:
                    is_supply_center_of_province_to_created = False
                
                change_game_stage(CREATE_PROVINCES)

                game_manager.add_province(GuiProvince("", type_of_province_to_created, coordinate_of_province_to_created, is_supply_center_of_province_to_created), [])

                print_map()
                print_provinces_on_map()

def print_choose_province_options(province_coordinates, text):
    surface = font_small.render(text, True, COLORS["BG"])
    screen.blit(surface, (province_coordinates[0]-surface.get_width()/2, province_coordinates[1]+20))


# Shading the window to the background color
screen.fill(COLORS["BG"])

init_map()
print_map()
print_button_next()
print_provinces_on_map()
#print_transitions_on_map()
print_units_on_map()
print_moves_on_map()
print_title("Выберете провинции")

# Main loop
while True:
    event_processing()

    clock.tick(75)

    print_fps()

    pygame.display.update()
