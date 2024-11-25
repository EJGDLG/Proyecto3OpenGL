# Proyecto3OpenGL
![imagen](https://github.com/EJGDLG/Proyecto3OpenGL/blob/ed2c49a0b4cfe6ed819342207c65ffb9e5581821/openGL.PNG)
Configuración inicial:

Importa bibliotecas necesarias como pygame, glm, y módulos personalizados (Renderer, Model, shaders).
Inicializa Pygame y su módulo de mezcla de audio para reproducir música.
Ventana y renderizador:

Crea una ventana OpenGL de 1280x720 píxeles.
Inicializa un objeto Renderer para manejar la renderización de gráficos 3D.
Skybox:

Configura una skybox usando seis texturas para simular el entorno 3D.
Carga de modelos 3D:

Carga modelos 3D desde archivos (Gun.obj, Tiger.obj, etc.).
Asigna texturas y transforma los modelos (escala, rotación, posición).
Shaders:

Asigna shaders de vértices y fragmentos predeterminados.
Permite cambiar dinámicamente los shaders durante la ejecución.
Controles del usuario:

Teclado:
Control de cámara: rotación, zoom, y ajuste de altura.
Cambiar entre modos de visualización (relleno, wireframe).
Alternar y cambiar shaders.
Reproducir/detener música de fondo.
Ratón:
Controla la cámara (rotación y desplazamiento vertical).
Selecciona modelos en la escena.
Cámara:

Usa LookAt para enfocar modelos específicos.
Implementa órbitas alrededor de los modelos seleccionados con un control dinámico de distancia y ángulo.
Bucle principal:

Procesa eventos de entrada (teclado, ratón).
Actualiza transformaciones de cámara y objetos.
Renderiza la escena 3D en cada cuadro.
Audio:

Reproduce música de fondo con ajustes de volumen.
Finalización:

Cierra Pygame de manera segura al salir del programa.
