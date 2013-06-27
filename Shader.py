from PyQt4 import QtCore, QtOpenGL
from PyQt4.QtOpenGL import *
from PyQt4.QtCore import *

'''
Video processing implemented on a QGLFramebuffer and using GLSL programmin
'''
class Shader():
	def __init__(self):
		self.shaderCodes = list()
		
		self.shaderCodes.append(self.getImadjustCode())
		self.shaderCodes.append(self.getMedianCode())
		self.shaderCodes.append(self.getGaussianCode())
		self.shaderCodes.append(self.getHsv2RgbCode())
		self.shaderCodes.append(self.getFluorescenceProcessCode())
		self.shaderCodes.append(self.getJetColormapCode())

	def getImadjustCode(self):
		s = """
			uniform sampler2DRect tex;
			uniform float mn, mx, r, g, b;
			
			void main() {
				gl_FragColor = texture2DRect(tex, gl_TexCoord[0].st);
				if(mn < mx) {
					float s = float(gl_FragColor.g);
					s -= mn;
					s /= (mx -mn);
					s = clamp(s, 0.0, 1.0);
					
					gl_FragColor.r = s * r;
					gl_FragColor.g = s * g;
					gl_FragColor.b = s * b;
				}
			}
		"""
		
		return s
		
	def getMedianCode(self):
		s = """
			uniform sampler2DRect tex;
			
			/*
			3x3 Median
			Morgan McGuire and Kyle Whitson
			http://graphics.cs.williams.edu
			*/

			#define s2(a, b)				temp = a; a = min(a, b); b = max(temp, b);
			#define mn3(a, b, c)			s2(a, b); s2(a, c);
			#define mx3(a, b, c)			s2(b, c); s2(a, c);

			#define mnmx3(a, b, c)			mx3(a, b, c); s2(a, b);                                   // 3 exchanges
			#define mnmx4(a, b, c, d)		s2(a, b); s2(c, d); s2(a, c); s2(b, d);                   // 4 exchanges
			#define mnmx5(a, b, c, d, e)	s2(a, b); s2(c, d); mn3(a, c, e); mx3(b, d, e);           // 6 exchanges
			#define mnmx6(a, b, c, d, e, f) s2(a, d); s2(b, e); s2(c, f); mn3(a, b, c); mx3(d, e, f); // 7 exchanges
			
			void main() {
				vec2 cc = gl_TexCoord[0].st;
				float a[9];
				a[0] = texture2DRect(tex, cc+vec2(-1.0, -1.0)).g;
				a[1] = texture2DRect(tex, cc+vec2(-1.0, 0.0)).g;
				a[2] = texture2DRect(tex, cc+vec2(-1.0, 1.0)).g;
				a[3] = texture2DRect(tex, cc+vec2(0.0, -1.0)).g;
				a[4] = texture2DRect(tex, cc+vec2(0.0, 0.0)).g;
				a[5] = texture2DRect(tex, cc+vec2(0.0, 1.0)).g;
				a[6] = texture2DRect(tex, cc+vec2(1.0, -1.0)).g;
				a[7] = texture2DRect(tex, cc+vec2(1.0, 0.0)).g;
				a[8] = texture2DRect(tex, cc+vec2(1.0, 1.0)).g;
				
				float temp;
				
				mnmx6(a[0], a[1], a[2], a[3], a[4], a[5]);
				mnmx5(a[1], a[2], a[3], a[4], a[6]);
				mnmx4(a[2], a[3], a[4], a[7]);
				mnmx3(a[3], a[4], a[8]);
				
				gl_FragColor = vec4(a[4], a[4], a[4], 1.0);
			}
		"""
		
		return s
		
	def getGaussianCode(self):
		s = """
			uniform sampler2DRect tex;

			void applyGaussianFilter(in int i, in int j, out float o)
			{
				
				int ch = 2;
				
				o = texture2DRect(tex,vec2(i,j)) [ch];
				
				const vec3 gr1 = vec3(6.9624782e-8,  2.8088641754e-5 ,  2.07548549665e-4);
				const vec3 gr2 = vec3(2.8088641754e-5  , 1.1331766853774e-2 ,  8.3731060982536e-2);
				const vec3 gr3 = vec3(2.07548549665e-4 ,8.3731060982536e-2  , 6.18693506822940e-1);
				
				const vec3 one3 = vec3(1.0, 1.0, 1.0);
				const vec2 one = vec2(one3);
				
				mat3 m1 = mat3(texture2DRect(tex,vec2(i-2,j-2)) [ch], texture2DRect(tex,vec2(i-2,j-1)) [ch], texture2DRect(tex,vec2(i-2,j)) [ch], 
								texture2DRect(tex,vec2(i-1,j-2)) [ch], texture2DRect(tex,vec2(i-1,j-1)) [ch], texture2DRect(tex,vec2(i-1,j)) [ch],	
								texture2DRect(tex,vec2(i,j-2)) [ch], texture2DRect(tex,vec2(i,j-1)) [ch], texture2DRect(tex,vec2(i,j)) [ch]);
				mat2 m2 = mat2(texture2DRect(tex,vec2(i+1,j-2)) [ch], texture2DRect(tex,vec2(i+1,j-1)) [ch], 
								texture2DRect(tex,vec2(i+2,j-2)) [ch], texture2DRect(tex,vec2(i+2,j-1)) [ch]);
								
				mat2 m3 = mat2(texture2DRect(tex,vec2(i+1,j)) [ch], texture2DRect(tex,vec2(i+1,j+1)) [ch], 
								texture2DRect(tex,vec2(i+2,j)) [ch], texture2DRect(tex,vec2(i+2,j+1)) [ch]);
								
				mat2 m4 = mat2(texture2DRect(tex,vec2(i-2,j+2)) [ch], texture2DRect(tex,vec2(i-2,j+1)) [ch], 
								texture2DRect(tex,vec2(i-1,j+2)) [ch], texture2DRect(tex,vec2(i-1,j+1)) [ch]);
								
				o = dot(matrixCompMult(m1,mat3(gr1, gr2, gr3)) * one3, one3);
				o += dot(matrixCompMult(m2,mat2(vec2(gr2), vec2(gr1))) * one, one);
				o += dot(matrixCompMult(m3,mat2(vec2(gr2), vec2(gr1))) * one, one);
				o += dot(matrixCompMult(m3,mat2(gr2[2], gr2[1], gr1[2], gr1[1])) * one, one);
				o += texture2DRect(tex,vec2(i,j+1)) [ch] * gr3[1];
			}

				
			void main()
			{
				gl_FragColor = texture2DRect(tex,gl_TexCoord[0].st);
				
				int i = int(gl_TexCoord[0].s);
				int j = int(gl_TexCoord[0].t);
				
				float o = 0.0;
				
				applyGaussianFilter(i, j, o);
				
				gl_FragColor.r = o;
				gl_FragColor.g = o;
				gl_FragColor.b = o;
				gl_FragColor.a = 1.0;
				//gl_FragColor[0] = gl_FragColor[2];
			}
		"""
		
		return s
		
	def getHsv2RgbCode(self):
		s = """
			uniform sampler2DRect view1, bckView;

			uniform float hmn;
			uniform float hmx;
			uniform float mn;
			uniform float mx;
			
			vec3 h2r(float h, float s, float v) {
				return mix(vec3(1.),clamp((abs(fract(h+vec3(3.,2.,1.)/3.)*6.-3.)-1.),0.,1.),s)*v;
			}

			void hsv2rgb(inout vec4 c)
			{
				float h = c.r * 6.0;
				int hi = int(floor(h));
				
				h = h - float(hi);
				float p = c.b * (1.0 - c.g);
				float q = c.b * (1.0 - h * c.g);
				float t = c.b * (1.0 - (1.0 - h) * c.g);
				
				switch (hi)
				{
					case 0:
						c.r = c.b;
						c.g = t;
						c.b = p;
						break;
					case 1:
						c.r = q;
						c.g = c.b;
						c.b = p;
						break;
					case 2:
						c.r = p;
						c.g = c.b;
						c.b = t;
						break;
					case 3:
						c.r = p;
						c.g = q;
						break;
					case 4:
						c.r = t;
						c.g = p;
						break;
					case 5:
						c.r = c.b;
						c.g = p;
						c.b = q;
						break;
					default:
						break;
				}
			}

				
			void main()
			{
				vec4 c = vec4(0.0, 0.0, 0.0, 1.0);
				//gl_FragColor = c;
				
				//int i = int(gl_TexCoord[0].s);
				//int j = int(gl_TexCoord[0].t);
				
				float s = texture2DRect(view1, gl_TexCoord[0].st).g;
				float tv = texture2DRect(bckView, gl_TexCoord[0].st).g;
				
				if( hmn < hmx )
				{
					
					s -= hmn;
					s /= (hmx-hmn);
					
					s = clamp(s, 0.0, 1.0);
					c.r = s;
					
					c.g = 1.0;
					
					tv -= mn;
					tv /= (mx-mn);
					
					tv = clamp(tv, 0.0, 1.0);
					c.b = tv;
					//c.b = 1.0;
				}
				
				c.r = 0.63 * (1.0 - c.r); //select a certain range for hue
				//hsv2rgb(c);
				//gl_FragColor = c;
				
				gl_FragColor = vec4(h2r(c.r, c.g, c.b), 1.0);
				
			}
		"""
		
		return s
		
	def getFluorescenceProcessCode(self):
		s = """
			uniform sampler2DRect f1, f2, ref;
			
			uniform int procType, dispType;
			uniform float bck1, bck2;

			void main() {
				float v1 = texture2DRect(f1, gl_TexCoord[0].st).g * 65535.0 - float(bck1);
				float v2 = 0.0;
				
				int f2Clip = 0;
				
				if(procType == 1) {
					v2 = texture2DRect(f2, gl_TexCoord[0].st).g * 65535.0 - float(bck2);
					if(v2 > 0.0) {
						v2 = max(v2, 0.0001);
					} else {
						v2 = min(v2, -0.0001);
					}
					
					v1 /= v2;
				}
				float r = 0.0;
				if(dispType > 0) {
					r = texture2DRect(ref, gl_TexCoord[0].st).g;
					
					if(dispType == 1) {
						v1 -= r;
					} else {
						if(r > 0.0) {
							r = max(r, 0.0001);
						} else {
							r = min(r, -0.0001);
						}
					
						v1 /= r;
					}
				}
				
				gl_FragColor = vec4(v1, v1, v1, 1.0);
			}
		"""
		
		return s
		
	def getJetColormapCode(self):
		s = """
			uniform sampler2DRect f1;
			uniform float mapMn;
			uniform float mapMx;

			void main() {
				float v1 = texture2DRect(f1, gl_TexCoord[0].st).r;
				v1 -= mapMn;
				v1 /= (mapMx - mapMn);
				
				v1 = clamp(v1, 0.0, 0.9);
				
				v1 *= 4.0;
				float r = min(v1 - 1.5, -v1 + 4.5);
				float g = min(v1 - 0.5, -v1 + 3.5);
				float b = min(v1 + 0.5, -v1 + 2.5);
				r = clamp(r, 0.0, 1.0);
				g = clamp(g, 0.0, 1.0);
				b = clamp(b, 0.0, 1.0);
				
				gl_FragColor = vec4(r, g, b, 1.0);
			}
		"""
		
		return s
		
	def getShader(self, code):
		sh = QGLShader(QGLShader.Fragment)
		sh.compileSourceCode(code)
		
		return sh

	def __del__(self):
		pass
	
