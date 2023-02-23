import threading
import queue
from contextlib import closing

import pyaudio
from wave import open as wopen
from time import time
from requests import post, get

API_KEY = "e31c5941249641af840c3821fc3f36b0"
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

seconds = 3
t0 = time()
frames = []
for _ in range(int(RATE/FRAMES_PER_BUFFER*seconds)):
    frames.append(stream.read(FRAMES_PER_BUFFER))

stream.stop_stream()
stream.close()
p.terminate()

filename = "output.wav"
with closing(wopen(filename, "wb")) as obj:
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(p.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b"".join(frames))

uploadEndpoint = 'https://api.assemblyai.com/v2/upload'
transcriptEndpoint = "https://api.assemblyai.com/v2/transcript"

def upload_file(q):
    headers = {'authorization': API_KEY}
    response = post(uploadEndpoint,
                    headers=headers,
                    data=read_file(filename))
    q.put(response.json()['upload_url'])

def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield data

def get_transcript(q):
    headers = {'authorization': API_KEY}
    json = { "audio_url": q.get() }
    response = post(transcriptEndpoint, json=json, headers=headers)
    transcript_id = response.json()['id']

    pollingEndpoint = transcriptEndpoint + '/' + transcript_id
    while True:
        pollingResponse = get(pollingEndpoint, headers=headers)
        status = pollingResponse.json()['status']
        if status == 'completed':
            print(time()-t0)
            print(pollingResponse.json()['text'])
            break
        elif status == 'error':
            raise ValueError("API ERROR")

q = queue.Queue()
t1 = threading.Thread(target=upload_file, args=(q,))
t1.start()

t2 = threading.Thread(target=get_transcript, args=(q,))
t2.start()

t1.join()
t2.join()