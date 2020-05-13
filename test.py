import io
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

client = speech.SpeechClient.from_service_account_json('credenciales.json')

with io.open('intro.flac','rb') as audio_file:
      content = audio_file.read()
      audio = types.RecognitionAudio(content=content)
      

config = types.RecognitionConfig(
      encoding = enums.RecognitionConfig.AudioEncoding.FLAC,
      sample_rate_hertz = 16000,
      language_code = 'es-es'
)

response = client.recognize(config,audio)

for result in response.result:
      print('Escuchando!!'.format(result.alternative[0].transcript))