import glm # pip install PyGLM
# pip install PyOpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from camera import Camera
from skybox import Skybox


class Renderer(object):
	def __init__(self, screen):
		self.screen = screen
		_, _, self.width, self.height = screen.get_rect()
		
		
		glEnable(GL_DEPTH_TEST)
		self.filledMode = False
		self.ToggleFilledMode()
		
		glViewport(0,0, self.width, self.height)
		
		self.camera = Camera(self.width, self.height)
		
		self.time = 0
		self.value = 0
		
		self.pointLight = glm.vec3(0,0,0)
		self.ambientLight = 0.1
		
		
		self.scene = [ ]
		self.active_shaders = None
		
		self.skybox = None
		

	def CreateSkybox(self, textureList):
		self.skybox = Skybox(textureList)
		
	def ToggleFilledMode(self):
		self.filledMode = not self.filledMode
		
		if self.filledMode:
			glEnable(GL_CULL_FACE)
			glPolygonMode(GL_FRONT, GL_FILL)
		else:
			glDisable(GL_CULL_FACE)
			glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

	def SetShaders(self, vShader, fShader):
		if vShader is not None and fShader is not None:
			vertex = compileShader(vShader, GL_VERTEX_SHADER)
			fragment = compileShader(fShader, GL_FRAGMENT_SHADER)
			self.active_shaders = compileProgram( vertex, fragment)
			
		else:
			self.active_shaders = None

		
	def Render(self):
		glClearColor(0.2, 0.2, 0.2, 1.0)
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		
		self.camera.Update()
		
		if self.skybox is not None:
			
			self.skybox.cameraRef = self.camera
			self.skybox.Render()
		
		if self.active_shaders is not None:
			glUseProgram(self.active_shaders)

			glUniform1f(glGetUniformLocation(self.active_shaders, "time"), self.time)
			
			glUniform1i(glGetUniformLocation(self.active_shaders, "tex0"), 0);
			glUniform1i(glGetUniformLocation(self.active_shaders, "tex1"), 1);
			
			glUniformMatrix4fv( glGetUniformLocation(self.active_shaders, "viewMatrix"),
								1, GL_FALSE, glm.value_ptr( self.camera.viewMatrix ))
			
			glUniformMatrix4fv( glGetUniformLocation(self.active_shaders, "projectionMatrix"),
								1, GL_FALSE, glm.value_ptr( self.camera.projectionMatrix ))
			
			glUniform3fv(glGetUniformLocation(self.active_shaders, "pointLight"), 1, glm.value_ptr(self.pointLight))
			glUniform1f(glGetUniformLocation(self.active_shaders, "ambientLight"), self.ambientLight)
			
			glUniform3fv(glGetUniformLocation(self.active_shaders, "cameraPos"), 1, glm.value_ptr(self.camera.position))
		

		for obj in self.scene:
			
			if self.active_shaders is not None:
				glUniformMatrix4fv( glGetUniformLocation(self.active_shaders, "modelMatrix"),
									1, GL_FALSE, glm.value_ptr( obj.GetModelMatrix()))
				
				glUniform3fv(glGetUniformLocation(self.active_shaders, "scale"), 1, glm.value_ptr(obj.scale))


			obj.Render()
		