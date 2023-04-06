from lib.test_gui import *
import pygame
import math


pygame.init()

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

font = pygame.font.SysFont("jetbrainsmononfm", 25)
font_fps = pygame.font.SysFont("jetbrainsmononfm", 14)

game_map = GuiMap()
game_manager = GameManager(game_map)

map_surface = pygame.image.load("game_maps/image.png")

clock = pygame.time.Clock()

create_map_flag = True

provinces = []



screen = pygame.display.set_mode((map_surface.get_width(), map_surface.get_height()+42))
screen.fill(COLORS["BG"])
screen.blit(font.render("Выберете все регионы", True, COLORS["FG"]), (5, 5))
button_next_rect = pygame.Rect(map_surface.get_width()-160, 5, 100, 30)
pygame.draw.rect(screen, COLORS["GREEN"], button_next_rect, border_radius=12)
screen.blit(font.render("ДАЛЕЕ", True, COLORS["BG"]), (map_surface.get_width()-148, 3))
screen.blit(map_surface, (0, 41))
while create_map_flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            create_map_flag = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button_next_rect.collidepoint(event.pos):
                    create_map_flag = False
                else:
                    provinces.append(GuiProvince("NAME", ProvinceType.land.value, event.pos, False))
                    pygame.draw.circle(screen, COLORS["COMM"], event.pos, 5)

    pygame.draw.line(screen, COLORS["LINE"], (0, 40), (1280, 40), 3)

    #screen.blit(map_surface, (0, 41))

    pygame.draw.rect(screen, COLORS["BG"], (screen.get_width()-55, 0, 55, 35))
    clock.tick(75)
    screen.blit(font_fps.render(str(round(clock.get_fps(), 2)), True, COLORS["FG"]), (screen.get_width()-50, 5))
    
    pygame.display.update()



pygame.draw.rect(screen, COLORS["BG"], (0, 0, map_surface.get_width(), 40))
screen.blit(font.render("Выберете связи", True, COLORS["FG"]), (5, 5))
pygame.draw.rect(screen, COLORS["GREEN"], button_next_rect, border_radius=12)
screen.blit(font.render("ДАЛЕЕ", True, COLORS["BG"]), (map_surface.get_width()-148, 3))
selected_province = None
create_provinces_connections = True
while create_provinces_connections:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            create_provinces_connections = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button_next_rect.collidepoint(event.pos):
                    create_provinces_connections = False
                else:
                    for pr in provinces:
                        if math.sqrt( (pr.coordinates[0]-event.pos[0])**2 + (pr.coordinates[1]-event.pos[1])**2 ) < 15:
                            if selected_province is None:
                                selected_province = pr
                                pygame.draw.circle(screen, COLORS["PURPLE"], pr.coordinates, 5)
                            else:
                                pygame.draw.circle(screen, COLORS["COMM"], pr.coordinates, 5)
                                pygame.draw.circle(screen, COLORS["COMM"], selected_province.coordinates, 5)
                                pygame.draw.line(screen, COLORS["YELLOW"], pr.coordinates, selected_province.coordinates)
                                selected_province = None

    pygame.draw.line(screen, COLORS["LINE"], (0, 40), (1280, 40), 3)

    pygame.draw.rect(screen, COLORS["BG"], (screen.get_width()-55, 0, 55, 35))
    clock.tick(75)
    screen.blit(font_fps.render(str(round(clock.get_fps(), 2)), True, COLORS["FG"]), (screen.get_width()-50, 5))
    
    pygame.display.update()



pygame.draw.rect(screen, COLORS["BG"], (0, 0, map_surface.get_width(), 40))
screen.blit(font.render("Выберете места для армий", True, COLORS["FG"]), (5, 5))
pygame.draw.rect(screen, COLORS["GREEN"], button_next_rect, border_radius=12)
screen.blit(font.render("ДАЛЕЕ", True, COLORS["BG"]), (map_surface.get_width()-148, 3))
create_units = True
while create_units:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            create_units = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button_next_rect.collidepoint(event.pos):
                    create_units = False
                else:
                    for pr in provinces:
                        if math.sqrt( (pr.coordinates[0]-event.pos[0])**2 + (pr.coordinates[1]-event.pos[1])**2 ) < 15:
                            game_map.add_unit(pr)
                            pygame.draw.circle(screen, COLORS["RED"], pr.coordinates, 15)


    pygame.draw.rect(screen, COLORS["BG"], (screen.get_width()-55, 0, 55, 35))
    clock.tick(75)
    screen.blit(font_fps.render(str(round(clock.get_fps(), 2)), True, COLORS["FG"]), (screen.get_width()-50, 5))
    
    pygame.display.update()



pygame.draw.rect(screen, COLORS["BG"], (0, 0, map_surface.get_width(), 40))
screen.blit(font.render("Создайте ходы", True, COLORS["FG"]), (5, 5))
pygame.draw.rect(screen, COLORS["GREEN"], button_next_rect, border_radius=12)
screen.blit(font.render("ДАЛЕЕ", True, COLORS["BG"]), (map_surface.get_width()-148, 3))
screen.blit(map_surface, (0, 41))
selected_unit = None
create_moves = True
for pr in provinces:
    pygame.draw.circle(screen, COLORS["COMM"], pr.coordinates, 5)
for unit in game_map.units:
    pygame.draw.circle(screen, COLORS["RED"], unit.location.coordinates, 15)
while create_moves:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            create_moves = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button_next_rect.collidepoint(event.pos):
                    game_manager.make_movements()
                    screen.blit(map_surface, (0, 41))
                    for pr in provinces:
                        pygame.draw.circle(screen, COLORS["COMM"], pr.coordinates, 5)
                    for unit in game_map.units:
                        pygame.draw.circle(screen, COLORS["RED"], unit.location.coordinates, 15)
                else:
                    if selected_unit is None:
                        for unit in game_map.units:
                            if math.sqrt( (unit.location.coordinates[0]-event.pos[0])**2 + (unit.location.coordinates[1]-event.pos[1])**2 ) < 15:
                                selected_unit = unit
                                pygame.draw.circle(screen, COLORS["PINK"], selected_unit.location.coordinates, 15)
                    else:
                        for pr in provinces:
                            if math.sqrt( (pr.coordinates[0]-event.pos[0])**2 + (pr.coordinates[1]-event.pos[1])**2 ) < 15:
                                game_manager.add_move(Move(selected_unit, pr))
                                pygame.draw.aaline(screen, COLORS["RED"], selected_unit.location.coordinates, pr.coordinates)
                                pygame.draw.circle(screen, COLORS["RED"], selected_unit.location.coordinates, 15)
                                selected_unit = None


    pygame.draw.rect(screen, COLORS["BG"], (screen.get_width()-55, 0, 55, 35))
    clock.tick(75)
    screen.blit(font_fps.render(str(round(clock.get_fps(), 2)), True, COLORS["FG"]), (screen.get_width()-50, 5))
    
    pygame.display.update()
