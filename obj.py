from pygame import image
import pygame
from OpenGL.GL import *
import glm # pip install PyGLM
import numpy as np
class Obj:
    def __init__(self, filename):
        self.vertices = []
        self.texCoords = []
        self.normals = []
        self.faces = []

        self.vao = glGenVertexArrays(1)
        self.vbo_vertices = glGenBuffers(1)
        self.vbo_normals = glGenBuffers(1)
        self.vbo_texCoords = glGenBuffers(1)

        self.load_obj(filename)

    def load_obj(self, filename):
        try:
            with open(filename, "r") as file:
                lines = file.read().splitlines()
        except FileNotFoundError:
            raise Exception(f"Archivo {filename} no encontrado.")

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(" ", 1)
            prefix = parts[0]
            value = parts[1] if len(parts) > 1 else ""

            if prefix == "v":
                self.vertices.append(list(map(float, value.split())))
            elif prefix == "vt":
                self.texCoords.append(list(map(float, value.split()[:2])))
            elif prefix == "vn":
                self.normals.append(list(map(float, value.split())))
            elif prefix == "f":
                face = [list(map(int, v.split("/"))) for v in value.split()]
                self.faces.append(face)

    def bind_data_to_shader(self, shader_program):
        glBindVertexArray(self.vao)

        # Vértices
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_vertices)
        glBufferData(GL_ARRAY_BUFFER, np.array(self.vertices, dtype=np.float32), GL_STATIC_DRAW)
        glVertexAttribPointer(shader_program["a_position"], 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(shader_program["a_position"])

        # Normales
        if self.normals:
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo_normals)
            glBufferData(GL_ARRAY_BUFFER, np.array(self.normals, dtype=np.float32), GL_STATIC_DRAW)
            glVertexAttribPointer(shader_program["a_normal"], 3, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(shader_program["a_normal"])

        # Coordenadas de textura
        if self.texCoords:
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo_texCoords)
            glBufferData(GL_ARRAY_BUFFER, np.array(self.texCoords, dtype=np.float32), GL_STATIC_DRAW)
            glVertexAttribPointer(shader_program["a_texCoord"], 2, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(shader_program["a_texCoord"])

        glBindVertexArray(0)

    def load_texture(self, texture_filename):
        try:
            img = pygame.image.load(texture_filename)
        except pygame.error:
            raise Exception(f"No se pudo cargar la textura: {texture_filename}")
        
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        img_data = pygame.image.tostring(img, "RGBA", True)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.get_width(), img.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return texture
