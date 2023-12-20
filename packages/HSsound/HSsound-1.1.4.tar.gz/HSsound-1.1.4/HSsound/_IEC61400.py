import pyees as pe
import matplotlib.pyplot as plt
import numpy as np


class IEC61400:
    def __init__(self) -> None:
        self.data = None
        
    def calculate(self):


        # make sure the data is in the correct units
        self.data.F.convert('Hz')
        self.data.L.convert('dB')

        ## plot the data
        fig, ax = plt.subplots()
        f = pe.dummy_fit(self.data.F, self.data.L)
        f.plotData(ax, color = 'blue')


        ## find local maxima
        indexes = []
        for i in range(1, len(self.data.L) - 1):
            if (self.data.L[i-1] < self.data.L[i] > self.data.L[i+1]):
                indexes.append(i)

        ## determine if the local maxima are possible tones
        isPossibleTone = [False] * len(indexes)
        for i, index in enumerate(indexes):

            f = self.data.F[index].value
            criticalBandWidth = 25 + 75 * (1 + 1.4 * (f / 1000)**2)**0.69
            fLow = f - criticalBandWidth / 2
            fHigh = f + criticalBandWidth / 2
            
            bandIndecies = [i for i, freq in enumerate(self.data.F.value) if (freq > fLow) and (freq < fHigh) and i not in [index, index+1, index-1]]
            if not bandIndecies: continue
            
            averageEnergy = 10 * np.log10(np.mean(10**(self.data.L.value[bandIndecies] / 10)))
            
            if self.data.L[index] > averageEnergy + pe.variable(6, 'dB'):
                isPossibleTone[i] = True

        ## plot the possible tones
        possibleTonesIndexes = [i for i, isPossible in zip(indexes, isPossibleTone) if isPossible]


        ## determine if the possible tones are actual tones
        identifiedTonesIndex = []
        identifiedTones = []
        toneSoundPressureLevels = []
        maskingSoundPressureLevels = []

        for index in possibleTonesIndexes:
            
            f = self.data.F[index].value
            
            if (20 < f < 70):
                fLow = 20
                fHigh = 120
            else:
                criticalBandWidth = 25 + 75 * (1 + 1.4 * (f / 1000)**2)**0.69
                fLow = f - criticalBandWidth / 2
                fHigh = f + criticalBandWidth / 2
            
            bandIndecies = [i for i, freq in enumerate(self.data.F.value) if (freq > fLow) and (freq < fHigh)]
            LBand = self.data.L.value[bandIndecies]
            
            L70 = np.sort(LBand)
            n70 = int(np.ceil(len(L70) * 0.7))
            L70 = L70[0:n70]
            L70 = 10 * np.log10(np.mean(10**(L70 / 10)))
            criterion = L70 + 6

            maskingIndexes = [i for i, L in zip(bandIndecies, LBand) if L < criterion]
            
            Lpn = self.data.L.value[maskingIndexes]
            Lpn = 10 * np.log10(np.mean(10**(Lpn / 10)))
            criterion = Lpn + 6
            
            ## find all indexes that are above the criterion line
            isTone = [i for i, L in zip(bandIndecies, LBand) if L > criterion]

            ## group the indexes in lists of consequtive indexes
            groups = []
            start = 0
            stop = 0
            for i in range(len(isTone)):
                stop = i+1
                if i == len(isTone)-1:
                    groups.append(isTone[start:stop])
                    break
                if isTone[i+1] != isTone[i] + 1:
                    groups.append(isTone[start:stop])
                    start = i+1
            
            
            ## only keep the elements in the list that are less than 10 dB lower than then maximum element
            for i, group in enumerate(groups):
                L = self.data.L.value[group]
                Lmax = np.max(L)
                group = [ii for ii, l in zip(group, L) if l > Lmax - 10]
                groups[i] = group
            
            ## collapse the groups
            tonesIndex = [elem for group in groups for elem in group]
            
            ## identify the tone as the frequency with the largest sound pressure
            L = self.data.L.value[tonesIndex]
            index = int(np.argmax(L))
            f = self.data.F[tonesIndex[index]]
            if f in identifiedTones:
                continue
            identifiedTonesIndex.append(tonesIndex[index])    
            identifiedTones.append(f)
            
            
            # determine the sound pressure level over the tone
            L = self.data.L[tonesIndex]
            L.convert('1')
            Lpt = sum(L)
            Lpt.convert('dB')
            L.convert('dB')
            for i in range(len(tonesIndex)-1):
                if tonesIndex[i+1] == tonesIndex[i] + 1:
                    Lpt /= 1.5
                    break
            toneSoundPressureLevels.append(Lpt)

            ## determine the masking noise level
            L = self.data.L[maskingIndexes]
            L.convert('1')
            Lpn_avg = sum(L)
            Lpn_avg.convert('dB')
            L.convert('dB')
            effectiveBandWidth = 1.5 * (np.max(self.data.F.value) - np.min(self.data.F.value)) / (len(self.data.F.value) - 1)
            correctionTerm = pe.variable(criticalBandWidth / effectiveBandWidth)
            correctionTerm.convert('dB')
            Lpn = Lpn_avg + correctionTerm
            maskingSoundPressureLevels.append(Lpn)


        identifiedTones = pe.variable(identifiedTones)
        toneSoundPressureLevels = pe.variable(toneSoundPressureLevels)
        maskingSoundPressureLevels = pe.variable(maskingSoundPressureLevels)
        tonality = toneSoundPressureLevels - maskingSoundPressureLevels
        audibleTonality = tonality - ( -2-np.log10(1 + (identifiedTones.value / 502)**2.5))
        isAudible = [True if DeltaL > 0 else False for DeltaL in audibleTonality ]


        print(identifiedTones)
        print(toneSoundPressureLevels)
        print(maskingSoundPressureLevels)
        print(tonality)    
        print(audibleTonality)
        print(isAudible)


        f_possibleTones = pe.dummy_fit(self.data.F[possibleTonesIndexes], self.data.L[possibleTonesIndexes])
        f_possibleTones.scatter(ax, color = 'red', label = 'Possible tones')
        f_tones = pe.dummy_fit(self.data.F[identifiedTonesIndex], self.data.L[identifiedTonesIndex])
        f_tones.scatter(ax, color = 'green', label = 'Identified tones')

        if any(isAudible):
            indexes = [i for i, elem in enumerate(isAudible) if elem]
            indexes = [identifiedTonesIndex[elem] for elem in indexes]
            f_audible = pe.dummy_fit(self.data.F[indexes], self.data.L[indexes])
            f_audible.scatter(ax, color = 'black', label = 'Audible tones')



        ax.set_xlabel('Frequency [Hz]')
        ax.set_ylabel('Sound pressure level [dB]')
        ax.legend()
        fig.tight_layout()
        plt.show() 
            
            
