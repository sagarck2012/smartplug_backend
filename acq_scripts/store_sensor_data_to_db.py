import datetime
import json
import logging

import pymysql

host = "127.0.0.1"
user = "root"
password = ""
db = "smartplug"


# Config logging format
logger = logging.getLogger(__name__)  # Create a logger object
logger.setLevel(logging.DEBUG)  # Below this level data will be printed to console
file_handler = logging.FileHandler(
    './projectlog/project_log_' + str(datetime.datetime.now().strftime('%Y-%m-%d')) + ".txt")
format = "%(asctime)s :: Source %(name)s :: Line No %(lineno)d :: %(levelname)s ::  %(message)s"
formatter = logging.Formatter(format)  # Create Formratter
file_handler.setFormatter(formatter)  # Add the Fomratter to handler
logger.addHandler(file_handler)  # Add handler to logger


# decide where to send
def sensor_data_handler(Topic, jsonData):
    logger.debug("Inside sensor data handler")
    print("in sensor data")
    if Topic.find("SENSOR") != -1:
        logger.debug(jsonData)
        database_handler(Topic, jsonData)


count = 0


# database handler
def database_handler(Topic, jsonData):
    print('in database handler')
    # print(Topic, jsonData)
    # getting sensor id from topic
    sensor_str = Topic.rsplit('/')
    sensor_id = sensor_str[4]

    try:
        print('in try', 2)
        # getting data from json data
        data = json.loads(jsonData)
        power = data["ENERGY"]["Power"]
        time = datetime.datetime.now()
        conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)

        cursor = conn.cursor()
        # checking if a device exist with same sensor id or not
        sql_str = "SELECT * FROM device_reg WHERE sensor_id = %s"
        cursor.execute(sql_str, sensor_id)
        row = cursor.fetchone()
        # print(row)

        if row["id"] != None:
            print('in con')
            # if a device id is found then inserting the values to temporary database
            sql_insert_string = "INSERT INTO temp_device_data (device_id, timestamp, energy_consumption, device_detail_id, is_connected_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_insert_string, (row["device_id"], time, power, row["id"], 1))

        conn.commit()
        cursor.close()
        logger.debug("Data inserted to database")
    except Exception as e:
        print(e)
        logger.error("Data insertion failed")
        logger.error(e)
