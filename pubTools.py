from pylab import *
from matplotlib.figure import Figure

inchestocm=2.54
micro=u'\u03bc'
delta=u'\u0394'
labelsize=8
fontFamily='Arial'
def oneColumnFigure(figsize=(3.5,2.5),dpi=200,addAxes=True):
	rcParams['lines.linewidth']=1
	rcParams['font.size']=7
	rcParams['figure.subplot.left']=0.15
	rcParams['figure.subplot.right']=0.97
	rcParams['figure.subplot.bottom']=0.15
	rcParams['figure.subplot.top']=0.90

	rcParams['xtick.labelsize']='small'
	rcParams['ytick.labelsize']='small'
	#rcParams['axes.labelsize']='small'
	rcParams['legend.fontsize']='medium'
	rcParams['font.sans-serif']=fontFamily
	rcParams['svg.fonttype'] = 'none'
	#rcParams['ytick.direction']='out'    
	#rcParams['xtick.direction']='out'  
	rcParams['mathtext.default']  = 'regular'
	#rcParams['axes.linewidth']=2
	#rcParams['xtick.major.size']=3
	#rcParams['ytick.major.size']=3
	#rcParams['xtick.minor.size']=2
	#rcParams['ytick.minor.size']=2
	#rc('lines', linewidth=1.5) 
	fig=Figure(figsize=figsize,dpi=dpi)
	if addAxes:
		ax=fig.add_subplot(111)
		ax.xaxis.set_ticks_position('bottom')
		ax.yaxis.set_ticks_position('left')
		return (fig,ax)
	return fig
	#for loc, spine in ax.spines.iteritems():
		#if loc in ['left','bottom']:
			#spine.set_position(('outward',0)) # outward by 10 points
		#elif loc in ['right','top']:
			#spine.set_color('none') # don't draw spine
		#else:
			#raise ValueError('unknown spine location: %s'%loc)
			
	

