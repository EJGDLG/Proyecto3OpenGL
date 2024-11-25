import pygame
from pygame.locals import *
from gl import Renderer
from model import Model
from shaders import *
import glm

width = 1280
height = 720

pygame.init()

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
                renderer.ToggleFilledMode()  # Asegúrate de que el método ToggleFilledMode() exista
            # Cambiar entre modos de renderizado
            elif event.key == pygame.K_F1:
                renderer.filledMode()
            elif event.key == pygame.K_F2:
                renderer.WireFrameMode()

            # Cambiar shaders de vértices
            elif event.key == pygame.K_F3:
                vShader = vertex_shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F4:
                vShader = distortion_shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F5:
                vShader = water_shader
                renderer.SetShaders(vShader, fShader)

            # Cambiar shaders de fragmentos
            elif event.key == pygame.K_F6:
                fShader = fragment_shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F7:
                fShader = negative_shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F8:
                fShader = Wobble_Shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F9:
                fShader = Twist_Shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F10:
                fShader = Ripple_Shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F11:
                fShader = Glow_Shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F12:
                fShader = Sepia_Shader
                renderer.SetShaders(vShader, fShader)

 # Movimiento de la cámara con límites para camHeight y camDistance
    if keys[K_LEFT]:
        faceModel.rotation.y -= 45 * deltaTime
    if keys[K_RIGHT]:
        faceModel.rotation.y += 45 * deltaTime
    if keys[K_UP]:
        camHeight = min(2, camHeight + 10 * deltaTime)      # Mover cámara hacia arriba con límite
    if keys[K_DOWN]:
        camHeight = max(-2, camHeight - 10 * deltaTime)     # Mover cámara hacia abajo con límite

    if keys[K_PAGEUP]:
        renderer.pointLight.y += 1 * deltaTime

    if keys[K_PAGEDOWN]:
        renderer.pointLight.y -= 1 * deltaTime

    if keys[K_a]:
        camAngle -= 45 * deltaTime

    if keys[K_d]:
        camAngle += 45 * deltaTime

    if keys[K_w]:
        if camDistance > 2:
            camDistance -= 2 * deltaTime

    if keys[K_s]:
        if camDistance < 10:
            camDistance += 2 * deltaTime

    if keys[K_q]:
        if renderer.camera.position.y < 2:
            renderer.camera.position.y += 5 * deltaTime

    if keys[K_e]:
        if renderer.camera.position.y > -2:
            renderer.camera.position.y -= 5 * deltaTime

    if pygame.mouse.get_pressed()[0]:
        camAngle -= mouseVel[0] * deltaTime * 5

        if mouseVel[1] > 0 and renderer.camera.position.y < 2:
            renderer.camera.position.y += mouseVel[1] * deltaTime

        if mouseVel[1] < 0 and renderer.camera.position.y > -2:
            renderer.camera.position.y += mouseVel[1] * deltaTime

    # Actualizar la cámara
    renderer.camera.LookAt(glm.vec3(faceModel.translation.x, faceModel.translation.y + camHeight, faceModel.translation.z))
    renderer.camera.Orbit(center=faceModel.translation, distance=camDistance, angle=camAngle)

    renderer.Render()

    renderer.time += deltaTime
    pygame.display.flip()

pygame.quit()











