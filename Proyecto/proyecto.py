import pygame
from pygame.locals import *

pygame.init()
ventana_x=1280
ventana_y=720

ventana=pygame.display.set_mode((ventana_x,ventana_y))
pygame.display.set_caption("Prototipo")
reloj=pygame.time.Clock()

def fondo_pantalla():
    ventana.blit(Fondoimagen, (460,180))
    pygame.display.update()

repetir=True
while repetir:

    Fondoimagen=pygame.image.load('Proyecto/imagenes/mogus.jpg')

    esta_jugando=True
    while esta_jugando:
        reloj.tick(27)
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                quit()
        fondo_pantalla()
pygame.quit()
