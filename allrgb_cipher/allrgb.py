import pygame
import itertools
import os


def show(image_size, pixels, colors, filename=None):
    """Draw [and save] image with the given size and pixel colors.
    """
    pygame.init()
    screen = pygame.display.set_mode(image_size)
    screen.fill((0, 0, 0))
    pygame.display.flip()
    waiting = True

    for pixel, color in zip(pixels, colors):
        x, y = pixel

        # screen.set_at((x*2+1, image_size[1] - 1 - y), color)
        # pygame.display.flip()
        #
        # screen.set_at((x*2, image_size[1]//1 - 1 - y), (color[0]//1, color[1]//1, color[2]//1))
        # pygame.display.flip()
        # print(color)
        screen.set_at((x, image_size[1] - 1 - y), color)
        pygame.display.flip()

        if pygame.QUIT in [ev.type for ev in pygame.event.get()]:
            waiting = False
            break
    if filename is None:
        while waiting and pygame.event.wait().type != pygame.QUIT:
            pass
    else:
        pygame.image.save(screen, filename)
    pygame.quit()
