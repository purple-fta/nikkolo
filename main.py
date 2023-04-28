from lib.map_creator.map_loader_saver import Map_LS
from lib.core.game_manager import GameManager
from lib.map_creator.gui_province import *

import pygame
import numpy


class Game(GameManager):
    def __init__(self):
        GameManager.__init__(self)

        pygame.init()

        self.screen = pygame.display.set_mode((42*32+350, 32*32))
        
        self.clock = pygame.time.Clock()

        self.map_loader = Map_LS((42, 32))
        provinces_and_neighboring = self.map_loader.load_map()
        for pr in provinces_and_neighboring:
            self.add_province(pr["province"], list(pr["neighboring"]))

        self.hover_province = None
        self.select_province = None


    def event_processing(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEMOTION:
                
                hover_province_now = self.get_province_with_tile_coordinations(event.pos[0]//16, event.pos[1]//16)
                if self.hover_province != hover_province_now:
                    if self.hover_province:
                        self.draw_province_tiles(self.hover_province)
                        self.draw_province_border(self.hover_province)

                    self.hover_province = hover_province_now
                    self.draw_hover_province()
                    
                    if self.hover_province:
                        self.draw_province_border(self.hover_province)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    if self.hover_province:
                        self.select_province = self.hover_province

    def draw_tiles(self):
        for province in self.provinces_graph:
            color = self.get_color_province_type((98, 114, 164), (80, 250, 123), province)
            for tile_x, tile_y in province.tiles_coordinates:
                self.draw_tile(tile_x, tile_y, color)
    
    def draw_province_tiles(self, province):
        for tile_x, tile_y in province.tiles_coordinates:
            self.draw_tile(tile_x, tile_y)

    def get_province_with_tile_coordinations(self, x, y):
        for province in self.provinces_graph:
            if [x, y] in province.tiles_coordinates:
                return province

    def draw_tile(self, x, y, color=None):
        if not color:
            province = self.get_province_with_tile_coordinations(x, y)
            color = self.get_color_province_type((98, 114, 164), (80, 250, 123), province)
        
        pygame.draw.rect(self.screen, color, (16*x, 16*y, 16, 16))

    def get_color_province_type(self, water_type_color, other_color, province):
        color = water_type_color if province.province_type == ProvinceType.water.value else other_color
        return color

    def draw_hover_province(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_tile_x, mouse_tile_y = mouse_x//16, mouse_y//16

        hover_province = self.get_province_with_tile_coordinations(mouse_tile_x, mouse_tile_y)
        if hover_province:
            color = self.get_color_province_type((139, 233, 253), (255, 184, 108), hover_province)
            for tile_x, tile_y in hover_province.tiles_coordinates:
                self.draw_tile(tile_x, tile_y, color)

    def draw_province_border(self, province):
        for tile_x, tile_y in province.tiles_coordinates:
            if [tile_x-1, tile_y] not in province.tiles_coordinates:
                pygame.draw.line(self.screen, (0, 0, 0), (tile_x*16, tile_y*16), (tile_x*16, tile_y*16+16), 2)

            if [tile_x+1, tile_y] not in province.tiles_coordinates:
                pygame.draw.line(self.screen, (0, 0, 0), (tile_x*16+16, tile_y*16), (tile_x*16+16, tile_y*16+16), 2)

            if [tile_x, tile_y-1] not in province.tiles_coordinates:
                pygame.draw.line(self.screen, (0, 0, 0), (tile_x*16, tile_y*16), (tile_x*16+16, tile_y*16), 2)
                
            if [tile_x, tile_y+1] not in province.tiles_coordinates:
                pygame.draw.line(self.screen, (0, 0, 0), (tile_x*16, tile_y*16+16), (tile_x*16+16, tile_y*16+16), 2)

    def draw_provinces_border(self):
        for province in self.provinces_graph:
            self.draw_province_border(province)


    def run(self):
        self.draw_tiles()
        self.draw_provinces_border()
        while True:
            self.event_processing()

            self.clock.tick(75)
            print(f"{round(self.clock.get_fps())}")

            pygame.display.update()

game = Game()
game.run()
