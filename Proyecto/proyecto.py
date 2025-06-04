import pygame
from pygame.locals import *

pygame.init()
ventana_x=1024
ventana_y=712

ventana=pygame.display.set_mode((ventana_x,ventana_y))
pygame.display.set_caption("Prototipo")
reloj=pygame.time.Clock()

def fondo_pantalla():
    ventana.blit(Fondoimagen, (0,0))
    pygame.display.update()

pet_image = pygame.image.load("Proyecto/imagenes/mogus3.jpg")
pet_image = pygame.transform.scale(pet_image, (100, 100))

#esto es para "definir" los valores que tendra la mascota, en esta version solo sera una para simplificar las tareas
class Pet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.happiness = 100
        self.image = pet_image

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


pet = Pet(256, 178)

repetir=True
while repetir:

    Fondoimagen=pygame.image.load('Proyecto/imagenes/fondoej.jpg')

    esta_jugando=True
    while esta_jugando:
        reloj.tick(60)
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                quit()
        fondo_pantalla()
        pet.draw(ventana)
        pygame.display.update()

pygame.quit()
