import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
# Configuración de la base de datos MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Reemplaza con tu URL de conexión si es diferente
db = client['SupercellDB']  # Reemplaza con el nombre de tu base de datos
collection = db['lecturasRFID']  # Reemplaza con el nombre de tu colección

# Configuración del cliente MQTT
mqtt_broker = "3.80.139.206"  # Reemplaza con la dirección de tu broker MQTT
mqtt_topic = "SupercellDB/lecturasRFID"  # Reemplaza con tu tópico MQTT

# Mapeo de tarjetas y tipos
tarjetas_acceso_garantizado = {
    "tipo_1": ["3C29A464", "2CDB3264"],  # IDs de tarjetas con acceso garantizado
    "tipo_2": ["2340E60E"]  # IDs de tarjetas con acceso denegado
}

def on_message(client, userdata, message):
    tarjeta_id = message.payload.decode("utf-8")
    lector_id = "RFID-1"  # ID del lector específico, ajusta según tu configuración
    timestamp = datetime.now()

    if tarjeta_id in tarjetas_acceso_garantizado["tipo_1"]:
        acceso = "garantizado"
        tipo = "tipo_1"
    elif tarjeta_id in tarjetas_acceso_garantizado["tipo_2"]:
        acceso = "denegado"
        tipo = "tipo_2"
    else:
        acceso = "desconocido"
        tipo = "desconocido"

    # Crear el documento para insertar en la base de datos
    documento = {
        "tarjeta_id": tarjeta_id,
        "tipo": tipo,
        "acceso": acceso,
        "lector_id": lector_id,
        "timestamp": timestamp
    }

    # Insertar el documento en la colección de MongoDB
    collection.insert_one(documento)
    print(f"Tarjeta ID: {tarjeta_id}, Tipo: {tipo}, Acceso: {acceso}, Timestamp: {timestamp}")

# Configuración del cliente MQTT
client = mqtt.Client()
client.on_message = on_message

client.connect(mqtt_broker)
client.subscribe(mqtt_topic)

client.loop_forever()
