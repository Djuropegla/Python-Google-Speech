import wave
obj = wave.open("basic.wav", "rb")

#.wav parameters

# print("Number of channels ", obj.getnchannels())
# print("Sample width ", obj.getsampwidth())
# print("Frame rate ", obj.getframerate())
# print("Number of frames ", obj.getnframes())
# print("parameters ", obj.getparams())

# Some calculations conserning parameters 

timeAudio = obj.getnframes() / obj.getframerate()
print(timeAudio)

# data about frames

frames = obj.readframes(-1)
print(type(frames), type(frames[0]))
print(len(frames))
obj.close()

# Using functions above as setters we make a copy of basic.wav

objNew = wave.open("basic_new.wav", "wb")
objNew.setnchannels(1)
objNew.setsampwidth(2)
objNew.setframerate(16000.0)
objNew.writeframes(frames)
objNew.close()