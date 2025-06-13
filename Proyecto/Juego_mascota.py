import pygame, random
from pygame.locals import *

pygame.init()

# Dimensiones ventana
ancho_ventana = 1024
alto_ventana = 712
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("JuegoProyecto")
tiempo = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Fondo por nivel
fondos_niveles = [
    pygame.image.load("imagenes/fondo.jpg"),
    pygame.image.load("imagenes/fondoej2.jpg"),
    #pygame.image.load("imagenes/mogus2.jpg")
]

# Jugador
animal_imagen = pygame.image.load("imagenes/mogus.png")
#animal_explosion = pygame.image.load("imagenes/")
animal_velocidad = 10
animal_ancho = animal_imagen.get_width()
animal_alto = animal_imagen.get_height()
animal_x = (ancho_ventana - animal_ancho) // 2
animal_y = alto_ventana - animal_alto

# Texto
texto_puntos = pygame.font.SysFont("comicsans", 30, True)

# Objetos
objeto_imagenes = [
    pygame.image.load("imagenes/Manzana.png"),  # normal
    pygame.image.load("imagenes/mogus4.png")    # trampa
]

# Juego
nivel = 0
meta_puntos = 20
esta_jugando = True

while esta_jugando and nivel < len(fondos_niveles):
    # Variables del nivel
    puntaje = 0
    objeto_ancho = 100
    objeto_alto = 100
    objeto_x = random.randint(0, ancho_ventana - objeto_ancho)
    objeto_y = -objeto_alto
    objeto_velocidad = 10
    objeto_tipo = random.choice([0, 1])
    fondo = fondos_niveles[nivel]

    # Tiempo por nivel
    tiempo_limite = 30000  # 30 segundos por nivel
    inicio_nivel = pygame.time.get_ticks()

    nivel_activo = True
    while nivel_activo:
        tiempo.tick(60)
        tiempo_actual = pygame.time.get_ticks()
        tiempo_restante = max(0, (tiempo_limite - (tiempo_actual - inicio_nivel)) // 1000)

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()

        # Movimiento jugador
        teclas = pygame.key.get_pressed()
        if teclas[K_LEFT] and animal_x - animal_velocidad >= 0:
            animal_x -= animal_velocidad
        if teclas[K_RIGHT] and animal_x + animal_ancho + animal_velocidad <= ancho_ventana:
            animal_x += animal_velocidad

        # Movimiento objeto
        objeto_y += objeto_velocidad
        if objeto_y > alto_ventana:
            objeto_y = -objeto_alto
            objeto_x = random.randint(0, ancho_ventana - objeto_ancho)
            objeto_velocidad += 1
            objeto_tipo = random.choice([0, 1])

        # Colisión
        if (objeto_y + objeto_alto > animal_y and animal_y + animal_alto > objeto_y and
            animal_x + animal_ancho > objeto_x and animal_x < objeto_x + objeto_ancho):
            if objeto_tipo == 1:
                puntaje = 0
            else:
                puntaje += 5
            objeto_y = -objeto_alto
            objeto_x = random.randint(0, ancho_ventana - objeto_ancho)
            objeto_tipo = random.choice([0, 1])

        # Comprobación de condiciones de fin del nivel
        if puntaje >= meta_puntos or tiempo_actual - inicio_nivel >= tiempo_limite:
            nivel += 1
            nivel_activo = False
            break

        # Dibujo en pantalla
        ventana.blit(fondo, (0, 0))
        ventana.blit(animal_imagen, (animal_x, animal_y))
        ventana.blit(objeto_imagenes[objeto_tipo], (objeto_x, objeto_y))

        # Mostrar puntaje
        texto_puntaje = texto_puntos.render("Puntaje: " + str(puntaje), True, NEGRO)
        ventana.blit(texto_puntaje, (10, 10))

        # Mostrar tiempo restante
        texto_tiempo = texto_puntos.render(f"Tiempo: {tiempo_restante}s", True, NEGRO)
        ventana.blit(texto_tiempo, (ancho_ventana - 180, 10))

        pygame.display.update()

# Fin del juego
ventana.fill(BLANCO)
texto_final = texto_puntos.render("¡Juego Terminado!", True, NEGRO)
ventana.blit(texto_final, ((ancho_ventana - texto_final.get_width()) // 2, alto_ventana // 2))
pygame.display.update()
pygame.time.delay(3000)
pygame.quit()
