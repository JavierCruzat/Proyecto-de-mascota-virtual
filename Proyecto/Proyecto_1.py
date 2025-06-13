import pygame
from pygame.locals import *
import time
import math 

pygame.init()
ventana_x=1024
ventana_y=712

ventana=pygame.display.set_mode((ventana_x,ventana_y))
pygame.display.set_caption("Prototipo")
reloj=pygame.time.Clock()

Fondoimagen=pygame.image.load('Proyecto/imagenes/fondoej.jpg')
pet_image=pygame.image.load("Proyecto/imagenes/mogus3.jpg")

boton_alimento_imag=pygame.image.load("Proyecto/imagenes/ArbolProyecto.png")
boton_alimento_rect=boton_alimento_imag.get_rect(topleft=(600,110))

boton_felicidad_imag=pygame.image.load("Proyecto/imagenes/LagoProyecto.png")
boton_felicidad_rect=boton_felicidad_imag.get_rect(topleft=(0,100))

fuente = pygame.font.SysFont(None,46) #esto es para la fuente de texto y el 46 el tamaño.

#esto es para "definir" los valores que tendra la mascota, en esta version solo sera una para simplificar las tareas
class Pet:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.original_y = y
        self.hambre = 100
        self.felicidad = 100
        self.image = pet_image
        self.movimiento_comida = False
        self.inicio_movimiento_comida = 0
        self.duracion_movimiento = 3 
        self.velocidad_movimiento = 5 

    def draw(self,surface):
        surface.blit(self.image, (self.x, self.y))

    def alimentar(self):
        self.hambre=min(100,self.hambre+10)
        self.movimiento_comida = True
        self.inicio_movimiento_comida = time.time()

    def jugar(self):
        self.felicidad=min(100,self.felicidad+10)

    def resta_stats(self):  #no sabia que nombre colocarle a la disminucion del hambre y felicidad
        self.hambre=max(0,self.hambre -0.015)  #el 0,5 es un ejemplo de la velocidad a la que disminuye
        self.felicidad=max(0,self.felicidad -0.3)

    def valor_stats(self,surface):#esto de los valores es pa que se vean en pantalla
        texto_hambre=fuente.render(f"Hambre: {round(self.hambre,1)}", True, (255,255,255))
        texto_felicidad=fuente.render(f"Felicidad: {round(self.felicidad,1)}", True, (255,255,255))
        surface.blit(texto_felicidad,(50,50))
        surface.blit(texto_hambre,(50,100))

    #moviemiento de la mascota
    def pos_estandar(self):
        if (self.felicidad>=80 and self.hambre>=80):
            self.x=400
            self.y=356
    def mov_feli(self):
        if self.felicidad<=60:
            self.x=300
            self.y=356
            if self.felicidad<=40:
                self.x=200
                self.y=356
    def mov_hambre(self):
        if self.hambre<=90:
            self.x=500
            self.y=356
            if self.hambre<=40:
                self.x=600
                self.y=356
#MOVIMIENTO AL COMER :)
    def animacion_alimentar(self):
        current_time = time.time()
        elapsed_time = current_time - self.inicio_movimiento_comida

        if elapsed_time < self.duracion_movimiento:
            
            self.y = self.original_y + 10 * math.sin(elapsed_time * 10)
        else:
            self.movimiento_comida = False
            self.y = self.original_y 

pet = Pet(400, 356)

repetir=True
while repetir:
    reloj.tick(60) 

    for evento in pygame.event.get():
        if evento.type==pygame.QUIT:
            repetir = False 
        if evento.type==pygame.MOUSEBUTTONDOWN:
            if boton_alimento_rect.collidepoint(evento.pos):
                pet.alimentar() 
            if boton_felicidad_rect.collidepoint(evento.pos):
                pet.jugar()

    if pet.movimiento_comida:
        pet.animacion_alimentar()
    else:
        pet.pos_estandar() 
        pet.mov_feli()
        pet.mov_hambre()


    ventana.blit(Fondoimagen, (0,0))
    pet.draw(ventana)
    pet.valor_stats(ventana)
    pet.resta_stats()

    ventana.blit(boton_alimento_imag, boton_alimento_rect.topleft)
    ventana.blit(boton_felicidad_imag,boton_felicidad_rect.topleft)
    pygame.display.flip()

pygame.quit()
