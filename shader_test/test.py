import sys
import pygame
import pygame_shaders

pygame.init()

w = 1000
h = 1000
screen = pygame.display.set_mode((w, h), pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE)
display = pygame.Surface((w, h))
display.set_colorkey((0, 0, 0))

shd_plasma = pygame_shaders.Shader((w, h), (w, h), (0, 0), "shaders/v-plasma.txt", "shaders/f-plasma.txt", display)
shd_blit = pygame_shaders.Shader((w, h), (w, h), (0, 0), "shaders/v-blit.txt", "shaders/f-blit.txt", display)

clock = pygame.time.Clock()

dt = 1.0

while True:
    display.fill((0, 0, 0)) #Fill with the color you set in the colorkey
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    #pygame.draw.rect(display, (0, 255, 0), (20, 20, 160, 160)) #Draw a red rectangle to the display at (20, 20)
    shd_plasma.send('iResolution', [1, 1])
    shd_plasma.send("iTime", [dt])
    shd_plasma.render(display) #Render the display onto the OpenGL display with the shaders!
    shd_blit.render(display)
    dt += 0.01
    pygame.display.flip()
    clock.tick(60)
