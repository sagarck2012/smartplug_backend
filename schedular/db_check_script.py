import datetime
import sched
import time

import pymysql
import schedule

host = "localhost"
user = "root"
password = ""
db = "smartplug"
conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)


# check and insert the missing device data
def check(*args, **kwargs):
    print('inside check')
    try:
        # conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        sql = "SELECT device_id, id FROM device_reg WHERE device_id NOT IN (SELECT t.device_id FROM temp_device_data AS t WHERE t.timestamp >= DATE_SUB(NOW(), INTERVAL 1 MINUTE))"
        cursor.execute(sql)
        rows = cursor.fetchall()
        time_s = datetime.datetime.now()
        for row in rows:
            print(row)
            cursor2 = conn.cursor()
            cursor3 = conn.cursor()
            cursor4 = conn.cursor()
            cursor5 = conn.cursor()
            sql1 = "SELECT id, TIMESTAMP, device_id,energy_consumption, SUM(energy_consumption) AS sum_en , device_detail_id, is_connected_id FROM ( SELECT id, TIMESTAMP, device_id, energy_consumption, device_detail_id, is_connected_id  FROM device_data WHERE device_id = %s ORDER BY TIMESTAMP DESC LIMIT 3) t"
            cursor2.execute(sql1, row['device_id'])
            single_row = cursor2.fetchone()
            print("single rowwwwwww--", single_row)
            delta = 0
            if single_row == None:
                sql = "INSERT INTO temp_device_data (device_id, timestamp, energy_consumption, device_detail_id, is_connected_id) VALUES (%s,%s,%s,%s,%s)"
                cursor5.execute(sql, (row["device_id"], time_s, 0, row["id"], 2))
                conn.commit()
            else:
                delta = time_s - single_row['timestamp']
                print(delta.total_seconds())
                if single_row["energy_consumption"] == 0 and single_row["sum_en"] == 0:
                    sql_str = "INSERT INTO temp_device_data (device_id, timestamp, energy_consumption, device_detail_id, is_connected_id) VALUES (%s,%s,%s,%s,%s)"
                    cursor3.execute(sql_str, (row["device_id"], time_s, 0, single_row["device_detail_id"], 2))
                    conn.commit()
                elif single_row["energy_consumption"] == 0 and single_row["sum_en"] != 0:
                    sql_str = "INSERT INTO `temp_device_data` (device_id, timestamp, energy_consumption, device_detail_id, is_connected_id) VALUES (%s,%s,%s,%s,%s)"
                    cursor4.execute(sql_str, (row["device_id"], time_s, 0, single_row["device_detail_id"], 1))
                    conn.commit()

            cursor2.close()
            del cursor2
            cursor3.close()
            del cursor3
            cursor5.close()
            del cursor5

        cursor.close()
        del cursor



    except Exception as e:
        print(e)


def updater(*args, **kwargs):
    print('inside updater')
    try:
        cursor = conn.cursor()
        cursor2 = conn.cursor()
        cursor3 = conn.cursor()
        sql = "SELECT * FROM temp_device_data "
        cursor.execute(sql)
        rows = cursor.fetchall()
        print(rows)
        for row in rows:
            sql2 = "INSERT INTO device_data (device_id, timestamp, energy_consumption, device_detail_id, is_connected_id) VALUES (%s,%s,%s,%s,%s)"
            count = cursor2.execute(sql2, (
                row["device_id"], row["timestamp"], row["energy_consumption"], row["device_detail_id"],
                row["is_connected_id"]))
            print(count)
            if count > 0:
                sql3 = "DELETE FROM temp_device_data WHERE device_id = %s AND timestamp = %s"
                cursor3.execute(sql3, (row["device_id"], row["timestamp"]))
                print('deleted')
            conn.commit()
        cursor2.close()
        del cursor2
        cursor3.close()
        del cursor3
        cursor.close()
        del cursor
    except Exception as e:
        print(e)


def run():
    task = sched.scheduler(time.time, time.sleep)
    task.enter(60, 1, check, (task,))
    task.enter(60 * 5, 1, updater, (task,))
    task.run()


def main():
    run()


if __name__ == "__main__":
    main()
