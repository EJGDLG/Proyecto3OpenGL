
# Vertex Shaders

vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normal;
layout (location = 3) in vec3 tangent;

out vec2 outTexCoords;
out vec4 outPosition;
out vec3 outNormals;
out mat3 TBN;

uniform float time;
uniform vec3 scale;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    outPosition = modelMatrix * vec4(position, 1.0);
	gl_Position = projectionMatrix * viewMatrix * outPosition;
    
    outTexCoords = texCoords;
    outNormals = normalize(vec3(modelMatrix * vec4(normal,    0.0)));
    
    vec3 T = normalize(vec3(modelMatrix * vec4(tangent,    0.0)));
    T = normalize(T - dot(T, outNormals) * outNormals);
    vec3 B = cross(outNormals, T);
    TBN = mat3(T, B, outNormals);    
}
'''

# Fragment Shaders

fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec4 outPosition;
in vec3 outNormals;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

out vec4 fragColor;

void main()
{
    vec3 lightDir = normalize(pointLight - outPosition.xyz);
    float intensity = max(dot(outNormals, lightDir) , 0) + ambientLight;
	fragColor = texture(tex0, outTexCoords) * intensity;
}
'''
distortion_shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;
out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;
void main()
{
  outPosition = modelMatrix * vec4(position + normals * sin(time) /10, 1.0);
  gl_Position = proyectionMatrix * viewMatrix * outPosition;
  outTextCoords =  textCoords;
  outNormals = normals;
}
"""



water_shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;
out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;
void main()
{
  outPosition = modelMatrix * vec4(position + vec3(0,1,0) * sin(time * position.x *10) /10, 1.0);
  gl_Position = proyectionMatrix * viewMatrix * outPosition;
  outTextCoords =  textCoords;
  outNormals = normals;
}
"""

negative_shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;


out vec4 fragColor;
uniform sampler2D tex;
void main()
{
  fragColor = 1 - texture(tex, outTextCoords);
}
"""

Wobble_Shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;
out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;

void main()
{
    float wobble = sin(time * 5.0 + position.y * 10.0) / 10.0;
    outPosition = modelMatrix * vec4(position + wobble * normals, 1.0);
    gl_Position = proyectionMatrix * viewMatrix * outPosition;
    outTextCoords = textCoords;
    outNormals = normals;
}
"""

Twist_Shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;
out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;

void main()
{
    float angle = position.y * 0.5 + time * 0.5;
    mat4 twistMatrix = mat4(
        cos(angle), 0.0, -sin(angle), 0.0,
        0.0, 1.0, 0.0, 0.0,
        sin(angle), 0.0, cos(angle), 0.0,
        0.0, 0.0, 0.0, 1.0
    );
    outPosition = modelMatrix * twistMatrix * vec4(position, 1.0);
    gl_Position = proyectionMatrix * viewMatrix * outPosition;
    outTextCoords = textCoords;
    outNormals = normals;
}

"""

Ripple_Shader  = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;
out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;

void main()
{
    float distance = length(position.xz);
    float offset = sin(distance * 10.0 - time * 5.0) / 20.0;
    outPosition = modelMatrix * vec4(position + offset * normals, 1.0);
    gl_Position = proyectionMatrix * viewMatrix * outPosition;
    outTextCoords = textCoords;
    outNormals = normals;
}

"""
Glow_Shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;
in vec4 outPosition;

out vec4 fragColor;
uniform sampler2D tex;
uniform vec3 pointLight;

void main()
{
    float intensity = dot(outNormals, normalize(pointLight - outPosition.xyz));
    intensity = pow(intensity, 2.0); // Ajuste para darle más suavidad
    fragColor = texture(tex, outTextCoords) * vec4(1.0, 1.0, 1.0, 1.0) * intensity * 1.5;
}
"""

Sepia_Shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;

out vec4 fragColor;
uniform sampler2D tex;

void main()
{
    vec4 color = texture(tex, outTextCoords);
    float gray = dot(color.rgb, vec3(0.3, 0.59, 0.11)); // Escala de grises
    fragColor = vec4(gray * vec3(1.2, 1.0, 0.8), color.a); // Aplicar tono sepia
}

"""