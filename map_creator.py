from lib.map_creator.map_loader_saver import Map_LS

import pygame


class MapCreator:
    def __init__(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height

        self.clock = pygame.time.Clock()   

        pygame.init()
        self.screen = pygame.display.set_mode((map_width*32+350, map_height*32))

        self.tiles = []
        self.tiles.append(pygame.image.load("game_maps/tile_land.png").convert())
        self.tiles.append(pygame.image.load("game_maps/tile_land_SC.png").convert())
        self.tiles.append(pygame.image.load("game_maps/tile_water.png").convert())

        self.font_small = pygame.font.SysFont("jetbrainsmononfm", 14)

        self.map_surface   = pygame.surface.Surface((map_width*32, self.screen.get_height()))
        self.panel_surface = pygame.surface.Surface((350, self.screen.get_height()))

        self.map_surface.fill((40, 42, 54))

        self.selected_tile = 0

        self.start_pos = None
        self.end_pos = None

        self.selected_paint_mode = 0

        self.province_number = 0

        self.map_loader = Map_LS((map_width, map_height))

        self.map_image = pygame.transform.scale(pygame.image.load("game_maps/image.png").convert(), (self.map_width*32, self.map_height*32))  # Map image
        self.map_surface.blit(self.map_image, (0, 0))
        #self.draw_tile_border()


    def event_processing(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
    
            if pygame.mouse.get_pressed()[0] == 1:
                if self.map_surface.get_rect().collidepoint(event.pos):
                    if self.selected_paint_mode == 1:
                        if not self.start_pos:
                            self.start_pos = [event.pos[0]//32, event.pos[1]//32]
                            self.end_pos = [event.pos[0]//32+1, event.pos[1]//32+1]
                        else:
                            self.end_pos = [event.pos[0]//32+1, event.pos[1]//32+1]
                    elif self.selected_paint_mode == 0:
                            self.map_surface.blit(self.tiles[self.selected_tile], (event.pos[0]//32*32, event.pos[1]//32*32))
                            self.map_loader.add_province_tile(event.pos[0]//32, event.pos[1]//32, self.selected_tile)
                            self.map_loader.add_province_number(event.pos[0]//32, event.pos[1]//32, self.province_number)
            
            if pygame.mouse.get_pressed()[0] == 0:
                if self.start_pos:
                    for x in range(self.start_pos[0], self.end_pos[0]):
                        for y in range(self.start_pos[1], self.end_pos[1]):
                            self.map_surface.blit(self.tiles[self.selected_tile], (x*32, y*32))
                            self.map_loader.add_province_tile(x, y, self.selected_tile)
                            self.map_loader.add_province_number(x, y, self.province_number)

                self.start_pos = None
                self.end_pos = None
                        
                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.selected_tile = 0
                if event.key == pygame.K_2:
                    self.selected_tile = 1
                if event.key == pygame.K_3:
                    self.selected_tile = 2

                if event.key == pygame.K_p:
                    self.selected_paint_mode = 0
                if event.key == pygame.K_r:
                    self.selected_paint_mode = 1

                if event.key == pygame.K_c:
                    self.province_number += 1

                if event.key == pygame.K_s:
                    self.map_loader.save_map()
                

    def display_side_panel(self):
        pygame.draw.rect(self.panel_surface, (68, 71, 90), (0, 0, 350, self.screen.get_height()))

        self.panel_surface.blit(self.font_small.render("Tiles:", True, (248, 248, 242)), (5, 5))

        for i, tile in enumerate(self.tiles):
            if i == self.selected_tile:
                pygame.draw.rect(self.panel_surface, (248, 248, 242), (10+42*i-1, 24, 34, 34))
            self.panel_surface.blit(tile, (10+42*i, 25))

        self.panel_surface.blit(self.font_small.render("Paint Mode:", True, (248, 248, 242)), (5, 67))
        self.panel_surface.blit(self.font_small.render("[x] Pen" if self.selected_paint_mode == 0 else  "    Pen", True, (248, 248, 242)), (5, 70+15))
        self.panel_surface.blit(self.font_small.render("[x] Rect" if self.selected_paint_mode == 1 else "    Rect", True, (248, 248, 242)), (5, 70+30))

        self.panel_surface.blit(self.font_small.render(f"Province number - {self.province_number}", True, (248, 248, 242)), (5, 125))


        self.screen.blit(self.panel_surface, (self.screen.get_width()-350, 0))


    def display_select_rect(self):
        if self.start_pos:
            if self.end_pos:
                pygame.draw.rect(self.screen, (255, 0, 0), (self.start_pos[0]*32, 
                                                            self.start_pos[1]*32, 
                                                            self.end_pos[0]*32-self.start_pos[0]*32, 
                                                            self.end_pos[1]*32-self.start_pos[1]*32), 1)


    def display_province_border(self):
        for x in range(0, self.map_width):
            for y in range(0, self.map_height):
                for x_n in range(x-1, x+1):
                    if self.map_loader.provinces_number_array[x_n, y] != self.map_loader.provinces_number_array[x, y]:
                        pygame.draw.line(self.screen, [0, 0, 0], ((x_n*32+32), (y*32)), ((x_n*32+32), (y*32+32)), 5)

                for y_n in range(y-1, y+1):
                    if self.map_loader.provinces_number_array[x, y_n] != self.map_loader.provinces_number_array[x, y]:
                        pygame.draw.line(self.screen, [0, 0, 0], ((x*32), (y_n*32+32)), ((x*32+32), (y_n*32+32)), 5)


    def draw_tile_border(self):
        for x in range(0, self.map_width*32, 32):
            pygame.draw.line(self.map_surface, (68, 71, 90), (x, 0), (x, self.map_surface.get_height()))
        
        for y in range(0, self.map_height*32, 32):
            pygame.draw.line(self.map_surface, (68, 71, 90), (0, y), (self.map_surface.get_width(), y))


    def run(self):
        while True:
            self.event_processing()

            self.display_side_panel()

            self.clock.tick(75)
            
            self.screen.blit(self.map_surface, (0, 0))
            
            self.display_province_border()

            self.display_select_rect()

            pygame.display.update()

    
if __name__ == "__main__":
    app = MapCreator(42, 32)
    app.run()
