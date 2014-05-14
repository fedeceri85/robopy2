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
			#extension GL_ARB_texture_rectangle : enable
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
			#extension GL_ARB_texture_rectangle : enable
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
			#extension GL_ARB_texture_rectangle : enable
			uniform sampler2DRect tex;
				
			void main()
			{
				vec2 b = gl_TexCoord[0].st;
				gl_FragColor = texture2DRect(tex, b) * 50.7167019;
				
				vec4 t = texture2DRect(tex, b + vec2(-2, -2));
				t += texture2DRect(tex, b + vec2(-2, 2));
				t += texture2DRect(tex, b + vec2(2, -2));
				t += texture2DRect(tex, b + vec2(2, 2));
				gl_FragColor += t  * 32.518554;
				
				t = texture2DRect(tex, b + vec2(-2, -1));
				t += texture2DRect(tex, b + vec2(-2, +1));
				t += texture2DRect(tex, b + vec2(2, -1));
				t += texture2DRect(tex, b + vec2(2, 1));
				t += texture2DRect(tex, b + vec2(-1, -2));
				t += texture2DRect(tex, b + vec2(1, -2));
				t += texture2DRect(tex, b + vec2(-1, 2));
				t += texture2DRect(tex, b + vec2(1, 2));
				gl_FragColor += t * 38.4161331;
				
				
				t = texture2DRect(tex, b + vec2(-2, 0));
				t += texture2DRect(tex, b + vec2(2, 0));
				t += texture2DRect(tex, b + vec2(0, -2));
				t += texture2DRect(tex, b + vec2(0, 2));
				gl_FragColor += t  * 40.61076;
				
				t = texture2DRect(tex, b + vec2(-1, -1));
				t += texture2DRect(tex, b + vec2(-1, 1));
				t += texture2DRect(tex, b + vec2(1, -1));
				t += texture2DRect(tex, b + vec2(1, 1));
				gl_FragColor += t  * 45.38329;
				
				
				t = texture2DRect(tex, b + vec2(-1, 0));
				t += texture2DRect(tex, b + vec2(1, 0));
				t += texture2DRect(tex, b + vec2(0, -1));
				t += texture2DRect(tex, b + vec2(0, 1));
				gl_FragColor += t  * 47.9759444;
				
				gl_FragColor /= 1024.0;
				
			}
		"""
		
		return s
		
	def getHsv2RgbCode(self):
		s = """
			#extension GL_ARB_texture_rectangle : enable
			uniform sampler2DRect view1, bckView;

			uniform float hmn;
			uniform float hmx;
			uniform float mn;
			uniform float mx;
			uniform float hcutoff;
			
			vec3 h2r(float h, float s, float v) {
				return mix(vec3(1.),clamp((abs(fract(h+vec3(3.,2.,1.)/3.)*6.-3.)-1.),0.,1.),s)*v;
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
				
				c.r = (1.0-hcutoff) * (1.0 - c.r); //select a certain range for hue
				
				gl_FragColor = vec4(h2r(c.r, c.g, c.b), 1.0);
				
			}
		"""
		
		return s
		
	def getFluorescenceProcessCode(self):
		s = """
			#extension GL_ARB_texture_rectangle : enable
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
						v1 -= r;
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
			#extension GL_ARB_texture_rectangle : enable
			uniform sampler2DRect f1;
			uniform float mapMn;
			uniform float mapMx;

			void main() {
				float v1 = texture2DRect(f1, gl_TexCoord[0].st).r;
				v1 -= mapMn;
				v1 /= (mapMx - mapMn);
				
				v1 = clamp(v1, 0.0, 0.9); // 0.9 to exclude "redder" colors
				
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
	
