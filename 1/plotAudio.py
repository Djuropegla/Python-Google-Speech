import wave
import matplotlib.pyplot as plt
import numpy as np
obj = wave.open("basic.wav", "rb")
sampleFreq = obj.getframerate()
numOfSamples = obj.getnframes()
signalWave = obj.readframes(-1)

obj.close()
tAudio = numOfSamples / sampleFreq
print(tAudio)

