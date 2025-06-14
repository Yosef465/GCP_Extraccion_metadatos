##Importa el decorador necesario para definir funciones compatibles con Cloud Functions
import functions_framework

## Módulo para registrar eventos en Cloud Logging
import logging

## (Opcional) Módulo para manejar datos JSON, aunque no se utiliza directamente aquí
import json

## Configura el nivel de detalle de los registros
## 'INFO' permite ver tanto los mensajes informativos como errores
logging.basicConfig(level=logging.INFO)

## Define la función que se ejecutará cuando se dispare un evento CloudEvent
## Esta función se activa cuando se sube un archivo a un bucket configurado
@functions_framework.cloud_event
def registrar_metadatos(event):
    try:
        ## Extrae el contenido del evento (metadatos del archivo subido)
        data = event.data

        ## Imprime un mensaje en consola que también aparece en los registros
        print("===> Evento recibido")  

        # Valida que los datos no estén vacíos
        if not data:
            raise ValueError("El evento no contiene datos")

        ## Extrae el nombre del archivo, su tamaño y tipo MIME
        ## Usa un valor por defecto ("No disponible") si alguna clave no existe
        nombre = data.get("name", "No disponible")
        tamaño = data.get("size", "No disponible")
        tipo = data.get("contentType", "No disponible")

        ## Registra los metadatos en Cloud Logging
        logging.info(f"Archivo subido: {nombre}")
        logging.info(f"Tamaño del archivo: {tamaño} bytes")
        logging.info(f"Tipo MIME: {tipo}")

        ## Mensaje final para indicar que todo se procesó correctamente
        logging.info("Evento procesado correctamente")

    except Exception as e:
        ## Captura cualquier error ocurrido en el proceso
        ## Registra el error completo incluyendo la traza (exc_info=True)
        logging.error("Error en la función", exc_info=True)
