import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from src.system.periscope import Periscope
from src.system.target import Target

RED = (1.0, 0., 0.)
WHITE = (1., 1., 1.)
BLUE = (0., 0.6, 1.)
GREEN = (0, 240, 10)
BLACK = (0., 0., 0.,)

verticies = (
    (0.02, -0.02, -0.02),
    (0.02, 0.02, -0.02),
    (-0.02, 0.02, -0.02),
    (-0.02, -0.02, -0.02),
    (0.02, -0.02, 0.02),
    (0.02, 0.02, 0.02),
    (-0.02, -0.02, 0.02),
    (-0.02, 0.02, 0.02)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )


def draw_cube(coords):
    glPushMatrix()
    glTranslatef(coords[0], coords[1], coords[2])

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()
    glPopMatrix()

def draw_lines(points, closed = False, color_l = WHITE):
    n = len(points)
    iters = n if closed else n - 1
    glBegin(GL_LINES)
    glColor3f(color_l[0], color_l[1], color_l[2])
    for i in range(iters):
        glVertex3fv(points[i])
        glVertex3fv(points[(i + 1) % n])

    glEnd()

def draw_sphere(coords, radius, color_s = BLUE):
    quad: gluNewQuadric = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_LINE)
    glColor3f(color_s[0], color_s[1], color_s[2])

    glPushMatrix()
    glTranslatef(coords[0], coords[1], coords[2])

    gluSphere(quad, radius, 12, 12)
    glPopMatrix()

class Renderer:
    def __init__(self, periscope: Periscope = None):
        display = (800, 500)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        gluPerspective(45, (display[0] / display[1]), 0.0, 10.0)

        glTranslatef(-0.4, -0.5, -1)

        self.periscope: Periscope = periscope

    def render(self, p1_intersect, p2_intersect, p3_intersect, target: Target, p_aim):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.__render_geometry(p1_intersect, p2_intersect, p3_intersect, target, p_aim)
        pygame.display.flip()


    def __render_geometry(self, p1_intersect, p2_intersect, p3_intersect, target: Target, p_aim):

        draw_lines(self.periscope.mirror_down.triangle.get_points(), True)
        draw_lines(self.periscope.mirror_up.triangle.get_points(), True)
        draw_lines(self.periscope.mirror_3.triangle.get_points(), True)

        draw_lines((self.periscope.laser.startPos.get_point(), p1_intersect.get_point(),
                    p2_intersect.get_point(), p3_intersect.get_point(), p_aim.get_point()), False, RED)
        draw_sphere(target.location.get_point(), target.radius)
        draw_sphere(p_aim.get_point(), 0.004, GREEN)
        draw_cube(self.periscope.laser.startPos.get_point())

