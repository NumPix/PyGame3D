from __future__ import annotations

import pygame
from pygame.locals import *

from functions import *
from Vector3 import Vector3
from Vector2 import Vector2

from Objects import *

RESOLUTION = WIDTH, HEIGHT = 16 * 10, 9 * 10
PIXEL_SIZE = 15
SIZE = WIDTH * PIXEL_SIZE, HEIGHT * PIXEL_SIZE
ASPECT = WIDTH / HEIGHT

MOVE_SPEED = 1
ROTATION_SPEED = 1

flags = DOUBLEBUF
screen = pygame.display.set_mode(SIZE, flags, 16)


reflection_rate = 1


camera_angle_x, camera_angle_y, camera_angle_z = 0, 5, -15

camera_x, camera_y, camera_z = -1.2974417223129857, 5.83266712670274, -3.3973386615901227

camera_angle = Vector3(0, 0, 0)

objects = [Box(Vector3(1, 0, 0), Vector3(1, 1, 1), Vector3(255, 0, 0)), Sphere(Vector3(-3, 0, 0), 1, Vector3(0, 255, 0)), Plane(Vector3(0, 0, -1), 1), Sphere(Vector3(0, -4, -.5), 1.5, Vector3(127, 127, 0))]


def draw():
    screen = pygame.display.set_mode(SIZE)

    colors = [Vector3(i, i, i) for i in range(256)]

    global camera_angle
    camera_direction = Vector3(1, 0, 0)
    camera_direction = rotate_x(camera_direction, camera_angle_x * 0.1)
    camera_direction = rotate_y(camera_direction, camera_angle_y * 0.1)
    camera_direction = rotate_z(camera_direction, camera_angle_z * 0.1)

    camera_angle = camera_direction

    for i in range(WIDTH):
        for j in range(HEIGHT):

            uv: Vector2 = Vector2(i, j) / Vector2(WIDTH, HEIGHT) * 2 - 1
            uv.x *= ASPECT

            camera_position: Vector3 = Vector3(camera_x, camera_y, camera_z)
            ray = normalize(Vector3(2, uv.x, uv.y))
            light_sources: [Vector3, ...] = [normalize(Vector3(-5, 0, 1))]

            ray = rotate_x(ray, camera_angle_x * 0.1)
            ray = rotate_y(ray, camera_angle_y * 0.1)
            ray = rotate_z(ray, camera_angle_z * 0.1)

            light_level = 0
            color = Vector3(0, 0, 0)

            diff = 0

            for k in range(10):
                closest_intersection = 999999
                n = Vector3(0, 0, 0)

                albedo = 1

                for render_object in objects:
                    if type(render_object) == Sphere:
                        intersection = sphere(camera_position - render_object.position, ray, render_object.radius)

                        if 0 < intersection.x < closest_intersection:
                            if k == 0:
                                color = render_object.color
                            intersection_point = camera_position - render_object.position + ray * intersection.x
                            closest_intersection = intersection.x
                            n = normalize(intersection_point)

                    elif type(render_object) == Box:
                        intersection, normal = box(camera_position, ray, render_object.position, render_object.size)

                        if 0 < intersection.x < closest_intersection:
                            if k == 0:
                                color = render_object.color
                            closest_intersection = intersection.x
                            n = normal

                    elif type(render_object) == Plane:
                        intersection = plane(camera_position, ray, render_object.p, render_object.w)

                        if 0 < intersection < closest_intersection:
                            if k == 0:
                                color = render_object.color
                            closest_intersection = intersection
                            n = render_object.p
                            albedo = .5

                if closest_intersection < 999999:
                    for source in light_sources:
                        diff = (dot(n, source) * .5 + .5) * albedo / (k * k / reflection_rate + 1)
                        light_level += int(diff * 50 / len(light_sources))
                    camera_position = camera_position + ray * (closest_intersection - 0.01)
                    ray = reflect(ray, n)
                else:
                    break

            light_level = clamp(light_level, 0, len(colors) - 1)

            pygame.draw.rect(screen, tuple(map(int, vec2tup(colors[light_level] / len(colors) * normalize(color) * 255))), (i * PIXEL_SIZE, j * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    while True:
        draw()
        for evt in pygame.event.get():
            if evt.type == QUIT:
                pygame.quit()
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_p:
                    print(camera_x, camera_y, camera_z)
                    print(camera_angle_x, camera_angle_y, camera_angle_z)

        if pygame.key.get_pressed()[pygame.K_q]:
            camera_angle_x += ROTATION_SPEED
        elif pygame.key.get_pressed()[pygame.K_e]:
            camera_angle_x -= ROTATION_SPEED

        if pygame.key.get_pressed()[pygame.K_w]:
            camera_angle_y -= ROTATION_SPEED
        elif pygame.key.get_pressed()[pygame.K_s]:
            camera_angle_y += ROTATION_SPEED

        if pygame.key.get_pressed()[pygame.K_d]:
            camera_angle_z += ROTATION_SPEED
        elif pygame.key.get_pressed()[pygame.K_a]:
            camera_angle_z -= ROTATION_SPEED

        if pygame.key.get_pressed()[pygame.K_UP]:
            camera_x += MOVE_SPEED * camera_angle.x
            camera_y += MOVE_SPEED * camera_angle.y
            camera_z += MOVE_SPEED * camera_angle.z
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            camera_x -= MOVE_SPEED * camera_angle.x
            camera_y -= MOVE_SPEED * camera_angle.y
            camera_z -= MOVE_SPEED * camera_angle.z

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            camera_x += MOVE_SPEED * camera_angle.y
            camera_y -= MOVE_SPEED * camera_angle.x
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            camera_x -= MOVE_SPEED * camera_angle.y
            camera_y += MOVE_SPEED * camera_angle.x

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            camera_z -= MOVE_SPEED
        elif pygame.key.get_pressed()[pygame.K_LSHIFT]:
            camera_z += MOVE_SPEED

        if pygame.key.get_pressed()[pygame.K_KP_PLUS]:
            reflection_rate += 0.1
        elif pygame.key.get_pressed()[pygame.K_KP_MINUS]:
            reflection_rate -= 0.1

