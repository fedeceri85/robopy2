import sys
sys.path.append('/home/federico/pythonModules/robopy')
import TiffSequence as tf
import shutil
import os
import fnmatch

topFolder = '.'
destFolder = 'crop'

def selectFiles(topDir,extension):
	out = []
	out2 = []
	for root, dirs, files in os.walk(topDir):     
		for file in files:
			if file.endswith(extension):
					out.append(os.path.join(root, file))
			else:
					out2.append(os.path.join(root,file))
	return out,out2



def listTiffFiles(src,names):
	out = []
	for name in names:
		if name.endswith('.tif'):
			out.append(name)

	return out

def anyFile(src,names):
	out = []
	for name in names:
		if os.path.isfile(name):
			out.append(name)
	return out

def BatchCropFiles(src,dest,x,y,originalSize=None):

	src = os.path.abspath(src)
	dest = os.path.abspath(dest)

	if src[-1] == os.sep:
		src = src[:-1]
	if dest[-1] == os.sep:
		dest = dest[:-1]

	if os.path.isdir(dest):
		filesLeft = [os.path.join(dp[len(src):], f) for dp, dn, fn in os.walk(os.path.expanduser(src)) for f in fn]
		filesRight = [os.path.join(dp[len(dest):], f) for dp, dn, fn in os.walk(os.path.expanduser(dest)) for f in fn]
		set1 = set(filesLeft)
		set2 = set(filesRight)
		difference = list(set1.difference(set2))
		tiffs = []
		nontiffs = []
		for f in difference:
			if f.endswith('.tif'):
				if f.startswith('/'):
					f = f[1:]
				tiffs.append(os.path.join(src,f))
			else:
				if f.startswith('/'):
					f = f[1:]
				nontiffs.append(os.path.join(src,f))

		for f in nontiffs:
			saveFileName = f[len(src)+1:]
			savePath = os.path.join(dest,saveFileName)
			saveDir = os.path.split(savePath)[0]
			try:
				os.makedirs(saveDir)
			except OSError:
				print('Directory already exists')
				

			shutil.copy(f,savePath+'_tmp')
			shutil.move(savePath+'_tmp',savePath)

	else:
		print('Copying non-tiff files')
		try: 
			shutil.copytree(src,dest,ignore=listTiffFiles)
		except OSError:
			dest = dest+'_2'

			shutil.copytree(src,dest,ignore=listTiffFiles)

		tiffs,nontiffs = selectFiles(src,'tif')
	options={}
	options['crop'] = True
	options['rightMargin'] = x[1]
	options['leftMargin']  = x[0]
	options['bottomMargin'] = y[1]
	options['topMargin'] = y[0]
	options['rebin'] = None
	options['LineCorrection'] = False
	totalFrames = 0
	for f in tiffs:
		print(f)
		saveFileName = f[len(src)+1:]
		saveDir = os.path.join(dest,saveFileName)
		try:
			if originalSize is None:
				newTiff = tf.TiffSequence([f,],options)
				newTiff.saveSequence(saveDir)
				os.utime(saveDir,(os.path.getatime(f),os.path.getmtime(f)))
				totalFrames = totalFrames + newTiff.frames
			else:
				oldTiff = tf.TiffSequence([f,],None)
				if originalSize[0] != oldTiff.width or originalSize[1] != oldTiff.height:
					print('Unespected picture size, copying ... ')
					shutil.copyfile(f,saveDir+'_tmp')
					shutil.move(saveDir+'_tmp',saveDir)
				
					os.utime(saveDir,(os.path.getatime(f),os.path.getmtime(f)))

				else:
					newTiff = tf.TiffSequence([f,],options)
					newTiff.saveSequence(saveDir+'_tmp')
					shutil.move(saveDir+'_tmp',saveDir)

					os.utime(saveDir,(os.path.getatime(f),os.path.getmtime(f)))				
					totalFrames = totalFrames + newTiff.frames
		except:
			print("Cannot open file, copying")
			shutil.copyfile(f,saveDir+'_tmp')
			shutil.move(saveDir+'_tmp',saveDir)
	print('Cropped '+str(totalFrames)+' frames')



