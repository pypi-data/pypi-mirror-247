$HEADER$

uniform vec2 resolution;
uniform float time;

void main(void)
{
	vec4 frag_coord = frag_modelview_mat * gl_FragCoord;
	float x = frag_coord.x;
	float y = frag_coord.y;
	float mov0 = x+y+cos(sin(time)*2.)*100.+sin(x/100.)*1000.;
	float mov1 = y / resolution.y / 0.2 + time;
	float mov2 = x / resolution.x / 0.2;
	float c1 = abs(sin(mov1+time)/2.+mov2/2.-mov1-mov2+time);
	float c2 = abs(sin(c1+sin(mov0/1000.+time)+sin(y/40.+time)+sin((x+y)/100.)*3.));
	float c3 = abs(sin(c2+cos(mov1+mov2+c2)+cos(mov2)+sin(x/1000.)));
	gl_FragColor = vec4( c1*0.05,c2*0.2,c3*0.2,1.0);
}
