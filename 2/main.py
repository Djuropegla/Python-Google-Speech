import requests
from api_secrets import API_KEY

uploadEndpoint = 'https://api.assemblyai.com/v2/upload'
transcriptEndpoint = "https://api.assemblyai.com/v2/transcript"

#upload

filename = r"C:\Users\X-TREME\Desktop\faks\epos\Python-Google-Speech\2\panic.wav"
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
print(pollingResponse.json())
while True:
    pollingResponse = requests.get(pollingEndpoint,headers=headers)
    if pollingResponse.json()['status'] == 'completed':
        data = pollingResponse.json()['text']
        print(data)
        break
    elif pollingResponse.json()['status'] == 'error':
        print('It is what it is')


#save transcription