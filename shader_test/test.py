import sys
import pygame
import pygame_shaders

#OpenGL
import OpenGL 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *

import cv2
import numpy as np

from PIL import Image

class csApp:
    def ScreenShot(self, filename):
        width, height = self.w, self.h
        glReadBuffer(GL_FRONT)
        pixels = glReadPixels(0,0,width,height,GL_RGB,GL_UNSIGNED_BYTE)
        
        image = Image.frombytes("RGB", (width, height), pixels)
        image = image.transpose( Image.FLIP_TOP_BOTTOM)
        image.save(filename)

    def cnvt_pil_to_cv2(pil_img):
        open_cv_image = np.array(pil_img) 
        # Convert RGB to BGR 
        open_cv_image = open_cv_image[:, :, ::-1].copy()     
        return open_cv_image

    def ScreenRec(self):
        width, height = self.w, self.h
        glReadBuffer(GL_FRONT)
        pixels = glReadPixels(0,0,width,height,GL_RGB,GL_UNSIGNED_BYTE)
        
        image = Image.frombytes("RGB", (width, height), pixels)
        image = image.transpose( Image.FLIP_TOP_BOTTOM)
        #image.save(filename)
        self.out.write(csApp.cnvt_pil_to_cv2(image))

    def resize(self, sz):
        #print(f'HIT.1: sz={sz}')
        self.w, self.h = w, h = sz
        self.out = cv2.VideoWriter('output.avi',self.fourcc, 20.0, sz)
        self.screen = pygame.display.set_mode((w, h), pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
        self.display = display = pygame.Surface((w, h))
        display.set_colorkey((0, 0, 0))
        self.shd_plasma = pygame_shaders.Shader((w, h), (w, h), (0, 0), "shaders/v-default.txt", "shaders/f-golfing-ether.txt", display)
        #self.shd_plasma = pygame_shaders.Shader((w, h), (w, h), (0, 0), "shaders/v-default.txt", "shaders/f-smoke-mirrors.txt", display)
        self.shd_blit = pygame_shaders.Shader((w, h), (w, h), (0, 0), "shaders/v-blit.txt", "shaders/f-blit.txt", display)
    
    def __init__(self):
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        pygame.init()

        self.resize((1000, 1000));
        self.clock = pygame.time.Clock()
        self.dt = 1.0

    def run(self):
        is_captured = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    self.resize(event.dict['size'])
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            display = self.display
            display.fill((0, 0, 0)) #Fill with the color you set in the colorkey
 
            #pygame.draw.rect(display, (0, 255, 0), (20, 20, 160, 160)) #Draw a red rectangle to the display at (20, 20)
            shd_plasma = self.shd_plasma
            shd_plasma.send('iResolution', [1, 1])
            shd_plasma.send("iTime", [self.dt])
            #print('HIT.4')
            shd_plasma.render(display) #Render the display onto the OpenGL display with the shaders!
            #print('HIT.5')
            self.shd_blit.render(display)
            #print('HIT.6')
            self.dt += 0.1
            #self.dt += 0.2
            pygame.display.flip()
            self.ScreenRec()
            if not is_captured:
                self.ScreenShot("screenshot.jpeg")
                is_captured = True

            self.clock.tick(60)

csApp().run()