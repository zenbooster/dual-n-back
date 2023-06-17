#version 330

uniform vec2      iResolution;           // viewport resolution (in pixels)
uniform float     iTime;                 // shader playback time (in seconds)
uniform float     iTimeDelta;            // render time (in seconds)
uniform float     iFrameRate;            // shader frame rate
uniform int       iFrame;                // shader playback frame
uniform float     iChannelTime[4];       // channel playback time (in seconds)
uniform vec3      iChannelResolution[4]; // channel resolution (in pixels)
uniform vec4      iMouse;                // mouse pixel coords. xy: current (if MLB down), zw: click
//uniform samplerXX iChannel0..3;          // input channel. XX = 2D/Cube
uniform sampler2D iChannel0;          // input channel. XX = 2D/Cube
uniform sampler2D iChannel1;
uniform sampler2D iChannel2;
uniform sampler2D iChannel3;
uniform vec4      iDate;                 // (year, month, day, time in seconds)
uniform vec2      iOffset;               // pixel offset for tiled rendering
//This was an experiment so I could learn some GLSL.
//Thanks to vug for his tutorial!  I also referenced swellbastion to use a texture for noise. Thank you!

#define PI 3.14159265359

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 p = vec2(fragCoord.xy / iResolution.xy); 
	//aspect ratio
    vec2 r =  2.0*vec2(fragCoord.xy - 0.5*iResolution.xy)/iResolution.y;
    //coordinates [0,1]  origin is the bottom left
    
	//animate
    float t = iTime;
    r = r * 8.0;
	
 //https://www.shadertoy.com/view/Md23DV   
    //vertical lines
    float v1 = sin(r.x +t);
    //vertical waves
    float v2 = sin(r.y +t);
    //diagonal
    float v3 = sin(r.x+r.y +t);
    //rings
    float v4 = sin(sqrt(r.x*r.x+r.y*r.y) +5.0*t);
    //blobs
	float v = v1+v2+v3+v4;
	
	vec3 ret;	
	// mix colors
	v *= 1.0;
	ret = vec3(sin(v), sin(v+(.5+t)*PI), sin(v+1.0*PI)-.5);
			
	ret = 0.5 + 0.5*ret;

    //ret.xy /= 10;
    //ret.z /= 4;

    ret.xy /= 8;
    ret.z /= 3;
	
    vec3 pixel = ret;
      
    
    p.y -= 0.5;
    fragColor = vec4(pixel, 1.0);
}

in vec2 fragmentTexCoord;

void main() {
    mainImage(gl_FragColor, fragmentTexCoord);
}