def BatchConvertFilesHDF5(src,dest,x=None,y=None,originalSize=None):
	src = os.path.abspath(src)
	dest = os.path.abspath(dest)

	if src[-1] == os.sep:
		src = src[:-1]
	if dest[-1] == os.sep:
		dest = dest[:-1]


	tiffs,nontiffs = selectFiles(src,'tif')

	for f in nontiffs:
		if f.endswith('times.txt'):
			saveFileName = f[len(src)+1:]
			saveFilename1 = os.path.split(saveFileName)
			savePath = os.path.join(dest,saveFilename1[0],'times',saveFilename1[1])
			saveDir = os.path.split(savePath)[0]
			if not os.path.isfile(savePath):
				try:
					os.makedirs(saveDir)
				except OSError:
					print('Directory already exists')

				shutil.copy(f,savePath+'_tmp')
				shutil.move(savePath+'_tmp',savePath)
				os.utime(savePath,(os.path.getatime(f),os.path.getmtime(f)))

		else:
			saveFileName = f[len(src)+1:]
			savePath = os.path.join(dest,saveFileName)
			saveDir = os.path.split(savePath)[0]
			
			if not os.path.isfile(savePath):
				try:
					os.makedirs(saveDir)
				except OSError:
					print('Directory already exists')

				shutil.copy(f,savePath+'_tmp')
				shutil.move(savePath+'_tmp',savePath)
				os.utime(savePath,(os.path.getatime(f),os.path.getmtime(f)))


	if x == None or y == None:
		options = None
	else:
		options={}
		options['crop'] = True
		options['rightMargin'] = x[1]
		options['leftMargin']  = x[0]
		options['bottomMargin'] = y[1]
		options['topMargin'] = y[0]
		options['rebin'] = None
		options['LineCorrection'] = False
	totalFrames = 0

	singleExperiments = []
	for tiff in tiffs:
		if tiff.endswith('part00.tif'):
			experiment = []
			pattern = tiff[:-6]+'*'+'.tif'
			for x in tiffs:

				if fnmatch.fnmatch(x,pattern):
					experiment.append(x)
			experiment.sort()

			singleExperiments.append(experiment)


	for tiff in tiffs:
		if not tiff[-10:-6]=='part':#tiff.rfind('part'):
			print("Warning, tiff not part of an experiment:")
			print(tiff)
			singleExperiments.append(tiff)
			
	filelist= []
	for nontiff in nontiffs:

		if not (nontiff.endswith('times.txt') or nontiff.endswith('.directory')):
			filelist.append(nontiff)

	if filelist!= []:
		print("Warning, non-tiff files not included:")
		print(filelist)

	for f in singleExperiments:
		print(f)
		saveFileName = f[0][len(src)+1:-3]+'h5'
		saveDir = os.path.join(dest,saveFileName)
		saveDir2 = os.path.split(saveDir)[0]
		saveDir_temp = saveDir+'_tmp'

		if not os.path.isdir(saveDir2):
			os.makedirs(saveDir2)
		
		if not os.path.isfile(saveDir):
			try:

				if originalSize is None:
					oldTiff = tf.TiffSequence(f,options)
					hdf = tf.HDF5Sequence(None)
					hdf.saveSequence(saveDir_temp,oldTiff)
					shutil.move(saveDir_temp,saveDir)
					os.utime(saveDir,(os.path.getatime(f[0]),os.path.getmtime(f[0])))
					totalFrames = totalFrames + oldTiff.frames
				else:
					oldTiff = tf.TiffSequence(f,None)
					if originalSize[0] != oldTiff.width or originalSize[1] != oldTiff.height:
						print('Unespected picture size, copying without cropping ... ')
						hdf = tf.HDF5Sequence(None)
						hdf.saveSequence(saveDir_temp,oldTiff)
						shutil.move(saveDir_temp,saveDir)
						os.utime(saveDir,(os.path.getatime(f[0]),os.path.getmtime(f[0])))
						totalFrames = totalFrames + oldTiff.frames
						
						os.utime(saveDir,(os.path.getatime(f[0]),os.path.getmtime(f[0])))

					else:
						oldTiff = tf.TiffSequence(f,options)
						hdf = tf.HDF5Sequence(None)
						hdf.saveSequence(saveDir_temp,oldTiff)
						shutil.move(saveDir_temp,saveDir)
						os.utime(saveDir,(os.path.getatime(f[0]),os.path.getmtime(f[0])))				
						totalFrames = totalFrames + oldTiff.frames
			except:
					print("Some errors occured, copying original file")

					for f2 in f:
						saveFileName2 = f2[len(src)+1:]
						saveDir_orig = os.path.join(dest,saveFileName2)
						shutil.copyfile(f2,saveDir_orig+'_tmp')
						shutil.move(saveDir_orig+'_tmp',saveDir_orig)
						os.utime(saveDir_orig,(os.path.getatime(f2),os.path.getmtime(f2)))				

	print('Converted '+str(totalFrames)+' frames')

	
	
def copyFilesfromList(fileList,src,dest):
	src = os.path.abspath(src)
	dest = os.path.abspath(dest)

	if src[-1] == os.sep:
		src = src[:-1]
	if dest[-1] == os.sep:
		dest = dest[:-1]
		
	
	for f in fileList:
		saveFileName = f[len(src)+1:]
		saveDir = os.path.join(dest,saveFileName)
		saveDir2 = os.path.split(saveDir)[0]
		
		if not os.path.isdir(saveDir2):
			os.makedirs(saveDir2)
		if not os.path.isfile(saveDir):
			shutil.copy(f,saveDir+'_tmp')
			shutil.move(saveDir+'_tmp',saveDir)
