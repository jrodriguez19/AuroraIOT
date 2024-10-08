import paho.mqtt.client as mqtt
from sensors.models import *
from mqttclient.models import *
import json
import time
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# from django.contrib.contenttypes.models import ContentType


# The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
    '''
    Arguments:
        client: client instace of mqtt.Client()
        rc: return code
    
    Connection Return Codes
    0: Connection successful
    1: Connection refused - incorrect protocol version
    2: Connection refused - invalid client identifier
    3: Connection refused - server unavailable
    4: Connection refused - bad username or password
    5: Connection refused - not authorised
    6-255: Currently unused.
    '''
    if rc == 0:
        client.connected_flag = True
        logger.info(f'MQTT: Connected successfully, returned code = {rc}')
        client.subscribe('auroraiot/energy', qos=0)
    else:
        logger.error(f'MQTT: Bad connection, returned code = {rc}')
        client.bad_connection_flag = True



FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

def on_disconnect(client, userdata, rc):
    # logging.info("Disconnected with result code: %s", rc)
    logger.warning("on_disconnect() was run")
    client.connected_flag = False
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        # logging.info("Reconnecting in %d seconds...", reconnect_delay)
        logger.info(f"MQTT: Reconnecting in {reconnect_delay} seconds...")
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            # logging.info("Reconnected successfully!")
            logger.info("MQTT: Reconnected successfully!")
            return
        except Exception as err:
            # logging.error("%s. Reconnect failed. Retrying...", err)
            logger.error(f"MQTT: {err}. Reconnect failed. Retrying...")

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    # logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)

# def on_disconnect(client, userdata, rc):
#     #logging.info("disconnecting reason  "  +str(rc))
#     client.connected_flag=False
#     client.disconnect_flag=True
#     #client.loop_stop(force=False) # removed instruction so it will try to reconnect automatically
#     if rc != 0:
#         logger.error("MQTT: Unexpected disconnection, returned code=", rc)
#     else:
#         logger.error("MQTT: Disconnected, returned code=", rc)


# The callback for when a PUBLISH message is received from the server.
def on_message(mqtt_client, userdata, msg):
    string_payload = msg.payload.decode('utf8').replace("'", '"')
    try:
        json_payload = json.loads(string_payload)
        # Saving datareceived via MQTT
        Data_Received.objects.create(
            sensor_id=Sensor(id=json_payload["sensor_id"]),
            data=json_payload["data"]
        )
        # Print data received MQTT only if Debug is True
        if settings.DEBUG:
            logger.debug(f'Topic: {msg.topic} Payload: {json_payload}')

        # Saving Sensor Data_PZEM-004t
        # The list [1,2] should be replaced by a query that collects all ids in the system for available PZEM-004t sensors in case a new sensor is added later on.
        if json_payload["sensor_id"] in [1, 2]:
            Data_PZEM004t.objects.create(sensor_id=Sensor(id=json_payload["sensor_id"]),
                                         sensor_address=json_payload["data"]["address"],
                                         volts=round(json_payload["data"]["voltage"]),
                                         amps=json_payload["data"]["current"],
                                         frequency=round(json_payload["data"]["frequency"]),
                                         watts=json_payload["data"]["power"],
                                         energy=json_payload["data"]["energy"],
                                         # power factor (0.00 to 1.00) is multiplied by 100 to store integer values (0 to 100).
                                         power_factor=json_payload["data"]["pf"] * 100
                                         )

        # content_type = ContentType.objects.get_for_model(Sensor)
        # print(content_type)
        # print(type(content_type))
        # print(ContentType.objects.all(),"\n")
        # Data.objects.create(object_id=json_payload["sensor_id"],  data=json_payload["data"])
        # content_type = ContentType.objects.get_for_model(Sensor)
        # Data.objects.filter(
        #     content_type = content_type,
        #     object_type =
        # )
        # Data.objects.create(object_id=Sensor(id=json_payload["sensor_id"]), data=json_payload["data"])
        ######
    except ValueError as err:
        if string_payload != "ESP32 Connected to MQTT Broker":
            logger.error(f"MQTT: Json data recevied not valid or empty - Error: {err}")
            logger.error(f"MQTT: Erroneous payload received was: {string_payload}")



client = mqtt.Client(client_id=settings.MQTT_CLIENT_ID)
if settings.MQTT_ACTIVE:
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
    client.connected_flag = False
    client.bad_connection_flag = False
    logger.info(f"MQTT: Connecting to Broker {settings.MQTT_SERVER}, {settings.MQTT_PORT}")
    try:
        client.connect(
            host=settings.MQTT_SERVER,
            # The port needs to be passed as int, not str.
            port=int(settings.MQTT_PORT),
            keepalive=settings.MQTT_KEEPALIVE)
        #it's better to call loop_start after connect() 
        #http://www.steves-internet-guide.com/loop-python-mqtt-client/
        #look for: Implementation Note
        client.loop_start()
        logger.debug("MQTT: Loop started")
        #Enter into a waiting loop while the connection is completed
        while not client.connected_flag and not client.bad_connection_flag: #wait in loop while the connection is completed
            logger.debug("MQTT: Waiting in while loop for connection")
            time.sleep(1)
        #This part could be useful for an independent script but not for something like Django
        #because we want to keep the responding even if the MQTT is down
        # if client.bad_connection_flag:
        #     client.loop_stop()    #Stop loop
        #     exit(1)


    except Exception as e:
        logger.error(f"MQTT: client.connect() connection failed, the error was: {e}")
        #logger.error(f"MQTT failed connection to broker server address: {settings.MQTT_SERVER} and port: {settings.MQTT_PORT}")
        # exit(1)

