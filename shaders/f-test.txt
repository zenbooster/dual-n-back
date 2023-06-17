uniform vec2      iResolution;           // viewport resolution (in pixels)
uniform float     iTime;                 // shader playback time (in seconds)


bool isInside = false;

mat2 r2d (float deg) {
	float rad = radians (deg);
	float c = cos (rad);
	float s = sin (rad);
	return mat2 (c,s,-s,c);
}

float smin (float d1, float d2, float k) {
	float h = clamp (.5 + .5*(d2 - d1)/k, .0, 1.);
	return mix (d2, d1, h) - h*k*(1. - h);
}

float sdBox (in vec3 p, in vec3 size, in float r)
{
	vec3 d = abs(p) - size;
	return min (max (d.x, max (d.y,d.z)), .0) + length (max (d, .0)) - r;
}

float map (vec3 p, inout int id, inout vec3 pout) {
	//float ground = p.y + 1.;
	float wall = p.z + 1.;
	vec3 pbox = p + vec3 (.0, -.4, -.2);
	pbox.xz *= r2d (14.*iTime);
	pbox.yz *= r2d (26.*iTime);
	float r = .75 + .1*(.5+.5*cos(4.*iTime + 9.*pbox.y));
	float box = sdBox (pbox, vec3 (.6), .05);
	p -= vec3 (2.5*cos (1.25*iTime), .75, .2);
	p.xz *= r2d (-60.*iTime);
	p.yz *= r2d (-90.*iTime);
	float ball = sdBox (p , vec3 (.4), .05);
	box = (isInside? -1. : 1.)*smin (box, ball, .5);
	//float d = min (ground, min (wall, box));
    float d = min (wall, box);
	//if (d == ground) {id = 1; pout = p;}
	if (d == wall) {id = 2; pout = p;}
	if (d == box) {id = 3; pout = p;}
    return d;
}

float march (vec3 ro, vec3 rd, inout int id, inout vec3 pout)
{
	float t = .0;
	float d = .0;
	for (int i = 0; i< 48; ++i) {
		vec3 p = ro+d*rd;
		t = map (p, id, pout);
		if (abs (t) < .00001*(1. + .125*t)) break;
		d += t*.75;
	}
	return d;
}

vec3 norm (vec3 p){
	int foo;
	vec3 bar;
	float d = map (p, foo, bar);
	vec2 e = vec2 (.001, .0);
	return normalize (vec3 (map (p+e.xyy, foo, bar),
                            map (p+e.yxy, foo, bar),
                            map (p+e.yyx, foo, bar))-d);
}

float sha (vec3 p, vec3 lp, vec3 n, vec3 ldir) {
	float d2l = distance (lp, p);
	int foo;
	vec3 bar;
	float d2w = march (p+.01*n, ldir, foo, bar);
	return d2l < d2w ? 1. : .1;
}

float ao (vec3 p, vec3 n, float stepsize, int iter, float i){
	float ao = .0;
	float dist = .0;
	int foo;
	vec3 bar;
	for (int a = 1; a <= iter; ++a) {
		dist = float (a)*stepsize;
		ao += max (.0, (dist - map (p+n*dist, foo, bar))/dist);
	}
	return 1. - ao*i;
}

vec3 cam (vec2 uv, vec3 ro, vec3 aim, float zoom) {
	vec3 f =normalize (aim - ro);
	vec3 wu = vec3 (.0, 1., .0);
	vec3 r = normalize (cross (wu, f));
	vec3 u = normalize (cross (f, r));
	vec3 c = ro + f*zoom;
	return normalize (c + r*uv.x+u*uv.y - ro);
}

float PI = 3.14159265;
uniform sampler2D iChannel0;
uniform sampler2D imageTexture;

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    //float time = mod(iTime + 1000.0, 2.0*PI);
    float time = iTime;
	vec2 uvRaw = fragCoord.xy/iResolution.xy;
	vec2 uv = uvRaw*2. - 1.;
	uv.x *= iResolution.x/iResolution.y;
	uv *= 1. + .25*length (uv);

	vec3 ro = vec3 (cos (time), 1. + .125*(.5+.5*cos(5.*time)), 2.5);
	vec3 rd = cam (uv, ro, vec3 (.0), 1.7);
	int id = 0;
	vec3 pout = vec3 (.0);
	isInside = false;
	float d = march (ro, rd, id, pout);
	vec3 p = ro + d*rd;
	vec3 n = norm (p);
	vec3 col = vec3 (.0);

	vec3  lp1 = vec3 (2., 1., 2.);
	vec3  lc1 = vec3 (.9, .8, .7);
	float li1 = 3.;
	vec3  lp2 = vec3 (.7, 3., .0);
	vec3  lc2 = vec3 (.2, .2, .9);
	float li2 = 6.;
	vec3  lp3 = vec3 (-2., 2., .5);
	vec3  lc3 = vec3 (.9, .3, .2);
	float li3 = 3.;

	float fac = 1.;
	if (id == 3) {
		fac = .025;
	}

	col = texture(imageTexture, fragCoord).rgb;
	//col = vec3(fragCoord, 1.0);

	if (id == 3) {
		//n = normalize (n + texture (iChannel0, .125*p.xy).r);
        //col.g = (col.g + texture (iChannel0, .125*p.xy).r*1.0) * 0.5;
		ro = p - .05*n;
		float ior = .7;
		rd = normalize (refract (rd, n, ior));
		isInside = true;
		d = march (ro, rd, id, pout);
		p = ro + d*rd;
		n = norm (p);
        col = (col + texture (imageTexture, .125*p.xy).rgb) * 0.5;

		ro = p - .01*n;
		rd = normalize (refract (rd, n, ior));
		isInside = false;
		d = march (ro, rd, id, pout);
		p = ro + d*rd;
		n = norm (p);
        col = (col + texture (imageTexture, .125*p.xy).rgb) * 0.5;

	}
    else
    if (id == 2)
        col = vec3(0.0, 0.0, 0.0);

	//col = col / (1. + col);
	//col *= 1. - .5*length(uvRaw*2.-1.);
	//col = pow (col, vec3 (1./2.2));

    fragColor = vec4(col, 1.);
}

in vec2 fragmentTexCoord;

void main() {
	vec4 color;
	mainImage(color, fragmentTexCoord);

	if (color.rgb == vec3(0.0))
	{
		gl_FragColor = texture2D(imageTexture, fragmentTexCoord);
	}
	else
	{
		gl_FragColor = color;
	}
}