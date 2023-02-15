import pyaudio
import wave
import time
import webbrowser

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)
print("Start recording")
seconds = 5
frames = []
t0 = time.time()
for i in range(0,int(RATE/FRAMES_PER_BUFFER*seconds)):
    data = stream.read(FRAMES_PER_BUFFER)
    frames.append(data)


stream.stop_stream()
stream.close()
p.terminate()

obj = wave.open("output.wav", "wb")
obj.setnchannels(CHANNELS)
obj.setsampwidth(p.get_sample_size(FORMAT))
obj.setframerate(RATE)
obj.writeframes(b"".join(frames))
obj.close()
import requests
from api_secrets import API_KEY

uploadEndpoint = 'https://api.assemblyai.com/v2/upload'
transcriptEndpoint = "https://api.assemblyai.com/v2/transcript"

#upload

filename = r"C:\Users\X-TREME\Desktop\faks\epos\Python-Google-Speech\output.wav"
def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

headers = {'authorization': API_KEY}
response = requests.post(uploadEndpoint,
                        headers=headers,
                        data=read_file(filename))

#print(response.json())
audioURL = response.json()['upload_url']
#transcribe

json = { "audio_url": audioURL }
response = requests.post(transcriptEndpoint, json=json, headers=headers)
#print(response.json())
transribeID = response.json()['id']
#poll

pollingEndpoint = transcriptEndpoint + '/' + transribeID
pollingResponse = requests.get(pollingEndpoint,headers=headers)
#print(pollingResponse.json())
while True:
    pollingResponse = requests.get(pollingEndpoint,headers=headers)
    if pollingResponse.json()['status'] == 'completed':
        print(time.time()-t0)
        data = pollingResponse.json()['text']
        print(data)
        if 'OPEN YOUTUBE.' in data.upper():
            webbrowser.open("https://www.youtube.com/")
        break
    elif pollingResponse.json()['status'] == 'error':
        print('It is what it is')

