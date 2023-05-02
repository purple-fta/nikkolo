from lib.map_creator.map_loader_saver import Map_LS
from lib.core.game_manager import GameManager
from lib.core.game_manager.map.unit import *
from lib.map_creator.gui_province import *
from lib.map_creator.gui_country import *
from lib.map_creator.gui_unit import *


from random import choice
import random
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
        for i in self.provinces_graph:
            self.select_province = i
            break

        self.font = pygame.font.SysFont("jetbrainsmononfm", 20)
        self.font_small = pygame.font.SysFont("jetbrainsmononfm", 14)

        self.STAGE_CREATE_COUNTRY = 1
        self.STAGE_CREATE_UNIT = 2
        self.STAGE_CREATE_MOVE = 3
        self.game_stage = self.STAGE_CREATE_COUNTRY

        self.MOVE_TYPE = 1
        self.SUPPORT_MOVE_TYPE = 2
        self.SUPPORT_HOLD_TYPE = 3
        self.CONVOY_TYPE = 4
        self.created_type_move = self.MOVE_TYPE

        self.county_colors = (
            (255, 85, 85),
            (189, 147, 249),
            (255, 121, 198),
            (252, 193, 30),
            (80, 250, 123)
        )
        self.county_colors_hover = (
            (247, 126, 126),
            (202, 171, 245),
            (250, 147, 206),
            (247, 210, 106),
            (122, 255, 156)
        )
        self.selected_country_number = 0

        self.color_free_province = (250, 222, 145)

        # for i, color in enumerate(self.county_colors):
        prs1_n = [0, 9, 24, 11, 1, 10, 64, 2, 66]
        prs1 = []
        for pr in self.provinces_graph:
            if int(pr.name) in prs1_n:
                prs1.append(pr)
        self.add_country(GuiCountry(str(0), prs1, self.county_colors[0]))
        prs_n = [5, 4, 7, 67]
        prs = []
        for pr in self.provinces_graph:
            if int(pr.name) in prs_n:
                prs.append(pr)
        self.add_country(GuiCountry(str(1), prs, self.county_colors[1]))
        prs_n = [68, 33, 65, 32, 70, 34, 69]
        prs = []
        for pr in self.provinces_graph:
            if int(pr.name) in prs_n:
                prs.append(pr)
        self.add_country(GuiCountry(str(2), prs, self.county_colors[2]))


        self.unit_for_create_move = None
        self.province_for_create_move = None

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

                    if self.select_province:
                        self.draw_province_border(self.select_province)
                    
                    self.draw_sc_s()
                    self.draw_moves()
                    self.draw_units()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.hover_province:
                        old_select_province = self.select_province
                        self.select_province = self.hover_province

                        if self.game_stage == self.STAGE_CREATE_COUNTRY:
                            self.add_province_to_country(self.select_province, self.countries[self.selected_country_number])
                            self.draw_hover_province()
                            self.draw_sc_s()
                        if self.game_stage == self.STAGE_CREATE_UNIT:
                            self.create_unit_in_province(pygame.mouse.get_pos(),self.hover_province)
                        if self.game_stage == self.STAGE_CREATE_MOVE:
                            if not self.unit_for_create_move:
                                self.unit_for_create_move = self.get_unit_in_province(self.select_province)
                                self.draw_units()
                            elif not self.province_for_create_move:
                                self.province_for_create_move = self.select_province

                                self.create_move(self.unit_for_create_move, self.province_for_create_move)

                        if old_select_province:
                            self.draw_province_border(old_select_province)
                            
                        self.draw_province_border(self.hover_province)
                        self.draw_moves()
                        self.draw_side_bar()
         
                if event.button == 3:
                    if self.hover_province:
                        if self.game_stage == self.STAGE_CREATE_COUNTRY:
                            country = self.get_county_with_province(self.hover_province)
                            country.provinces.remove(self.hover_province)

                            self.draw_hover_province()
                            self.draw_province_border(self.hover_province)
                            self.draw_sc_s()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if self.game_stage == self.STAGE_CREATE_COUNTRY:
                        self.selected_country_number = 0
                    if self.game_stage == self.STAGE_CREATE_MOVE:
                        self.created_type_move = self.MOVE_TYPE

                if event.key == pygame.K_2:
                    if self.game_stage == self.STAGE_CREATE_COUNTRY:
                        self.selected_country_number = 1
                    if self.game_stage == self.STAGE_CREATE_MOVE:
                        self.created_type_move = self.SUPPORT_MOVE_TYPE

                if event.key == pygame.K_3:
                    if self.game_stage == self.STAGE_CREATE_COUNTRY:
                        self.selected_country_number = 2
                    if self.game_stage == self.STAGE_CREATE_MOVE:
                        self.created_type_move = self.SUPPORT_HOLD_TYPE

                if event.key == pygame.K_4:
                    if self.game_stage == self.STAGE_CREATE_COUNTRY:
                        self.selected_country_number = 3
                    if self.game_stage == self.STAGE_CREATE_MOVE:
                        self.created_type_move = self.CONVOY_TYPE

                if event.key == pygame.K_5:
                    if self.game_stage == self.STAGE_CREATE_COUNTRY:
                        self.selected_country_number = 4

                if event.key == pygame.K_6:
                    if self.game_stage == self.STAGE_CREATE_COUNTRY:
                        self.selected_country_number = 5
                
                if event.key == pygame.K_c:
                    self.game_stage = self.STAGE_CREATE_COUNTRY
                if event.key == pygame.K_u:
                    self.game_stage = self.STAGE_CREATE_UNIT
                if event.key == pygame.K_m:
                    self.game_stage = self.STAGE_CREATE_MOVE
                
                if event.key == pygame.K_n:
                    self.applying_moves()
                    self.draw_tiles()
                    self.draw_provinces_border()
                    self.draw_sc_s()
                    self.draw_moves()
                    self.draw_units()
                if event.key == pygame.K_f:
                    self.form()

                self.draw_side_bar()

    def create_unit_in_province(self, mouse_pos, province):
        unit = GuiUnit(list(mouse_pos), province)
        country = self.get_county_with_province(province)

        if not country:
            return

        try:
            self.add_unit(unit, country)
        except:
            pass

        self.draw_units()

    def get_unit_in_province(self, province):
        for unit in self.units:
            if unit.location == province:
                return unit

    def get_move_in_unit(self, unit):
        for move in self.moves:
            if move.unit == unit:
                return move

    def create_move(self, unit, province):
        if self.created_type_move == self.MOVE_TYPE:
            self.add_move(GuiMove(unit, province, pygame.mouse.get_pos()))
        if self.created_type_move == self.SUPPORT_MOVE_TYPE:
            move = self.get_move_in_unit(self.get_unit_in_province(province))
            if move:
                self.add_move(GuiSupportMove(unit, move.province_target, move, pygame.mouse.get_pos()))

        self.unit_for_create_move = None
        self.province_for_create_move = None

    def draw_moves(self):
        for move in self.moves:
            if type(move) == GuiMove:
                pygame.draw.line(self.screen, (255, 0, 0), move.unit.coordinates, move.target_coordinates, 5)
            if type(move) == GuiSupportMove:
                pygame.draw.line(self.screen, (255, 255, 0), move.unit.coordinates, move.target_coordinates, 5)


    def draw_units(self):
        for country in self.countries:
            for unit in country.units:
                pygame.draw.circle(self.screen, (255, 255, 255) if unit == self.unit_for_create_move else (0, 0, 0), unit.coordinates, 12)
                pygame.draw.circle(self.screen, country.color, unit.coordinates, 10)
                self.screen.blit(self.font.render("U", True, (0, 0, 0)), (unit.coordinates[0]-6, unit.coordinates[1]-13))

    def get_county_with_province(self, province):
        for country in self.countries:
            if province in country.provinces:
                return country

    def draw_side_bar(self):
        panel_x, panel_y = self.screen.get_width()-350, 0

        pygame.draw.rect(self.screen, (68, 71, 90), (panel_x, panel_y, 350, self.screen.get_height()))

        if self.select_province:
            self.screen.blit(self.font.render(f"Province", True, (248, 248, 242)), (panel_x+125, panel_y+10))
            self.screen.blit(self.font.render(f"Name: {self.select_province.name}", True, (248, 248, 242)), (panel_x+15, panel_y+35))
            self.screen.blit(self.font.render(f"SC: {self.select_province.is_supply_center}", True, (248, 248, 242)), (panel_x+15, panel_y+60))
            pygame.draw.line(self.screen, (248, 248, 242), (panel_x, panel_y+100), (panel_x+350, panel_y+100))
        
        self.screen.blit(self.font.render(f"New Country", True, (248, 248, 242)), (panel_x+110, panel_y+110))
        for i, color in enumerate(self.county_colors):
            if color == self.county_colors[self.selected_country_number]:
                pygame.draw.rect(self.screen, (255, 255, 255), (panel_x+15+i*40, panel_y+145, 30, 30))
            pygame.draw.rect(self.screen, color, (panel_x+17+i*40, panel_y+147, 26, 26))

        pygame.draw.line(self.screen, (248, 248, 242), (panel_x, panel_y+190), (panel_x+350, panel_y+190))
        self.screen.blit(self.font.render("Game Stage", True, (255, 255, 255)), (panel_x+115, 192))
        self.screen.blit(self.font_small.render(("[x]" if self.game_stage == self.STAGE_CREATE_COUNTRY else "[ ]")+" Create (c)ountry", True, (255, 255, 255)), (panel_x+15, 220))
        self.screen.blit(self.font_small.render(("[x]" if self.game_stage == self.STAGE_CREATE_UNIT else "[ ]")+" Create (u)nit", True, (255, 255, 255)), (panel_x+15, 240))
        self.screen.blit(self.font_small.render(("[x]" if self.game_stage == self.STAGE_CREATE_MOVE else "[ ]")+" Create (m)ove", True, (255, 255, 255)), (panel_x+15, 260))

        pygame.draw.line(self.screen, (248, 248, 242), (panel_x, panel_y+290), (panel_x+350, panel_y+290))
        self.screen.blit(self.font.render("Create Move", True, (255, 255, 255)), (panel_x+110, 292))
        self.screen.blit(self.font_small.render(("[x]" if self.created_type_move == self.MOVE_TYPE else "[ ]")+" Move (1)", True, (255, 255, 255)), (panel_x+15, 320))
        self.screen.blit(self.font_small.render(("[x]" if self.created_type_move == self.SUPPORT_MOVE_TYPE else "[ ]")+" Support Move (2)", True, (255, 255, 255)), (panel_x+15, 340))
        self.screen.blit(self.font_small.render(("[x]" if self.created_type_move == self.SUPPORT_HOLD_TYPE else "[ ]")+" Support Hold (3)", True, (255, 255, 255)), (panel_x+15, 360))
        self.screen.blit(self.font_small.render(("[x]" if self.created_type_move == self.CONVOY_TYPE else "[ ]")+" Convoy (4)", True, (255, 255, 255)), (panel_x+15, 380))

    def draw_tiles(self):
        for province in self.provinces_graph:
            color = self.get_color_province_type((98, 114, 164), self.color_free_province, province)
            country = self.get_county_with_province(province)
            if country:
                color = country.color
            for tile_x, tile_y in province.tiles_coordinates:
                self.draw_tile(tile_x, tile_y, color)
    
    def draw_sc_s(self):
        for province in self.provinces_graph:
            if province.is_supply_center:
                random.seed(province.name)
                tile_x_for_sc, tile_y_for_sc = choice(province.tiles_coordinates)
                pygame.draw.circle(self.screen, (0, 0, 0), (tile_x_for_sc*16+8, tile_y_for_sc*16+8), 9)
                pygame.draw.circle(self.screen, (255, 255, 255), (tile_x_for_sc*16+8, tile_y_for_sc*16+8), 7)

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
            color = self.get_color_province_type((98, 114, 164), self.color_free_province, province)
            for county in self.countries:
                for province in county.provinces:
                    if [x, y] in province.tiles_coordinates:
                        color = county.color
        
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
            for county in self.countries:
                for province in county.provinces:
                    tile = hover_province.tiles_coordinates[0]
                    if tile in province.tiles_coordinates:
                        color = self.county_colors_hover[int(county.name)]

            for tile_x, tile_y in hover_province.tiles_coordinates:
                self.draw_tile(tile_x, tile_y, color)

    def draw_province_border(self, province):
        color = (248, 248, 242) if province == self.select_province else (0, 0, 0)
        for tile_x, tile_y in province.tiles_coordinates:
            if [tile_x-1, tile_y] not in province.tiles_coordinates:
                pygame.draw.line(self.screen, color, (tile_x*16, tile_y*16), (tile_x*16, tile_y*16+16), 2)

            if [tile_x+1, tile_y] not in province.tiles_coordinates:
                pygame.draw.line(self.screen, color, (tile_x*16+16, tile_y*16), (tile_x*16+16, tile_y*16+16), 2)

            if [tile_x, tile_y-1] not in province.tiles_coordinates:
                pygame.draw.line(self.screen, color, (tile_x*16, tile_y*16), (tile_x*16+16, tile_y*16), 2)
                
            if [tile_x, tile_y+1] not in province.tiles_coordinates:
                pygame.draw.line(self.screen, color, (tile_x*16, tile_y*16+16), (tile_x*16+16, tile_y*16+16), 2)

    def draw_provinces_border(self):
        for province in self.provinces_graph:
            self.draw_province_border(province)

    def run(self):
        self.draw_tiles()
        self.draw_provinces_border()
        self.draw_sc_s()
        self.draw_side_bar()
        while True:
            self.event_processing()

            self.clock.tick(75)
            #print(f"FPS: {round(self.clock.get_fps())}")
            #print(self.moves)

            pygame.display.update()

game = Game()
game.run()
