#version 330

/*in vec2 in_vert;
in vec2 in_uv;
out vec2 v_uv;

void main()
{
    gl_Position = vec4(in_vert, 0.0, 1.0);
    v_uv = in_uv;
}
*/
in vec2 vertexPos;
in vec2 vertexTexCoord;
//in vec2 in_vert;
//in vec2 in_uv;
out vec2 fragmentTexCoord;

void main()
{
    //gl_Position = vec4(vertexPos, 0.0, 1.0);
    //fragmentTexCoord = vertexTexCoord;
    gl_Position = vec4(vertexPos, 0.0, 1.0);
    fragmentTexCoord = vertexTexCoord;
}