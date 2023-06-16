import sys
import pygame
import pygame_shaders

pygame.init()

w = 200
h = 200
screen = pygame.display.set_mode((w, h), pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE)
display = pygame.Surface((w, h))
display.set_colorkey((0, 0, 0))

shader = pygame_shaders.Shader((w, h), (w, h), (0, 0), "shaders/vertex.txt", "shaders/fragment.txt", display)
shader_1 = pygame_shaders.Shader((w, h), (w, h), (0, 0), "shaders/vertex_1.txt", "shaders/fragment_1.txt", display)

clock = pygame.time.Clock()

dt = 1.0

while True:
    display.fill((0, 0, 0)) #Fill with the color you set in the colorkey
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.draw.rect(display, (0, 255, 0), (20, 20, 160, 160)) #Draw a red rectangle to the display at (20, 20)
    shader.send('iResolution', [1, 1])
    shader.send("iTime", [dt])
    shader.render(display) #Render the display onto the OpenGL display with the shaders!
    shader_1.render(display)
    dt += 0.1
    pygame.display.flip()
    clock.tick(60)
