import sqlite3
import datetime
from datetime import timedelta

def insert_recording(device_id:int, audio:int, motion:int):
    """Assume that the data has already been processed into the form that is supposed to be saved"""
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO data_records VALUES(?,?,?,?)",(device_id,datetime.datetime.now(tz=datetime.timezone.utc),audio,motion))
        connection.commit()
        cursor.close()

def get_all_device_records(device_id:int):
    """Deprecated"""
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM data_records WHERE id = ?", (device_id,))
        result = []
        for entry in cursor.fetchall():
            py_dict = {'datetime':entry[1],'audio':entry[2],'motion':entry[3]}
            result.append(py_dict)
        cursor.close()
        return result

#Return result list and a value indicating minimum audio
def get_all_within_day(device_id:int, date:datetime):
    #Format to convert string to datetime, and the minimum date time we will consider (24 hour period from the given datetime)
    date_format = '%Y-%m-%d %H:%M:%S.%f%z'
    startConsider = date - timedelta(hours = 24)
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM data_records WHERE id = ?", (device_id,))
        
        result = []
        for entry in cursor.fetchall():
            entryDate = datetime.datetime.strptime(entry[1], date_format)
            if startConsider <= entryDate <= date:
                py_dict = {'datetime':entry[1],'audio':entry[2],'motion':entry[3]}
                result.append(py_dict)
        cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
        result = {"name": cursor.fetchone(), "date" : date, "data":result}
        cursor.close()
        return result
def get_all_devices():
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM devices ORDER BY devicename DESC")
        result = []
        for entry in cursor.fetchall():
            py_dict = {'id': entry[0], 'devicename': entry[1]}
            result.append(py_dict)
        cursor.close()
        return result
def initialize_tables():
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS devices (id INTEGER, devicename TEXT,  PRIMARY KEY (id));")
        cursor.execute("CREATE TABLE IF NOT EXISTS data_records (id INTEGER, datetime TEXT, audio INTEGER, motion INTEGER, PRIMARY KEY (id,datetime), FOREIGN KEY (id) REFERENCES devices(id));")
        res = cursor.execute("SELECT name FROM sqlite_master WHERE name='data_records'")
        print(res.fetchone())
        cursor.close()
def add_device(device_id:int, name:str):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO devices VALUES(?,?)",(device_id,name))
        connection.commit()
        cursor.close()
    
if __name__ == '__main__':
    initialize_tables()
    # You must add a device and name to the devices table before inserting records
    # Or not apparently. sqllite does not respect foreign keys for backwards compatibility lmao
    print(get_all_devices())
    
    print(get_all_within_day(1,datetime.datetime.now(tz=datetime.timezone.utc)))
    user_input = input("Add a device? (y/n)")
    if user_input == 'y':
        id = int(input('Give an integer id'))
        name = input('Give a human readable name to the device')
        add_device(id,name)
        print(get_all_devices())
    user_input = input("Add a record? (y/n)")
    if user_input == 'y':
        motion = int(input('Give an integer motion level'))
        name = int(input('Give a integer audio level'))
        id = int(input('Give an integer id for the'))
        