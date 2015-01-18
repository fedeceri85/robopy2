import tables as tb
import numpy as np
import xml.etree.ElementTree as xet
import os
import shutil
class Raw2HDF5:
    def __init__(self):
        self.hdf5Handler = None
        self.timesLabel = 's'
        self.frameData = None
        self.width = 0
        self.height = 0
        self.nFrames = 0
        self.pixelSize = 0.0
        self.channels = [0,0,0,0]
        self.nchannels = 0
    def open(self, seqName):
        fi = tb.open_file(seqName)
        self.hdf5Handler = fi.root.x
        self.timesArray = fi.root.times.timesArray.read()
        self.timesLabel = unicode(fi.root.times.timeLabel.read().tostring(),'utf-8')

    def getRawImage(self,n):
        return self.hdf5Handler[:,:,n]
        
    def saveSequence(self, fileName, frames, times = None, filterLevel = 5):
        if frames is None:
            return
        if fileName is None:
            return
            
        h,w,nFrames = frames.shape
        
        h5file = tb.openFile(fileName, mode='w')
        root = h5file.root
        atom = tb.UInt16Atom() #tb.Atom.from_dtype(data.dtype)
        if filterLevel == 0:
            filters = None
        else:
            filters = tb.Filters(complevel=filterLevel, complib='zlib',shuffle=True)
            
        x = h5file.createEArray(root,'x', atom, shape=(h, w, 0), expectedrows=nFrames, filters = filters)
        for i in range(nFrames):
            data = frames[:,:,i]
            try:
                x.append(data)
            except ValueError:
                print("Can't add frame "+str(i)+". Wrong dimensions?")
                
        if times != None:
            tGroup = h5file.createGroup(root,'times')
            tA = np.vstack((range(1,nFrames+1), times)).T
            _t = h5file.createCArray(tGroup,'timesArray',tb.Atom.from_dtype(tA.dtype),tA.shape,filters=filters)
            _t[:] = tA
            bytes = np.fromstring(self.timesLabel.encode('utf-8'),np.uint8)
            _tStr = h5file.createCArray(tGroup,'timeLabel',tb.UInt8Atom(),shape=(len(bytes), ),filters=filters)
            _tStr[:] = bytes
            
        h5file.flush()
        h5file.close()
        
    def fromThorlabsXMLInfo(self, infoFile):
        try:
            tree = xet.parse(infoFile)
        except ValueError:
            print("Could not parse xml info file!")
            return
            
        root = tree.getroot()
        cam = root.find("Camera")
        
        if cam is None:
            return
        
        ks = cam.keys()
        if "pixelSizeUM" in ks:
            self.pixelSize = float(cam.attrib["pixelSizeUM"])
        else:
            self.pixelSize= 0
            
        lsm = root.find("LSM")
        ks = lsm.keys()
        if "pixelX" in ks:
            self.width = int(lsm.attrib["pixelX"])
        else:
            self.width = 0
            
        if "pixelY" in ks:
            self.height = int(lsm.attrib["pixelY"])
        else:
            self.height = 0
            
        pmt = root.find("PMT")
        ks = pmt.keys()
        for i,key in enumerate(["enableA","enableB","enableC","enableD"]):
		if key in ks:
			self.channels[i] = int(pmt.attrib[key])
		else:
			self.channels[i] = 0
	
        self.nchannels = sum(self.channels)
        
        stream = tree.find("Streaming")
        if stream is None:
            print("No Stream section found in info!")
        else:
            ks = stream.keys()
            if "frames" in ks:
                self.nFrames = int(stream.attrib["frames"])
            else:
                self.nFrames = 0
                
    def convertThorlabsRawToH5(self, infoFile, dataFile, timeFile, outH5File, filterLevel=5,outChannel=0):
        self.fromThorlabsXMLInfo(infoFile)
        
        if self.width == 0 or self.height == 0 or self.nFrames < 1:
                return
        
        frameSize = np.uint64(self.width * self.height * 2)
        totalSize = frameSize  * np.uint64(self.nFrames)*self.nchannels
        chunkSize = np.uint64(1024 * 1024* 128) #500 mb
        chunkFrames = np.uint64(chunkSize / frameSize/self.nchannels)   
        if self.nchannels !=1:
		chunkFrames = np.uint64(1)
        chunkSize = chunkFrames * frameSize
        
        f = open(dataFile, "rb")
        if f is None:
           print("Cannot open data file!")
           return
            
        #check if calculated frames correspond to raw file data size
        f.seek(0, 2)
        fileSize = f.tell()
        f.seek(0)

        if totalSize != fileSize:
            print("Calculated data size differs " + str(totalSize) + " from file size " + str(fileSize) + "!")
            if self.nchannels != 0:
		self.nFrames = np.uint64(fileSize/frameSize/self.nchannels)
		print("New number of frames: " + str(self.nFrames))
		totalSize =  frameSize  * np.uint64(self.nFrames)*self.nchannels
            else:
		print("Nothing to do")
		f.close()
		return
                
        h5file = tb.openFile(outH5File, mode='w')
        root = h5file.root
        atom = tb.UInt16Atom() #tb.Atom.from_dtype(data.dtype)
        if filterLevel == 0:
            filters = None
        else:
            filters = tb.Filters(complevel=filterLevel, complib='blosc',shuffle=True)
            
        x = h5file.createEArray(root,'x', atom, shape=(self.height, self.width, 0), expectedrows=self.nFrames, filters = filters)

        readBytes = 0L   
        processedFrames = np.uint64(0)
        
        t = np.loadtxt(timeFile)
        dt = np.diff(t).mean()
        times = np.arange(self.nFrames)*dt
        self.addTimestoH5(h5file,times,filters)
	if self.nchannels !=1:
		f.seek(outChannel*frameSize)
		
        while readBytes < fileSize:
            readBytes += chunkSize * self.nchannels
            if readBytes > fileSize:
                chunkSize = fileSize - (readBytes - chunkSize)#readBytes - fileSize - 1 
                chunkFrames = np.uint64(chunkSize / frameSize)
                chunkSize = chunkFrames*frameSize
                print chunkSize
                print chunkFrames
            rawData = f.read(chunkSize)
            #print("Chunk frames " + str(chunkFrames) + " and chunkSize " + str(chunkSize))
            rawData = np.fromstring(rawData, np.uint16)
            rawData = rawData.reshape((chunkFrames, self.height, self.width,1))
        
            for i in range(chunkFrames):
                data = rawData[i,:,:,:]#.reshape((rawData.shape[1], rawData.shape[2], 1))
                try:
                    x.append(data)
                except ValueError:
                    print("Can't add frame "+str(i)+". Wrong dimensions?") 
            processedFrames += chunkFrames        
          #  print("Frames " + str(processedFrames) + "/" + str(self.nFrames))
            
            f.seek((self.nchannels-1)*frameSize,1)
        
        f.close()
        
      
        h5file.flush()
        h5file.close()
        
        
    def addTimestoH5(self,h5file,times,filters):
	root = h5file.root
	tGroup = h5file.createGroup(root,'times')
	nFrames = times.size
	tA = np.vstack((np.arange(0,nFrames), times)).T
	_t = h5file.createCArray(tGroup,'timesArray',tb.Atom.from_dtype(tA.dtype),tA.shape,filters=filters)
	_t[:] = tA
	bytes = np.fromstring(self.timesLabel.encode('utf-8'),np.uint8)
	_tStr = h5file.createCArray(tGroup,'timeLabel',tb.UInt8Atom(),shape=(len(bytes), ),filters=filters)
	_tStr[:] = bytes

