import pygame as pg
import pymunk.pygame_util
from random import randrange

pymunk.pygame_util.positive_y_is_up = False

RES = WIDTH, HEIGHT = 1200, 800
FPS = 60

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

space = pymunk.Space()
space.gravity = 0, 1500


def create_ball(space, pos):
    ball_mass, ball_radius = 100, 60
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    ball_body = pymunk.Body(ball_mass, ball_moment)
    ball_body.position = pos
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    ball_shape.elasticity = 0.8
    ball_shape.friction = 0.5
    ball_shape.color = [randrange(256) for _ in range(4)]
    space.add(ball_body, ball_shape)


segment_shape = pymunk.Segment(space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 20)
segment_shape.elasticity = 0.8
segment_shape.friction = 0.5
space.add(segment_shape)

wall_shape = pymunk.Segment(space.static_body, (0, 0), (0, WIDTH), 20)
wall_shape.elasticity = 0.5
wall_shape.friction = 0.5
space.add(wall_shape)

wall1_shape = pymunk.Segment(space.static_body, (WIDTH,30), (0, WIDTH), 20)
wall1_shape.elasticity = 0.5
wall1_shape.friction = 0.5
space.add(wall1_shape)


box_mass, box_size = 1, (60, 40)

for x in range(120, WIDTH - 60, box_size[0]):
    for y in range(HEIGHT // 2, HEIGHT - 20, box_size[1]):
        box_moment = pymunk.moment_for_box(box_mass, box_size)
        box_body = pymunk.Body(box_mass, box_moment)
        box_body.position = x, y
        box_shape = pymunk.Poly.create_box(box_body, box_size)
        box_shape.elasticity = 0.1
        box_shape.friction = 1.0
        box_shape.color = [randrange(256) for _ in range(4)]
        space.add(box_body, box_shape)

while True:
    surface.fill(pg.Color('black'))
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                create_ball(space, i.pos)
    space.step(1 / FPS)
    space.debug_draw(draw_options)
    pg.display.flip()
    clock.tick(FPS)
