import glm # pip install PyGLM

from numpy import array, float32

# pip install PyOpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class Buffer(object):
	def __init__(self, data):
		
		self.data = array(data, float32)
		
		# Vertex Buffer Object
		self.bufferObject = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.bufferObject)
		
		# Mandar la informacion de vertices
		glBufferData(GL_ARRAY_BUFFER,	# Buffer ID
					 self.data.nbytes,	# Buffer size in bytes
					 self.data,			# Buffer data
					 GL_STATIC_DRAW)	# Usage
		
		
	def Use(self, attribNumber, size):
		
		# Atar los buffer objects a la tarjeta de video
		glBindBuffer(GL_ARRAY_BUFFER, self.bufferObject)
		
		# Atributo
		glEnableVertexAttribArray(attribNumber)
		
		glVertexAttribPointer(attribNumber,			# Attribute number
							  size,					# Size
							  GL_FLOAT,				# Type
							  GL_FALSE,				# Is it normalized?
							  0,					# Stride size in bytes
							  ctypes.c_void_p(0))	# Offset

