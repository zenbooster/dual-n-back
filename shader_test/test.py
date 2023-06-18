import sys
import pygame
import pygame_shaders


class csApp:
    def resize(self, sz):
        print(f'HIT.1: sz={sz}')
        w, h = sz
        screen = pygame.display.set_mode((w, h), pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
        self.display = display = pygame.Surface((w, h))
        display.set_colorkey((0, 0, 0))
        self.shd_plasma = pygame_shaders.Shader((w, h), (w, h), (0, 0), "shaders/v-default.txt", "shaders/f-golfing-ether.txt", display)
        #self.shd_plasma = pygame_shaders.Shader((w, h), (w, h), (0, 0), "shaders/v-default.txt", "shaders/f-smoke-mirrors.txt", display)
        self.shd_blit = pygame_shaders.Shader((w, h), (w, h), (0, 0), "shaders/v-blit.txt", "shaders/f-blit.txt", display)
    
    def __init__(self):
        pygame.init()

        self.resize((1000, 1000));
        self.clock = pygame.time.Clock()
        self.dt = 1.0

    def run(self):
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
            self.dt += 0.01
            pygame.display.flip()
            self.clock.tick(60)

csApp().run()