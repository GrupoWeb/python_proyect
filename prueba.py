import pyttsx3
import speech_recognition as sr
import mysql.connector
from difflib import SequenceMatcher as SM
import random
import time



# importlib.reload(sys)
# sys.setdefaultencoding('utf-8')
# importlit.reload(sys)


### Variables de entorno

request_data = ""
x = 1



recognizer = sr.Recognizer()
microphone = sr.Microphone(device_index= 0)
eng = pyttsx3.init()
eng.setProperty("rate",140)
eng.setProperty("volume",1.0)
listVoices = eng.getProperty("voices")
eng.setProperty("voice",listVoices[0].id)
eng.say("Hola, soy Maritza. ¿En qué puedo ayudarte?")
eng.runAndWait()


## Error data

response_error = 'No se puede entender lo que dices'

def recognizeMicAudio():
      request_data = ""
      print("Escuchando")
      with microphone as source:
            audio = recognizer.listen(source)
            try:
                  request_data = recognizer.recognize_google(audio, language="es-ES")
            except sr.UnknownValueError:
                  eng.say(response_error)
                  eng.runAndWait()
            except sr.RequestError as e:
                  eng.say(response_error)
                  eng.runAndWait()
      return request_data

conexion = mysql.connector.connect(host="127.0.0.1", user="root", passwd="12345678", database="asistente")
cursor = conexion.cursor(buffered=True)


while request_data != "silencio":
      request_data = recognizeMicAudio()
      cursor.execute("SELECT * FROM diccionario_datos")
      nDatos = cursor.rowcount
      print(request_data)
      print(nDatos)
      

      for fila in cursor:
            id_data = fila[0]
            key_data = fila[1]
            description_data = fila[2]
            comparacion = SM(None,key_data,request_data).ratio()
            
            if comparacion > 0.7:
                  eng.say(description_data)
                  eng.runAndWait()



      

      # if palabra == "En qué clase estamos":
      #       eng.say("estamos en la clase del ingeniero kalki")
      #       eng.runAndWait()
      # if palabra == "que dia es hoy":
      #       eng.say("hoy es sabado")
      #       eng.runAndWait()
      # if palabra == "adiós":
      #       eng.say("hasta pronto")
      #       eng.runAndWait()
      #       break
      # if  palabra == 'fechas':
      #       # temperatura = dame_Temperatura()
      #       fecha = dimeFecha()
      #       eng.say(fecha)
      #       eng.runAndWait()
      # if  palabra == 'fecha':
      #       # temperatura = dame_Temperatura()
      #       fecha = dimeFecha()
      #       eng.say(fecha)
      #       # eng.say(temperatura)
      #       eng.runAndWait()
      # # eng.say(palabra)
      # # eng.runAndWait()


# print(recognizeMicAudio())