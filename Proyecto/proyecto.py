import pygame
from pygame.locals import *

pygame.init()
ventana_x=1024
ventana_y=712

ventana=pygame.display.set_mode((ventana_x,ventana_y))
pygame.display.set_caption("Prototipo")
reloj=pygame.time.Clock()

Fondoimagen=pygame.image.load('Proyecto/imagenes/fondoej.jpg')
pet_image = pygame.image.load("Proyecto/imagenes/mogus3.jpg")

fuente = pygame.font.SysFont(None,46) #esto es para la fuente de texto y el 46 el tamaño. 

#esto es para "definir" los valores que tendra la mascota, en esta version solo sera una para simplificar las tareas
class Pet:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.hambre = 100 #Siempre empezara el valor en 100
        self.felicidad = 100
        self.image = pet_image

    def draw(self,surface): #El surface es por lo que entendi para que la imagen, en este caso de la mascota, salga sobre el fondo
        surface.blit(self.image, (self.x, self.y))

    def alimentar(self):
        self.hambre=min(100,self.hambre+10)

    def jugar(self):
        self.felicidad=min(100,self.felicidad+10)
    
    def resta_stats(self):  #no sabia que nombre colocarle a la disminucion del hambre y felicidad
        self.hambre=max(0,self.hambre -0.005)  #Esto establece que el hambre tenga como minimo 0 y el 0,5 es un ejemplo de la velocidad a la que disminuye
        self.felicidad=max(0,self.felicidad -0.003) #mismo caso de arriba

    def valor_stats(self,surface):#esto de los valores es pa que se vean en pantalla
        texto_hambre=fuente.render(f"Hambre: {round(self.hambre,2)}", True, (255,255,255))
        texto_felicidad=fuente.render(f"Felicidad: {round(self.felicidad,2)}", True, (255,255,255))
        surface.blit(texto_felicidad,(50,50))
        surface.blit(texto_hambre,(50,100))

pet = Pet(400, 356)

repetir=True
while repetir:

    esta_jugando=True
    while esta_jugando:
        reloj.tick(30)
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                quit()
        
        ventana.blit(Fondoimagen, (0,0))
        pet.draw(ventana)
        pet.valor_stats(ventana)
        pet.resta_stats()

        pygame.display.flip()

pygame.quit()

#estoy cansado jefe
