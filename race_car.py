import pygame as pg
import pytmx
import random
import os
import math
import numpy as np

from os import path, listdir

vec = pg.math.Vector2

WIDTH, HEIGHT = 500, 400
TITLE = 'LYRIO RACE - V_03'
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
LIGHTGREEN = (208, 240, 192)
LIGHTGRAY = (211,211,211)

FPS = 15

ENEMY_DELAY = 900
MOVE = 3
S_WIDTH = 25
W_WIDTH = 50
TARGET_UPDATE = 60
LOOP_TIME = 25000 #miliseconds
TOTAL_DIST = 4000

class Game():
    def __init__(self, size=1):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '1'
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.player_size = size
        self.font_name = pg.font.match_font('arial')
        self.load()
        
    def load(self):
        self.dir = path.dirname(path.abspath("__file__"))
        self.img_dir = path.join(self.dir, 'img')
        self.map_dir = path.join(self.img_dir, 'Map')

    def new(self, show_line=False, show_start=False, debug=False):
        # Variables
        self.line = show_line
        self.start = show_start
        self.debug = debug
        self.time = 0
        self.top_car = []
        # Sprite Groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.cars = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        # Load Objects
        self.map = Map(self)
        self.camera = Camera(self, self.map.width, self.map.height)
        self.target = Target(self)
        self.car = []

        for objects in self.map.tmx.objects:
            if objects.name == 'car_2':
                for _ in range(self.player_size):
                    self.car.append(Car(self, objects.x, objects.y))
            if objects.name == 'offroad':
                Obstacle(self, objects.x, objects.y, objects.width, objects.height)
            if objects.name == 'checkpoint':
                self.target.add(objects.id, objects.x, objects.y)
        self.target.ini()
        
        # Show start screen
        if show_start:
            self.show_start_screen()
        #self.run()

    def run(self, txt=0):
        self.events()
        self.update()
        self.draw(txt)
        ml_time = self.clock.tick(FPS)
        self.time = ml_time / 1000.0
            
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    self.running = False

    def update(self):
        self.all_sprites.update()
        #dist = 0
        self.top_car = sorted(range(len(self.car)), key=lambda i: self.car[i].reward, reverse=True)[:10]
        self.id = self.top_car[0]
        #for idx, car in enumerate(self.car):
        #    if car.reward > dist:
        #        dist = car.reward
        #        self.id = idx
        self.camera.update(self.car[self.id])
            
    def draw(self, txt):
        self.screen.blit(self.map.image, self.camera.apply_rect(self.map.rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.debug:
                pg.draw.rect(self.screen, BLACK, self.camera.apply_rect(sprite.rect), 1)

        for idx, sprite in enumerate(self.cars):
            if idx in self.top_car:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
                if self.debug:
                    pg.draw.rect(self.screen, BLACK, self.camera.apply_rect(sprite.rect), 1)

        if self.debug:
            for obstacle in self.obstacles:
                pg.draw.rect(self.screen, BLACK, self.camera.apply_rect(obstacle.rect), 1)

        #for target in self.target.all_points:
        #    pg.draw.circle(self.screen, BLUE, target[1] + self.camera.get_coord(), 20)
        #    self.draw_text(str(target[0]), 16, BLACK, target[1].x + self.camera.get_coord()[0], target[1].y + self.camera.get_coord()[1])

        self.draw_text('FPS (ms): {0:.1f}'.format(0 if self.time == 0 else 1000/(self.time*1000)), 16, BLACK, WIDTH // 2, 15)                 
        self.draw_text('Time (s): {0:.1f}'.format(self.car[self.id].play_time), 16, BLACK, WIDTH // 2, 35)                 
        self.draw_text('Target Dist: {0:.0f}'.format(self.car[self.id].target_dist), 16, BLACK, WIDTH // 2, 55)
        self.draw_text('Reward: {0:.3f}'.format(self.car[self.id].reward), 16, BLACK, WIDTH // 2, 75)
        self.draw_text('Players: {0:.0f}'.format(txt), 16, BLACK, WIDTH // 2, 95)
        
        if self.line:
            self.draw_vectors(self.car[0],self.screen)
            l_number = 20
            for idx, aux in enumerate(self.car[0].sensor_info):
                self.draw_text('Sensor[{0:.0f}°]: {1:.0f}'.format(aux[0], aux[3]), 16, BLACK, WIDTH - 100, 15+l_number)
                l_number+=20
            
        pg.display.flip()
        
    def show_start_screen(self):
        self.screen.fill(LIGHTBLUE)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("UP and DOWN Arrows to go Accelerate and Break", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("<- | -> to Turn", 22, WHITE, WIDTH / 2, (HEIGHT / 2) + 30)
        self.draw_text("Press any key to Play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
    
    def show_game_over(self):
        if not self.running:
            return
        self.screen.fill(LIGHTBLUE)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        self.wait_for_key()
        self.running = False
        
    def draw_text(self, text, size, color, x, y, location='midtop'):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        setattr(text_rect, location, (x, y))
        self.screen.blit(text_surface, text_rect)
        
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    waiting = False

    def draw_vectors(self, car, screen):
        #for car_id, car in enumerate(car):
        for idx, aux in enumerate(car.sensor_info):
            pg.draw.line(screen, LIGHTGRAY, car.pos + self.camera.get_coord(), aux[2] + self.camera.get_coord(), 3)


class Car(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 5
        self.groups = game.cars
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.game_over = False
        self.x = x
        self.y = y
        self.max_acc = 1.5
        self.max_steering = 45
        self.max_vel = 10
        self.min_vel = 6
        self.orig_image = self.load_images()
        #self.ini(vec(self.x, self.y))
        
    def load_images(self):
        img = pg.image.load(path.join(self.game.img_dir, 'car_4.png')).convert_alpha()
        img = pg.transform.smoothscale(img, (int(img.get_rect().width*0.25), int(img.get_rect().height*0.25))) 
        img = pg.transform.rotate(img, -90)
        return img

    def ini(self):
        self.start_car = pg.time.get_ticks()
        self.loop_time = self.start_car
        self.play_time = 0
        self.playing = True
        self.vel = vec(0, 0)
        self.target_dist = 0.0
        self.target_ang = 0.0
        self.angle = 0
        self.ang_vel = 0
        self.acc = 0.0
        self.steering = 0.0
        self.stop = False
        self.is_crashed = False
        self.goal = False
        self.car_target = 0
        self.crash_acc = 0
        self.reward = 0
        self.target_mult = 0

        self.car_hits = []
        
        self.pos = vec(self.x, self.y)
        self.sensor_steps = np.arange(0, 360, 30)
        self.sensor = self.create_sensors(size=20, dist=6)
        self.sensor_info = []
        self.target_point = self.game.target.all_points

        self.obj_len = int(self.orig_image.get_height() * 0.95)
        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

    def event(self, action=0):
        self.action = action
        if self.action in [0,4,5]: # Go forward
            self.acc += 1 * self.game.time
        elif self.action in [1,6,7]: # Go reverse
            self.acc -= 1 * self.game.time
        else:
            self.acc = 0

        if self.action in [2,4,6]: # Turn Right
            if self.steering > 0:
                self.steering = self.max_steering * (self.game.time)
            else:
                self.steering -= self.max_steering * (self.game.time)
        elif self.action in [3,5,7]: # Turn Left
            if self.steering < 0:
                self.steering = self.max_steering * (self.game.time)
            else:
                self.steering += self.max_steering * (self.game.time)
        else:
            self.steering = 0 


    def update(self):
        self.goal = False
        self.acc = max(-self.max_acc, min(self.acc, self.max_acc))
    
        self.vel += (self.acc, 0)
        self.vel.x = max(self.min_vel, min(self.vel.x, self.max_vel))

        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))
        if self.steering:
            radius = self.obj_len / math.sin(math.radians(self.steering))
            self.ang_vel = self.vel.x / radius
        else:
            self.ang_vel = 0 
        
        aux_angle = math.degrees(self.ang_vel)
        self.angle += aux_angle
        self.angle = self.angle % 360
        self.pos += self.vel.rotate(-self.angle)
        
        self.image = pg.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.mask = pg.mask.from_surface(self.image)
        
        self.update_sensors(-aux_angle) 
        self.sensor_info = self.sensor_dist()
        self.get_target()

        if self.hit():
            if not self.is_crashed:
                self.is_crashed = True
                self.playing = False
                self.vel.x = 0
        else:
            self.is_crashed = False

        self.reward = ((1-(self.target_dist / TOTAL_DIST))/10) + self.target_mult + (self.vel.x/100)
        self.play_time = (pg.time.get_ticks() - self.start_car) / 1000
        
        if (pg.time.get_ticks() - self.loop_time >= LOOP_TIME):
            self.playing = False

        return self.playing, self.reward, self.get_state()

    def get_state(self):
        state_n = []
        state_n.append(self.vel.x / 10) # Car Vel
        state_n.append(self.angle / 360) # Car Angle
        state_n.append((self.steering + 45) / 90) # Car Steering Angle
        for dist in self.sensor_info: # Sensor Dist
            state_n.append(dist[3] / 150)

        return np.asarray(state_n, dtype=np.float)

    def create_sensors(self, size=6, dist=10, skip=6):
        sensor = []
        for ang in self.sensor_steps:
            for i in range(1, size):
                vector = vec(skip + (dist * i), 0).rotate(ang)
                sensor.append([ang, vector])
        
        return sensor

    def update_sensors(self, ang):
        for idx, _ in enumerate(self.sensor):
            self.sensor[idx][1].rotate_ip(ang)

    def hit(self):
        crash = False
        self.car_hits = pg.sprite.spritecollide(self, self.game.obstacles, False, pg.sprite.collide_mask)
        if self.car_hits:
            crash = True
        return crash

    def sensor_dist(self):
        sensor_info = []
        for ang in self.sensor_steps:
            lt = list(filter(lambda x: x[0] == ang, self.sensor))
            sensor_info.append(self.sensor_data(lt))
        return sensor_info

    def sensor_data(self, lt):
        first_point = lt[0][1] + self.pos
        for item in lt:
            coord = item[1] + self.pos
            for obstacle in self.game.obstacles:
                if obstacle.rect.collidepoint(coord):
                    return item[0], first_point, coord, math.sqrt((self.pos[0]-coord[0])**2 + (self.pos[1]-coord[1])**2)
        return item[0], first_point, coord, math.sqrt((self.pos[0]-coord[0])**2 + (self.pos[1]-coord[1])**2)

    def get_target(self):
        target_dist = math.sqrt((self.pos.x-self.target_point[self.car_target][1].x)**2 + (self.pos.y-self.target_point[self.car_target][1].y)**2)

        if target_dist < TARGET_UPDATE:
            if self.car_target >= len(self.target_point)-1:
                self.target_mult += 1
                self.car_target = 0
            else:    
                self.car_target += 1
            #self.start_car = pg.time.get_ticks()
            self.goal = True
            self.loop_time = pg.time.get_ticks()
        
        #self.last_target_dist = self.target_dist
        #self.target_point = self.game.target.get_point()
        self.target_dist = math.sqrt((self.pos.x-self.target_point[self.car_target][1].x)**2 + (self.pos.y-self.target_point[self.car_target][1].y)**2) + self.target_point[self.car_target][2]
        self.target_ang = (self.get_points_ang(self.sensor[0][1], self.target_point[self.car_target][1]) + self.angle) % 360

    def get_points_ang(self, coord_1, coord_2):
        dx = coord_2[0] - coord_1[0]
        dy = coord_2[1] - coord_1[1]
        rads = math.atan2(dy,dx)
        #rads %= 2*math.pi
        ang = math.degrees(rads)
        return ang % 360


class Target():
    def __init__(self, game):
        self.game = game
        self.all_points = []
        self.next_point = []
        self.next_id = 0
        self.before_id = 0
        self.max_id = 0
        
    def add(self, id, x, y):
        self.all_points.append([id, vec(x, y), 0, 0])

    def ini(self):
        self.all_points.sort(key=lambda x: x[0])
        self.max_id = len(self.all_points)-1
        self.next_id = 0
        self.before_id = self.max_id
        dist = 0
        dist_global = 0
        idx = self.max_id
        for val in reversed(self.all_points):
            if idx == self.max_id:
                ini = self.all_points[idx][1]
                end = self.all_points[0][1]
                self.all_points[idx][2] = 0
                self.all_points[idx][3] = math.sqrt((ini.x-end.x)**2 + (ini.y-end.y)**2)
            else:
                ini = self.all_points[idx][1]
                end = self.all_points[idx+1][1]
                dist = math.sqrt((ini.x-end.x)**2 + (ini.y-end.y)**2)
                dist_global += dist
                self.all_points[idx][2] = dist_global
                self.all_points[idx][3] = dist
            idx -= 1
        self.working_points = [self.all_points[self.before_id][1], self.all_points[self.next_id][1], 
                               self.all_points[self.next_id][2], self.all_points[self.before_id][3]]


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((w, h), pg.SRCALPHA)
        self.image.fill(LIGHTGREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pg.mask.from_surface(self.image)


class Map():
    def __init__(self, game):
        self.game = game
        self.tmx = pytmx.load_pygame(path.join(self.game.map_dir, 'race_v2.tmx'), pixelalpha=True)
        self.width = self.tmx.width * self.tmx.tilewidth
        self.height = self.tmx.height * self.tmx.tileheight
        self.load()

    def load(self):
        self.image = pg.Surface((self.width, self.height))
        self.draw(self.image)
        self.rect = self.image.get_rect()

    def draw(self, surface):
        for layer in self.tmx.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = self.tmx.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmx.tilewidth, y * self.tmx.tileheight))


class Camera:
    def __init__(self, game, width, height):
        self.game = game
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def get_coord(self):
        return self.camera.topleft

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
        