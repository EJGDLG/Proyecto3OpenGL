from obj import Obj
from buffer import Buffer
from pygame import image
from OpenGL.GL import *
import glm

class Model:
    def __init__(self, filename):
        self.objFile = Obj(filename)
        self.translation = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)
        self.textures = []
        self.materials = {}
        self.vertexCount = 0
        self.visible = True
        self.BuildBuffers()

    def GetModelMatrix(self):
        identity = glm.mat4(1)
        translateMat = glm.translate(identity, self.translation)
        pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        yawMat = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        rollMat = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        rotationMat = pitchMat * yawMat * rollMat
        scaleMat = glm.scale(identity, self.scale)
        return translateMat * rotationMat * scaleMat

    def BuildBuffers(self):
        positions, texCoords, normals, tangents = [], [], [], []

        for face in self.objFile.faces:
            try:
                facePositions = [self.objFile.vertices[vertex[0] - 1] for vertex in face]
                faceTexCoords = [
                    self.objFile.texCoords[vertex[1] - 1] if vertex[1] > 0 else [0, 0]
                    for vertex in face
                ]
                faceNormals = [
                    self.objFile.normals[vertex[2] - 1] if len(vertex) > 2 and vertex[2] > 0 else [0, 0, 1]
                    for vertex in face
                ]

                deltaPos1 = glm.vec3(*[b - a for a, b in zip(facePositions[0], facePositions[1])])
                deltaPos2 = glm.vec3(*[b - a for a, b in zip(facePositions[0], facePositions[2])])
                deltaUV1 = glm.vec2(*[b - a for a, b in zip(faceTexCoords[0], faceTexCoords[1])])
                deltaUV2 = glm.vec2(*[b - a for a, b in zip(faceTexCoords[0], faceTexCoords[2])])

                r = 1.0 / (deltaUV1.x * deltaUV2.y - deltaUV1.y * deltaUV2.x)
                tangent = glm.normalize((deltaPos1 * deltaUV2.y - deltaPos2 * deltaUV1.y) * r)

                for i in range(len(face)):
                    positions.extend(facePositions[i])
                    texCoords.extend(faceTexCoords[i])
                    normals.extend(faceNormals[i])
                    tangents.extend(tangent)

                self.vertexCount += 3
            except ZeroDivisionError:
                print("Warning: Degenerate UV mapping in face skipped.")

        self.positionBuffer = Buffer(positions)
        self.texCoordsBuffer = Buffer(texCoords)
        self.normalsBuffer = Buffer(normals)
        self.tangentBuffer = Buffer(tangents)

    def AddTexture(self, textureFilename, textureType="diffuse"):
        textureSurface = image.load(textureFilename)
        textureData = image.tostring(textureSurface, "RGB", True)
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGB,
            textureSurface.get_width(),
            textureSurface.get_height(),
            0, GL_RGB, GL_UNSIGNED_BYTE, textureData
        )
        glGenerateMipmap(GL_TEXTURE_2D)
        self.materials[textureType] = texture

    def Render(self):
        if not self.visible:
            return

        for i, texture in enumerate(self.materials.values()):
            glActiveTexture(GL_TEXTURE0 + i)
            glBindTexture(GL_TEXTURE_2D, texture)

        self.positionBuffer.Use(0, 3)
        self.texCoordsBuffer.Use(1, 2)
        self.normalsBuffer.Use(2, 3)
        self.tangentBuffer.Use(3, 3)

        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glDisableVertexAttribArray(3)
