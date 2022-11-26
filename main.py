from __future__ import annotations

import pygame
from pygame.locals import *
from functions import *
from Objects import *


RESOLUTION = WIDTH, HEIGHT = 1920, 1080
PIXEL_SIZE = 1
SIZE = WIDTH * PIXEL_SIZE, HEIGHT * PIXEL_SIZE
ASPECT = WIDTH / HEIGHT

MOVE_SPEED = 1
ROTATION_SPEED = 1

screen = pygame.display.set_mode(SIZE, DOUBLEBUF, 16)


reflection_rate = 3


camera_angle_x, camera_angle_y, camera_angle_z = 0, 5, -15

camera_x, camera_y, camera_z = -1.2974417223129857, 5.83266712670274, -3.3973386615901227

camera_angle = np.array([0, 0, 0])

objects = [Box(np.array([1, 0, 0]), np.array([1, 1, 1]), np.array([255, 0, 0])),
           Sphere(np.array([-3, 0, 0]), 1, np.array([0, 255, 0])),
           Plane(np.array([0, 0, -1]), 1),
           Sphere(np.array([0, -4, -.5]), 1.5, np.array([127, 127, 0]))]


def draw(screen, objects):

    colors = [np.array([i, i, i]) for i in range(256)]

    camera_direction = np.array([1, 0, 0])
    camera_direction = rotate_x(camera_direction, camera_angle_x * 0.1)
    camera_direction = rotate_y(camera_direction, camera_angle_y * 0.1)
    camera_direction = rotate_z(camera_direction, camera_angle_z * 0.1)

    for i in range(WIDTH):
        for j in range(HEIGHT):

            uv = np.array([i, j]) / np.array([WIDTH, HEIGHT]) * 2 - 1
            uv[0] *= ASPECT

            camera_position = np.array([camera_x, camera_y, camera_z])
            ray = normalize(np.array([2, uv[0], uv[1]]))
            light_sources = [normalize(np.array([-5, 0, 1]))]

            ray = rotate_x(ray, camera_angle_x * 0.1)
            ray = rotate_y(ray, camera_angle_y * 0.1)
            ray = rotate_z(ray, camera_angle_z * 0.1)

            light_level = 0
            color = np.array([0, 0, 0])

            diff = 0

            for k in range(10):
                closest_intersection = 999999
                n = np.array([0, 0, 0])

                albedo = 1

                for render_object in objects:
                    if type(render_object) == Sphere:
                        intersection = sphere(camera_position - render_object.position, ray, render_object.radius)

                        if 0 < intersection[0] < closest_intersection:
                            if k == 0:
                                color = render_object.color
                            intersection_point = camera_position - render_object.position + ray * intersection[0]
                            closest_intersection = intersection[0]
                            n = normalize(intersection_point)

                    elif type(render_object) == Box:
                        intersection = box(camera_position, ray, render_object.position, render_object.size)
                        normal = box_normal(camera_position, ray, render_object.position, render_object.size)

                        if 0 < intersection[0] < closest_intersection:
                            if k == 0:
                                color = render_object.color
                            closest_intersection = intersection[0]
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
                        light_level += int(diff * 90 / len(light_sources))
                    camera_position = camera_position + ray * (closest_intersection - 0.01)
                    ray = reflect(ray, n)
                else:
                    break

            light_level = clamp(light_level, 0, len(colors) - 1)

            draw_color = tuple(map(int, tuple(colors[light_level] / len(colors) * normalize(color) * 255)))

            pygame.draw.rect(screen, draw_color, (i * PIXEL_SIZE, j * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    pygame.display.flip()
    return camera_direction


if __name__ == '__main__':
    pygame.init()
    while True:
        camera_angle = draw(screen, objects)
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
            camera_x += MOVE_SPEED * camera_angle[0]
            camera_y += MOVE_SPEED * camera_angle[1]
            camera_z += MOVE_SPEED * camera_angle[2]
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            camera_x -= MOVE_SPEED * camera_angle[0]
            camera_y -= MOVE_SPEED * camera_angle[1]
            camera_z -= MOVE_SPEED * camera_angle[2]

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            camera_x += MOVE_SPEED * camera_angle[1]
            camera_y -= MOVE_SPEED * camera_angle[0]
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            camera_x -= MOVE_SPEED * camera_angle[1]
            camera_y += MOVE_SPEED * camera_angle[0]

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            camera_z -= MOVE_SPEED
        elif pygame.key.get_pressed()[pygame.K_LSHIFT]:
            camera_z += MOVE_SPEED

        if pygame.key.get_pressed()[pygame.K_KP_PLUS]:
            reflection_rate += 0.1
        elif pygame.key.get_pressed()[pygame.K_KP_MINUS]:
            reflection_rate -= 0.1