def BatchConvertFilesHDF5(src,dest,channels=[]):
	src = os.path.abspath(src)
	dest = os.path.abspath(dest)

	if src[-1] == os.sep:
		src = src[:-1]
	if dest[-1] == os.sep:
		dest = dest[:-1]


	raws,nonraws = selectFiles(src,'raw')
	roimasks =  [raw for raw in raws if os.path.split(raw)[1]=='ROIMask.raw']

	raws = [raw for raw in raws if os.path.split(raw)[1]!='ROIMask.raw']
	nonraws.extend(roimasks)
	
	for rmask in nonraws:
		fname = rmask[len(src)+1:]
		outfname = os.path.join(dest,fname)
		if not os.path.isfile(outfname):
			
			saveDir = os.path.split(outfname)[0]
			try:
				os.makedirs(saveDir)
			except OSError:
				print('Directory already exists')

			shutil.copy(rmask,outfname+'_tmp')
			shutil.move(outfname+'_tmp',outfname)
			os.utime(outfname,(os.path.getatime(rmask),os.path.getmtime(rmask)))
		
	
	for raw in raws:
		
		fold = os.path.split(raw)[0]
		xml = os.path.join(fold,'Experiment.xml')
		tFile = os.path.join(fold,'timing.txt')
		h = Raw2HDF5()
		h.fromThorlabsXMLInfo(xml)
		print("converting "+raw)
		fname = raw[len(src)+1:]
		outraw = os.path.join(dest,fname)
		saveDir = os.path.split(outraw)[0]
		try:
			os.makedirs(saveDir)
		except OSError:
			print('Directory already exists')
		
		if not os.path.isfile(outraw):
		
			if h.nchannels == 1:
				try:
					out = os.path.splitext(outraw)[0]+'blosc.h5'
					h.convertThorlabsRawToH5(xml,raw, tFile, out+'_tmp', filterLevel=5)
					shutil.move(out+'_tmp',out)
					os.utime(out,(os.path.getatime(raw),os.path.getmtime(raw)))
		
				except:
					print("Error in converting file "+raw)
			else:
				for channel in channels:
					try:
						out = os.path.splitext(outraw)[0]+'blosc_Channel'+str(channel)+'.h5'
						h.convertThorlabsRawToH5(xml,raw, tFile, out+'_tmp', filterLevel=5,outChannel=channel)
						shutil.move(out+'_tmp',out)
						os.utime(out,(os.path.getatime(raw),os.path.getmtime(raw)))
					except:
						print("Error in converting file "+raw)
		else:
			print("file already exists: "+outraw)
			
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

if __name__ == '__main__':
	f  = 'file:///run/media/federico/SAMSUNG/20150109-bl6p5/6topo1/1-apical005/Image_0001_0001.raw'[7:]
	out = '/home/federico/Desktop/Image_0001_00012_chand_blosc7.h5'
	xml = 'file:///run/media/federico/SAMSUNG/20150109-bl6p5/6topo1/1-apical005/Experiment.xml'[7:]
	tFile = 'file:///run/media/federico/SAMSUNG/20150109-bl6p5/6topo1/1-apical005/timing.txt'[7:]
	h = Raw2HDF5()
	h.convertThorlabsRawToH5(xml, f, tFile, out, filterLevel=7,outChannel=2)