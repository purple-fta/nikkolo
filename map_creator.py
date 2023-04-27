from lib.map_creator.map_loader_saver import Map_LS

import pygame


class MapCreator:
    def __init__(self, map_width, map_height, tile_size):
        self.map_width = map_width
        self.map_height = map_height

        self.tile_size = tile_size

        self.clock = pygame.time.Clock()   

        pygame.init()
        self.screen = pygame.display.set_mode((map_width*self.tile_size+350, map_height*self.tile_size))

        self.tiles = []
        self.tiles.append(pygame.image.load("game_maps/tile_land.png").convert())
        self.tiles.append(pygame.image.load("game_maps/tile_land_SC.png").convert())
        self.tiles.append(pygame.image.load("game_maps/tile_water.png").convert())

        self.font_small = pygame.font.SysFont("jetbrainsmononfm", 14)

        self.map_surface   = pygame.surface.Surface((map_width*self.tile_size, self.screen.get_height()))
        self.panel_surface = pygame.surface.Surface((350, self.screen.get_height()))

        self.map_surface.fill((40, 42, 54))

        self.selected_tile = 0

        self.start_pos = None
        self.end_pos = None

        self.selected_paint_mode = 0

        self.province_number = 0

        self.map_loader = Map_LS((map_width, map_height))

        self.map_image = pygame.transform.scale(pygame.image.load("game_maps/image.png").convert(), (self.map_width*self.tile_size, self.map_height*self.tile_size))  # Map image
        self.map_surface.blit(self.map_image, (0, 0))
        #self.draw_tile_border()

        self.is_print_province_numbers = False


    def event_processing(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
    
            if pygame.mouse.get_pressed()[0] == 1:
                if self.map_surface.get_rect().collidepoint(event.pos):
                    if self.selected_paint_mode == 1:
                        if not self.start_pos:
                            self.start_pos = [event.pos[0]//self.tile_size, event.pos[1]//self.tile_size]
                            self.end_pos = [event.pos[0]//self.tile_size+1, event.pos[1]//self.tile_size+1]
                        else:
                            self.end_pos = [event.pos[0]//self.tile_size+1, event.pos[1]//self.tile_size+1]
                    elif self.selected_paint_mode == 0:
                            if self.selected_tile != self.map_loader.tile_number_array[event.pos[0]//self.tile_size, event.pos[1]//self.tile_size] or \
                               self.province_number != self.map_loader.provinces_number_array[event.pos[0]//self.tile_size, event.pos[1]//self.tile_size]:
                                self.map_surface.blit(self.tiles[self.selected_tile], (event.pos[0]//self.tile_size*self.tile_size, event.pos[1]//self.tile_size*self.tile_size))
                            
                                self.map_loader.add_province_number(event.pos[0]//self.tile_size, event.pos[1]//self.tile_size, self.province_number)
                                
                                if self.is_print_province_numbers:
                                    self.print_province_number(event.pos[0]//self.tile_size, event.pos[1]//self.tile_size)
    
                            self.map_loader.add_province_tile(event.pos[0]//self.tile_size, event.pos[1]//self.tile_size, self.selected_tile)
                            self.map_loader.add_province_number(event.pos[0]//self.tile_size, event.pos[1]//self.tile_size, self.province_number)
            
            if pygame.mouse.get_pressed()[0] == 0:
                if self.start_pos:
                    for x in range(self.start_pos[0], self.end_pos[0]):
                        for y in range(self.start_pos[1], self.end_pos[1]):
                            self.map_loader.add_province_tile(x, y, self.selected_tile)
                            self.map_loader.add_province_number(x, y, self.province_number)
                            
                            self.map_surface.blit(self.tiles[self.selected_tile], (x*self.tile_size, y*self.tile_size))
                            
                            if self.is_print_province_numbers:
                                self.print_province_number(x, y)

                self.start_pos = None
                self.end_pos = None
            
            if pygame.mouse.get_pressed()[2] == 1:
                if self.map_surface.get_rect().collidepoint(event.pos):
                    self.map_surface.blit(self.map_image, (0, 0))
                    self.redraw_tiles()
                    self.map_loader.add_province_tile(event.pos[0]//self.tile_size, event.pos[1]//self.tile_size, -1)
                    self.map_loader.add_province_number(event.pos[0]//self.tile_size, event.pos[1]//self.tile_size, -1)
            
                        
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

                if event.key == pygame.K_x:
                    self.province_number -= 1
                if event.key == pygame.K_c:
                    self.province_number += 1

                if event.key == pygame.K_s:
                    self.map_loader.save_map()
                
                if event.key == pygame.K_n:
                    self.redraw_tiles()
                    self.is_print_province_numbers = not self.is_print_province_numbers
                    if self.is_print_province_numbers:
                        self.print_province_numbers()


    def display_side_panel(self):
        pygame.draw.rect(self.panel_surface, (68, 71, 90), (0, 0, 350, self.screen.get_height()))

        self.panel_surface.blit(self.font_small.render("Tiles:", True, (248, 248, 242)), (5, 5))

        for i, tile in enumerate(self.tiles):
            if i == self.selected_tile:
                pygame.draw.rect(self.panel_surface, (248, 248, 242), (10+42*i-1, 24, 34, 34))
            self.panel_surface.blit(pygame.transform.scale(tile, (32, 32)), (10+42*i, 25))

        self.panel_surface.blit(self.font_small.render("Paint Mode:", True, (248, 248, 242)), (5, 67))
        self.panel_surface.blit(self.font_small.render("[x] Pen" if self.selected_paint_mode == 0 else  "    Pen", True, (248, 248, 242)), (5, 70+15))
        self.panel_surface.blit(self.font_small.render("[x] Rect" if self.selected_paint_mode == 1 else "    Rect", True, (248, 248, 242)), (5, 70+30))

        self.panel_surface.blit(self.font_small.render(f"Province number - {self.province_number}", True, (248, 248, 242)), (5, 125))


        self.screen.blit(self.panel_surface, (self.screen.get_width()-350, 0))


    def display_select_rect(self):
        if self.start_pos:
            if self.end_pos:
                pygame.draw.rect(self.screen, (255, 0, 0), (self.start_pos[0]*self.tile_size, 
                                                            self.start_pos[1]*self.tile_size, 
                                                            self.end_pos[0]*self.tile_size-self.start_pos[0]*self.tile_size, 
                                                            self.end_pos[1]*self.tile_size-self.start_pos[1]*self.tile_size), 1)


    def display_province_border(self):
        for x in range(0, self.map_width):
            for y in range(0, self.map_height):
                for x_n in range(x-1, x+1):
                    if self.map_loader.provinces_number_array[x_n, y] != self.map_loader.provinces_number_array[x, y]:
                        pygame.draw.line(self.screen, [0, 0, 0], ((x_n*self.tile_size+self.tile_size), (y*self.tile_size)), ((x_n*self.tile_size+self.tile_size), (y*self.tile_size+self.tile_size)), 2)

                for y_n in range(y-1, y+1):
                    if self.map_loader.provinces_number_array[x, y_n] != self.map_loader.provinces_number_array[x, y]:
                        pygame.draw.line(self.screen, [0, 0, 0], ((x*self.tile_size), (y_n*self.tile_size+self.tile_size)), ((x*self.tile_size+self.tile_size), (y_n*self.tile_size+self.tile_size)), 2)

    
    def print_province_number(self, x, y):
        self.map_surface.blit(self.font_small.render(str(self.map_loader.provinces_number_array[x, y]), True, (0, 0, 0)), (x*self.tile_size+self.tile_size/2-3, y*self.tile_size+self.tile_size/2-9))


    def print_province_numbers(self):
        for x in range(self.map_loader.map_size[0]):
            for y in range(self.map_loader.map_size[1]):
                if self.map_loader.provinces_number_array[x, y] != -1:
                    self.print_province_number(x, y)


    def redraw_tiles(self):
        self.map_surface.blit(self.map_image, (0, 0))

        for x in range(self.map_loader.map_size[0]):
            for y in range(self.map_loader.map_size[1]):
                if self.map_loader.tile_number_array[x, y] != -1:
                    self.map_surface.blit(self.tiles[self.map_loader.tile_number_array[x, y]], (x*self.tile_size, y*self.tile_size))


    def draw_tile_border(self):
        for x in range(0, self.map_width*self.tile_size, self.tile_size):
            pygame.draw.line(self.map_surface, (68, 71, 90), (x, 0), (x, self.map_surface.get_height()))
        
        for y in range(0, self.map_height*self.tile_size, self.tile_size):
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
    app = MapCreator(84, 64, 16)
    app.run()
