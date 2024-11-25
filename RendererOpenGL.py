import pygame
from pygame.locals import *
from gl import Renderer
from model import Model
from shaders import *
import glm

width = 1280
height = 720

pygame.init()

# Inicializar el módulo de música
pygame.mixer.init()

# Cargar el archivo de música de fondo
pygame.mixer.music.load("sounds/Call-of-Duty-2-Theme.mp3")  # Cambia "Call-of-Duty-2-Theme.mp3" por la ruta de tu archivo
pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen (0.0 a 1.0)

# Cargar el sonido del revolver
revolver_sound = pygame.mixer.Sound("sounds/revolver.mp3")  # Cambia "revolver.mp3" por la ruta de tu archivo
revolver_sound.set_volume(1.0)  # Ajusta el volumen del sonido

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

renderer = Renderer(screen)

# Texturas de la Skybox
skyboxTextures = [
    "skybox/right.jpg",
    "skybox/left.jpg",
    "skybox/top.jpg",
    "skybox/bottom.jpg",
    "skybox/front.jpg",
    "skybox/back.jpg"
]
renderer.CreateSkybox(skyboxTextures)

# Modelos y sus propiedades
faceModel = Model("models/Gun.obj")
faceModel.AddTexture("textures/Gun.bmp")
faceModel.translation = glm.vec3(-20, -0.5, 1)  # Posición
faceModel.scale = glm.vec3(2, 2, 2)

moonModel = Model("models/Tiger.obj")
moonModel.AddTexture("textures/Tank_Body_Desert.BMP")
moonModel.translation = glm.vec3(-10, -4, -5)  # Posición
moonModel.scale = glm.vec3(0.005, 0.005, 0.005)

spidey = Model("models/Tiger-Destroyed.obj")
spidey.AddTexture("textures/Tank_Body_Destroyed.BMP")
spidey.translation = glm.vec3(170, -4, 100)  # Posición
spidey.scale = glm.vec3(0.02, 0.02, 0.02)

helicopter = Model("models/Helicopter.obj")
helicopter.AddTexture("textures/tex.png")
helicopter.translation = glm.vec3(0, 8, -5)  # Posición
helicopter.scale = glm.vec3(0.05, 0.05, 0.05)

# Añadir modelos a la escena
renderer.scene.extend([faceModel, moonModel, spidey, helicopter])

# Shaders iniciales
vShader = vertex_shader
fShader = fragment_shader
renderer.SetShaders(vShader, fShader)

# Variables de la cámara y selección de modelos
camDistance = 5
camAngle = 0
camHeight = 0
modelIndex = 0
isRunning = True
mouseX, mouseY = pygame.mouse.get_pos()

while isRunning:

    deltaTime = clock.tick(60) / 1000

    keys = pygame.key.get_pressed()
    mouseVel = pygame.mouse.get_rel()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.MOUSEWHEEL:
            if event.y < 0 and camDistance < 10:
                camDistance -= event.y * deltaTime * 10
            if event.y > 0 and camDistance > 2:
                camDistance -= event.y * deltaTime * 10

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:
                modelIndex += 1
                modelIndex %= len(renderer.scene)
                for i in range(len(renderer.scene)):
                    renderer.scene[i].visible = i == modelIndex

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_SPACE:
                renderer.ToggleFilledMode()
            elif event.key == pygame.K_h:
                revolver_sound.play()  # Reproducir el sonido del revolver
            elif event.key == pygame.K_j:
                if not pygame.mixer.music.get_busy():  # Verifica si la música no está sonando
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.stop()  # Detener música si ya está sonando

    # Movimiento de la cámara
    if keys[K_LEFT]:
        faceModel.rotation.y -= 45 * deltaTime
    if keys[K_RIGHT]:
        faceModel.rotation.y += 45 * deltaTime
    if keys[K_UP]:
        camHeight = min(2, camHeight + 10 * deltaTime)
    if keys[K_DOWN]:
        camHeight = max(-2, camHeight - 10 * deltaTime)
    if keys[K_w] and camDistance > 2:
        camDistance -= 2 * deltaTime
    if keys[K_s] and camDistance < 10:
        camDistance += 2 * deltaTime
    if keys[K_a]:
        camAngle -= 45 * deltaTime
    if keys[K_d]:
        camAngle += 45 * deltaTime

    # Actualizar la cámara
    renderer.camera.LookAt(glm.vec3(faceModel.translation.x, faceModel.translation.y + camHeight, faceModel.translation.z))
    renderer.camera.Orbit(center=faceModel.translation, distance=camDistance, angle=camAngle)

    renderer.Render()
    renderer.time += deltaTime
    pygame.display.flip()

pygame.quit()
