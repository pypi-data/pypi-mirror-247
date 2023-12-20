import pyees as pe
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class _ISO3744parallelPipedSurfaceWithTwoReflectingPlaneUsingRectangularSegments: 
    
    def __init__(self):
        self._l1 = None
        self._l2 = None
        self._l3 = None
        self._d = None
        
        self.nSubdivisions = 0
        self.data = None
        self.backgroundData = None
        self._microphonePositions = None
        self._surface = None
        self._segments = None
        self._k1 = None
        self.k2 = pe.variable(0, 'dB')
        self._soundPressureLevel = None
        self._correctedSoundPressureLevel = None
        self._soundPowerLevel = None
        
        self.positionalUncertanty = pe.variable(0, 'cm')
        self.soundPressureUncertanty = pe.variable(0, 'dB')
        self.uncertantyOfOperation = pe.variable(0, 'dB')
         
    @property
    def k1(self):
        return self._k1

    @property
    def soundPressureLevel(self):
        return self._soundPressureLevel
    
    @property
    def correctedSoundPressureLevel(self):
        return self._correctedSoundPressureLevel
    
    @property
    def soundPowerLevel(self):
        return self._soundPowerLevel
    
    @property
    def microphonePositions(self):
        return self._microphonePositions

    @property
    def d(self):
        return self._d
    
    @d.setter
    def d(self, d):
        """
        d (variable): the measurement distance, which has to be at least 0.25 [m], but preferably 1 m or more.
        """
        self._d = d
   
    @property
    def l1(self):
        return self._l1
    
    @l1.setter
    def l1(self, l1):
        """
        l1 (variable): the length of the reference box from the wall to the front face.
        """
        self._l1 = l1
        
    @property
    def l2(self):
        return self._l2
    
    @l2.setter
    def l2(self, l2):
        """
        l2 (variable): the width of the reference box.
        """
        self._l2 = l2
    
    @property
    def l3(self):
        return self._l3
    
    @l3.setter
    def l3(self, l3):
        """
        l3 (variable): the height of the reference box.
        """
        self._l3 = l3

    def _calculateBackGroundCorrection(self):
        
        self.soundPressureUncertanty.convert(self.data.LAeq.unit)
        self.data.LAeq = pe.variable(self.data.LAeq.value, self.data.LAeq.unit, [self.soundPressureUncertanty.value] * len(self.data.LAeq))
        
        self.soundPressureUncertanty.convert(self.backgroundData.LAeq.unit)
        self.backgroundData.LAeq = pe.variable(self.backgroundData.LAeq.value, self.backgroundData.LAeq.unit, [self.soundPressureUncertanty.value] * len(self.backgroundData.LAeq))
        
        # determine the total equavilent A-weighted noise level as the logarithmic mean of the measurements
        meanSoundPressureLevel_backgound = pe.logarithmic.mean(self.backgroundData.LAeq)
        self._soundPressureLevel = pe.logarithmic.mean(self.data.LAeq)

        # determine the korrektion faktor for the backgound noise
        meanSoundPressureLevelDifference = self.soundPressureLevel - \
            meanSoundPressureLevel_backgound
        if (meanSoundPressureLevelDifference > pe.variable(15, 'dB')):
            k1 = pe.variable(0, 'dB')
        elif (pe.variable(6, 'dB') <= meanSoundPressureLevelDifference <= pe.variable(15, 'dB')):
            k1 = pe.variable(- 10 * np.log10(1 - 10 **
                                            (-0.1 * meanSoundPressureLevelDifference.value)), 'dB')
        else:
            # DeltaLp < 6 dB
            raise ValueError(f'The difference between the mena sound pressure level of the test specifimen and the mean sound pressure level of the backgound noise is {meanSoundPressureLevelDifference}. This is below the minimum allowed value of 6 dB')

        self._k1 = k1

    def _checkInputs(self):
          
        if self.data is None:
            raise ValueError('You have to supply a data file')
        
        if not hasattr(self.data, 'LAeq'):
            raise ValueError('The data has to include a parameter with the name LAeq')
        
        if not (self.data.LAeq.unit == 'dB'):
            raise ValueError('The parameter LAeq of the data has to have the unit "dB"')
        
        if not hasattr(self.data, 'x'):
            raise ValueError('The data has to include background a parameter with the name "x"')
               
        if not hasattr(self.data, 'y'):
            raise ValueError('The data has to include background a parameter with the name "y"')        
        
        if not hasattr(self.data, 'z'):
            raise ValueError('The data has to include background a parameter with the name "z"')
        
        if self.backgroundData is None:
            raise ValueError('You have to supply a background data file')
           
        if not hasattr(self.backgroundData, 'LAeq'):
            raise ValueError('The background data has to include a parameter with the name LAeq')

        if not (self.backgroundData.LAeq.unit == 'dB'):
            raise ValueError('The parameter LAeq of the background data has to have the unit "dB"')
        
        if not hasattr(self.backgroundData, 'x'):
            raise ValueError('The background data has to include a parameter with the name "x"')
               
        if not hasattr(self.backgroundData, 'y'):
            raise ValueError('The background data has to include a parameter with the name "y"')        
        
        if not hasattr(self.backgroundData, 'z'):
            raise ValueError('The background data has to include a parameter with the name "z"')
        
        if self.k2 > pe.variable(4, 'dB'):
            raise ValueError('The environment correction factor, k2, has to be less than 4 dB')

    
    
        
        if self.l1 is None:
            raise ValueError('You have to supply the variable "l1"')
        
        if self.l2 is None:
            raise ValueError('You have to supply the variable "l2"')
        
        if self.l3 is None:
            raise ValueError('You have to supply the variable "l3"')
        
        if self.d is None:
            raise ValueError('You have to supply the variable "d"')
   
    def _calculateSurfaceArea(self):
        """
        2a = l1 + d
        a = 0.5*l1 + 0.5*d
        
        2b = l2 + 2*d 
        b = 0.5 * l2 + d
        
        c = l3 + d
        """

        self.a = 0.5 * self.l1 + 0.5 * self.d
        self.b = 0.5 * self.l2 + self.d
        self.c = self.l3 + self.d
        
        self.positionalUncertanty.convert(self.a.unit)
        self.a = pe.variable(self.a.value, self.a.unit, self.positionalUncertanty.value)

        self.positionalUncertanty.convert(self.b.unit)
        self.b = pe.variable(self.b.value, self.b.unit, self.positionalUncertanty.value)
        
        self.positionalUncertanty.convert(self.c.unit)
        self.c = pe.variable(self.c.value, self.c.unit, self.positionalUncertanty.value)
        
        self.surfaceArea = 2 * (2*self.a*self.b + self.b*self.c + 2*self.c*self.a)
    
    def _calculateLocations(self):
        
        o = pe.variable(0, 'm')
        r1 = pe.variable([o,            self.d,             o])
        r2 = pe.variable([self.l1,      self.d,             o])
        r3 = pe.variable([self.l1,      self.d+self.l2,     o])
        r4 = pe.variable([o,            self.d+self.l2,     o])
        r5 = pe.variable([o,            self.d,             self.l3])
        r6 = pe.variable([self.l1,      self.d,             self.l3])
        r7 = pe.variable([self.l1,      self.d+self.l2,     self.l3])
        r8 = pe.variable([o,            self.d+self.l2,     self.l3])
        
        self._referenceBox = [
            [r1, r2, r3, r4],
            [r1, r2, r6, r5],
            [r2, r3, r7, r6],
            [r3, r4, r8, r7],
            [r4, r1, r5, r8],
            [r5, r6, r7, r8]   
        ]
        
        p1 = pe.variable([o,            o,          o])
        p2 = pe.variable([2*self.a,     o,          o])
        p3 = pe.variable([2*self.a,     2*self.b,   o])
        p4 = pe.variable([o,            2*self.b,   o])
        p5 = pe.variable([o,            o,          self.c])
        p6 = pe.variable([2*self.a,     o,          self.c])
        p7 = pe.variable([2*self.a,     2*self.b,   self.c])
        p8 = pe.variable([o,            2*self.b,   self.c])

        self._vertices = [p1, p2, p3, p4, p5, p6, p7, p8]
        
        self._segments = [
            [p1, p2, p6, p5],
            [p2, p3, p6, p7],
            [p3, p4, p8, p7],
            [p5, p6, p7, p8]
        ]
        
        ## only corner pieces
        self._microphonePositions = [p6, p7]
        
        def getMicrophonePositionsFromSegments(segments, nSubdivisions):
            if nSubdivisions == -1:
                return
            
            for segment in segments:
                p1, p3, p7, p9 = segment
                
                p2 = (p1 + p3) / 2
                p4 = (p1 + p7) / 2
                p5 = (p1 + p3 + p7 + p9) / 4
                p6 = (p3 + p9) / 2
                p8 = (p7 + p9) / 2
                
                self._microphonePositions.append(p5)
                
                newSegments = [
                    [p1, p2, p5, p4],
                    [p2, p3, p6, p5],
                    [p4, p5, p8, p7],
                    [p5, p6, p9, p8]
                ]
                
                getMicrophonePositionsFromSegments(newSegments, nSubdivisions - 1)
                
        getMicrophonePositionsFromSegments(self._segments, self.nSubdivisions)    
        
    def plotMeasurementSetup(self, fig):
        ## plot the setup in 3d
        ax = fig.add_subplot(projection='3d')
        for i, vertex in enumerate(self._vertices):
            label = 'Vertices' if i == 0 else None
            ax.scatter(vertex[0].value, vertex[1].value, vertex[2].value, color = 'red', marker = 'o', label = label)
        
        for i, microphonePosition in enumerate(self._microphonePositions):
            label = 'Microphone Positions' if i == 0 else None
            ax.scatter(microphonePosition[0].value, microphonePosition[1].value, microphonePosition[2].value, color = 'green', marker = 'o', label = label)
        
        for i, referenceSurface in enumerate(self._referenceBox):
            label = 'Reference Box' if i == 0 else None
            
            subRerenceSufaces = [
                [referenceSurface[0], referenceSurface[1], referenceSurface[2]],
                [referenceSurface[2], referenceSurface[3], referenceSurface[0]]
            ]
            
            triangles = []
            for subRerenceSuface in subRerenceSufaces:
                newTriangle = []
                for vert in subRerenceSuface:
                    newTriangle.append([elem.value for elem in vert])
                triangles.append(newTriangle)
            
            ax.add_collection(Poly3DCollection(triangles, color = 'blue', label = label))


        ax.legend()
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_aspect('equal')
    
    def calculate(self):
        self._checkInputs()
        
        self._calculateSurfaceArea()
        self._calculateLocations()
        
        # determine the sound pressure level
        self._calculateBackGroundCorrection()
        self._checkData()   
        
        self._correctedSoundPressureLevel = self.soundPressureLevel - self.k1 - self.k2
        
        normalizedSurfaceArea = self.surfaceArea / pe.variable(1, 'm2')
        normalizedSurfaceArea.convert('dB')
        
        
        self._soundPowerLevel = self._correctedSoundPressureLevel + normalizedSurfaceArea   
        self.uncertantyOfOperation.convert('dB')
        operationScaling = pe.variable(0, 'dB', self.uncertantyOfOperation.value)
        self._soundPowerLevel += operationScaling
      
    def _checkData(self):
        
        ## determine the difference between the maximum and minimum sound pressure level the microphone positions
        ## More microphone positions are necessary if this difference is larger than the number of microphones used
        diff = np.max(self.data.LAeq) - np.min(self.data.LAeq)
        diff._uncert = 0
        if (diff > len(self.data.LAeq)):
            raise ValueError(f'The differnce between the maximum and minimum value of the sound pressure levels, {diff}, is more than the number of measurement points, {len(self.data.LAeq)}. The measurement cannot be used as more measurement points are necessary.')
            
        ## determine the difference between the maximum and minimum sound pressure level the microphone positions of the background data
        ## More microphone positions are necessary if this difference is larger than the number of microphones used
        diff = np.max(self.backgroundData.LAeq) - np.min(self.backgroundData.LAeq)
        diff._uncert = 0
        if (diff > len(self.backgroundData.LAeq)):
            raise ValueError(f'The differnce between the maximum and minimum value of the background sound pressure levels, {diff}, is more than the number of measurement points, {len(self.data.LAeq)}. The measurement cannot be used as more measurement points are necessary.')

        ## determine the apparent directivity index 
        # D = Lp_i - Lp
        # where Lp_i is the background corrected sound pressure level at the i'th microphone position,
        # and Lp is the mean (energy level) background corrected sound pressure level on the measurement surface
        meanSoundPressureLevel_data = pe.logarithmic.mean(self.data.LAeq)
        D = (self.data.LAeq - self.k1) - (meanSoundPressureLevel_data - self.k1)    
        if (any(D > pe.variable(5, 'dB'))):
            
            ## determine the number of positions where the apparant directivity index is greater than 5 dB
            nPositions = sum([1 for elem in D if elem > pe.variable(5, 'dB')])
            
            ## determine the difference between the data and the background data
            diff = self.data.LAeq - self.backgroundData.LAeq
            
            if (any(diff > pe.variable(6, 'dB'))):
                raise ValueError(f'The apparent A-weighted directivity exceeds 5 dB at {nPositions} microphone positions. However, the background data is within 6 dB at some of the microphone positions. Therefore, reducing the background noise is prioritized.')
            else:
                raise ValueError(f'The apparent A-weighted directivity exceeds 5 dB at {nPositions} microphone positions. More microhone positions are necessasry.')

        
        ## check the microphone positions used during the test
        for xi, yi, zi in zip(self.data.x, self.data.y, self.data.z):
            pos = pe.variable([xi,yi,zi])
            eq = [1 if all(pos == elem) else 0 for elem in self.microphonePositions]
            if sum(eq) == 0:
                raise ValueError(f'The position {pos} was not in the list of microphone positions')
    
        ## check the microphone positions used during the background data
        for xi, yi, zi in zip(self.backgroundData.x, self.backgroundData.y, self.backgroundData.z):
            pos = pe.variable([xi,yi,zi])
            eq = [1 if all(pos == elem) else 0 for elem in self.microphonePositions]
            if sum(eq) == 0:
                raise ValueError(f'The position {pos} was not in the list of microphone positions')
        
