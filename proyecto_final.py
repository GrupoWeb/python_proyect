import pyttsx3
import speech_recognition as sr
import mysql.connector
from difflib import SequenceMatcher as SM


### Variables de entorno
request_data = ""
response_error = 'No se puede entender lo que dices'
description_get = 'no tengo esa información por el momento, me podrias decir de nuevo la informacion para que lo recuerde?'
description_end = 'ok, muchas gracias, hasta luego!'
description_save = 'ya almacene el dato en mi memoria, puedes repetirme la pregunta por favor!'



recognizer = sr.Recognizer()
microphone = sr.Microphone(device_index= 0)
eng = pyttsx3.init()
eng.setProperty("rate",140)
eng.setProperty("volume",1.0)
listVoices = eng.getProperty("voices")
eng.setProperty("voice",listVoices[0].id)
eng.say("Hola, soy Maritza. ¿En qué puedo ayudarte?")
eng.runAndWait()


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
      
def __setData(key,descripction):
      query = "INSERT INTO diccionario_datos(key_data,descripcion) VALUES(%s,%s)"
      cursor.execute(query,(str(key), str(descripction)))
      conexion.commit()
      
      return True

def __getData(busqueda):

      cursor.execute("SELECT * FROM diccionario_datos WHERE key_data = '"+busqueda+"'")
      records = cursor.fetchall()
      rows_affected=cursor.rowcount
      if rows_affected == 1:
            return records
      else:
            return 0
      
      


while True:
      request_data = recognizeMicAudio()
      
      if request_data != 'silencio':
            data = __getData(request_data)
            if data != 0:
                  for fila in data:
                        id_data = fila[0]
                        key_data = fila[1]
                        description_data = fila[2]
                        comparacion = SM(None,key_data,request_data).ratio()
                        print(request_data)
                        print(comparacion)
                        if comparacion > 0.7:
                              eng.say(description_data)
                              eng.runAndWait()
                        else:
                              eng.say(description_get)
                              eng.runAndWait()
                              request_description = recognizeMicAudio()
                              __setData(request_data,request_description)
            else:
                  eng.say(description_get)
                  eng.runAndWait()
                  request_description = recognizeMicAudio()
                  __setData(request_data,request_description)
                  eng.say(description_save)
                  eng.runAndWait()
      else:
            eng.say(description_end)
            eng.runAndWait()
            break
