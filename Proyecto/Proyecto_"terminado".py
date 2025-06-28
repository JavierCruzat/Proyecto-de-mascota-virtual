import pygame, random
from pygame.locals import *

pygame.init()

ancho_ventana=1024
alto_ventana=712
ventana=pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("ChiPet")
tiempo=pygame.time.Clock()

BLANCO=(255,255,255)
NEGRO=(0,0,0)

fondos_niveles=[
    pygame.image.load("Proyecto/imagenes/fondo_nuevo.png"),
    pygame.image.load("Proyecto/imagenes/Fondo.jpg")
]

animal_imagen = pygame.image.load("Proyecto/imagenes/mogus.png")
animal_ancho = animal_imagen.get_width()
animal_alto = animal_imagen.get_height()

objeto_imagenes=[
    pygame.image.load("Proyecto/imagenes/Manzana.png"),
    pygame.image.load("Proyecto/imagenes/hoja.png") 
]
objeto_imagenes_nivel2 = [
    pygame.image.load("Proyecto/imagenes/gota.png"),  
    pygame.image.load("Proyecto/imagenes/explode.png")     
]

texto_puntos = pygame.font.SysFont("comicsans", 40, True)

def pantalla_inicio():
    ventana.fill(NEGRO)
    fuente_titulo = pygame.font.SysFont("comicsans", 50, True)
    fuente_subtitulo = pygame.font.SysFont("comicsans", 20, True)

    texto_titulo = fuente_titulo.render("ChiPet", True, BLANCO)
    texto_comenzar = fuente_subtitulo.render("Pulsa R para comenzar", True, BLANCO)
    texto_controles = fuente_subtitulo.render("Controles (<- ->)", True, BLANCO)
    
    texto_objetivo_titulo = fuente_subtitulo.render("Objetivo:", True, BLANCO)
    texto_linea1 = fuente_subtitulo.render("- Consigue manzana y gotas", True, BLANCO)
    texto_linea2 = fuente_subtitulo.render("- Evita hojas y lodo", True, BLANCO)

    # Dibujar textos en pantalla
    ventana.blit(texto_titulo, texto_titulo.get_rect(center=(ancho_ventana // 2, alto_ventana // 2 - 100)))
    ventana.blit(texto_comenzar, texto_comenzar.get_rect(center=(ancho_ventana // 2, alto_ventana // 2 - 40)))
    ventana.blit(texto_controles, texto_controles.get_rect(center=(ancho_ventana // 2, alto_ventana // 2)))
    ventana.blit(texto_objetivo_titulo, texto_objetivo_titulo.get_rect(center=(ancho_ventana // 2, alto_ventana // 2 + 60)))
    ventana.blit(texto_linea1, texto_linea1.get_rect(center=(ancho_ventana // 2, alto_ventana // 2 + 90)))
    ventana.blit(texto_linea2, texto_linea2.get_rect(center=(ancho_ventana // 2, alto_ventana // 2 + 120)))
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            elif evento.type == KEYDOWN:
                if evento.key == K_r:
                    esperando = False

EVENTO_TIEMPO = pygame.USEREVENT + 1
pygame.time.set_timer(EVENTO_TIEMPO, 1000)

def mostrar_pantalla_nivel(nivel_actual):
    ventana.fill(NEGRO)
    fuente_nivel = pygame.font.SysFont("comicsans", 60, True)
    texto_nivel = fuente_nivel.render(f"Nivel {nivel_actual + 1}", True, BLANCO)
    texto_rect = texto_nivel.get_rect(center=(ancho_ventana // 2, alto_ventana // 2))
    ventana.blit(texto_nivel, texto_rect)
    pygame.display.update()
    pygame.time.delay(2000)

def mostrar_resultado_final(hambre, limpieza, final=False):
    pygame.mixer.music.stop()
    pygame.mixer.music.load("Proyecto/snd/Finalbuenomusica.mp3")
    pygame.mixer.music.play(-1)
    ventana.fill(NEGRO)
    fuente_final = pygame.font.SysFont("comicsans", 30, True)

    if final:
        mensaje = "Tu mascota sufrió de hambre y se fue con dios :("
    elif hambre <= 10 and limpieza >= 80:
        mensaje = "Excelente tu mascota puede ser liberada."
    elif hambre <= 30 and limpieza >= 30:
        mensaje = "¡Buen trabajo! Pero podrías mejorar."
    elif hambre <= 70 and limpieza >= 20:
        mensaje = "Tu mascota no logró recuperarse del todo."
    elif limpieza == 0:
        mensaje = "Tu mascota se enfermó"
    
    texto = fuente_final.render(mensaje, True, BLANCO)
    texto_rect = texto.get_rect(center=(ancho_ventana // 2, alto_ventana // 2))
    ventana.blit(texto, texto_rect)
    pygame.display.update()
    pygame.time.delay(3000)

def pantalla_reintentar():
    ventana.fill(NEGRO)
    fuente = pygame.font.SysFont("comicsans", 35, True)
    texto = fuente.render("¿Quieres reintentarlo? Pulsa R", True, BLANCO)
    texto_rect = texto.get_rect(center=(ancho_ventana // 2, alto_ventana // 2))
    ventana.blit(texto, texto_rect)
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            elif evento.type == KEYDOWN:
                if evento.key == K_r:
                    esperando = False

def jugar_niveles():
    nivel=0
    if nivel==0:
        pygame.mixer.music.load("Proyecto/snd/nivel1musica.mp3")
    elif nivel == 1:
        pygame.mixer.music.load("Proyecto/snd/nivel2musica.mp3")
    pygame.mixer.music.play(-1)

    nivel = 0
    meta_puntos = 100
    puntaje_hambre = 0
    puntaje_limpieza = 0
    esta_jugando = True

    while esta_jugando and nivel < len(fondos_niveles):
        mostrar_pantalla_nivel(nivel)

        if nivel == 0:
            pygame.mixer.music.load("Proyecto/snd/nivel1musica.mp3")
        elif nivel == 1:
            pygame.mixer.music.load("Proyecto/snd/nivel2musica.mp3")
        pygame.mixer.music.play(-1)

        fondo = fondos_niveles[nivel]
        animal_x = (ancho_ventana - animal_ancho) // 2
        animal_y = alto_ventana - animal_alto
        objeto_ancho = 100
        objeto_alto = 100
        objeto_x = random.randint(0, ancho_ventana - objeto_ancho)
        objeto_y = -objeto_alto
        objeto_velocidad = 10
        objeto_tipo = random.choice([0, 1])
        puntaje = 50 if nivel == 0 else 20
        tiempo_nivel = 0
        jugando_nivel = True

        while jugando_nivel:
            tiempo.tick(50)

            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    exit()
                elif evento.type == EVENTO_TIEMPO:
                    tiempo_nivel += 1
                    if nivel == 0:
                        puntaje += 1
                        if puntaje >= 100:
                            mostrar_resultado_final(100, 0, final=True)
                            pantalla_reintentar()
                            return  
                    elif nivel == 1:
                        puntaje -= 1
                        if puntaje < 0:
                            puntaje = 0

            teclas = pygame.key.get_pressed()
            if teclas[K_LEFT] and animal_x - 10 >= 0:
                animal_x -= 10
            if teclas[K_RIGHT] and animal_x + animal_ancho + 10 <= ancho_ventana:
                animal_x += 10

            objeto_y += objeto_velocidad
            if objeto_y > alto_ventana:
                objeto_y = -objeto_alto
                objeto_x = random.randint(0, ancho_ventana - objeto_ancho)
                if objeto_velocidad < 15:
                    objeto_velocidad += 1
                objeto_tipo = random.choice([0, 1])

            # Colisión
            if (objeto_y + objeto_alto > animal_y and animal_y + animal_alto > objeto_y and
                animal_x + animal_ancho > objeto_x and animal_x < objeto_x + objeto_ancho):
                if objeto_tipo == 1:
                    if nivel == 0:
                        puntaje += 5
                    else:
                        puntaje -= 5
                        if puntaje < 0:
                            puntaje = 0
                else:
                    if nivel == 0:
                        puntaje -= 5
                        if puntaje < 0:
                            puntaje = 0
                    else:
                        puntaje += 5
                        if puntaje > 100:
                            puntaje = 100
                objeto_y = -objeto_alto
                objeto_x = random.randint(0, ancho_ventana - objeto_ancho)
                objeto_tipo = random.choice([0, 1])

            ventana.blit(fondo, (0, 0))
            ventana.blit(animal_imagen, (animal_x, animal_y))
            if nivel == 0:
                ventana.blit(objeto_imagenes[objeto_tipo], (objeto_x, objeto_y))
            else:
                ventana.blit(objeto_imagenes_nivel2[objeto_tipo], (objeto_x, objeto_y))

            etiqueta = "Hambre" if nivel == 0 else "Limpieza"
            color_texto = BLANCO if nivel == 0 else NEGRO
            puntos = texto_puntos.render(f"{etiqueta}: {puntaje}", True, color_texto)
            ventana.blit(puntos, (10, 10))
            pygame.display.update()

            if (nivel == 0 and puntaje <= 0) or (nivel == 1 and puntaje >= meta_puntos) or tiempo_nivel >= 30:
                if nivel == 0:
                    puntaje_hambre = puntaje
                elif nivel == 1:
                    puntaje_limpieza = puntaje
                jugando_nivel = False

        nivel += 1

    mostrar_resultado_final(puntaje_hambre, puntaje_limpieza)
    pantalla_reintentar()

pantalla_inicio()
while True:
    jugar_niveles()
