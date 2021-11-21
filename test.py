# -*- coding: utf-8 -*-
from time import sleep
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import serial
import time
import pymysql
import datetime


class Connection:
    """首先获取连接对象conn"""
    conn = pymysql.connect(
        host="120.26.167.88",  # 指示host表明是本地MySQL还是远程
        port=3306,
        user="root",  # 用户名
        password="MySQL@123!",  # 密码
        db="test",  # 要连接的数据库名
        charset="utf8mb4",  # 指定字符集，可以解决中文乱码
        cursorclass=pymysql.cursors.DictCursor
    )

    def Insert(self):
        datatimenow=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(datatimenow)
        try:
            with self.conn.cursor() as cursor:
                sql = "insert into testsensordb (time, humidity,temp,co2) values(%s, %s,%s,%s)"
                result = cursor.execute(sql, (datatimenow, 11.0,11.0,11.0))
                self.conn.commit()  # 提交事务
        finally:
            self.conn.close()

        def Insert(self,encode):
            datatimenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(datatimenow)
            try:
                with self.conn.cursor() as cursor:
                    sql = "insert into testsensordb (time, humidity,temp,co2) values(%s, %s,%s,%s)"
                    result = cursor.execute(sql, (datatimenow, encode[0] / 10, encode[1] / 10, encode[2]))
                    self.conn.commit()  # 提交事务
            finally:
                self.conn.close()



class sensorReader(object):
    def __init__(self, serialCom, baud=4800, devAddr=1):
        """
        实例初始化时，自动打开端口以及modbus协议
        """
        self.serialCom = serialCom  # 端口号 COM3或其他
        self.baud = baud  # 波特率 4800
        self.devAddr = devAddr  # 设备号

        try:
            self.mSerial = serial.Serial(self.serialCom, self.baud)
            if self.mSerial.isOpen():
                print("串口通信打开成功")
            print("初始化modbus服务")
            self.master = modbus_rtu.RtuMaster(self.mSerial)
            self.master.set_timeout(5)
            self.master.set_verbose(True)
            print("Modbus服务启动成功")
        except Exception as error:
            self.mSerial.close()
            print("异常\n")
            print(error)
            print("=====\n")

    def closeCom(self):
        self.mSerial.close()
        if self.mSerial.isOpen():
            print("关闭失败")
        else:
            print("关闭成功")

    def deCode(encode):
        result = []
        humidity = encode[0] / 10
        humidity = str(humidity) + " %"
        result.append(humidity)
        temp = encode[1] / 10
        temp = str(temp) + "摄氏度"
        result.append(temp)
        co2 = encode[2]
        co2 = str(co2) + "ppm"
        result.append(co2)
        return result

    def readData(self):
        conn=Connection()
        conn.Insert()
        encode = self.master.execute(self.devAddr, cst.READ_HOLDING_REGISTERS, 0, 5)
        # encode.set_timeout(1.0)

        conn.Insert(encode)
        print(encode)
        result = []
        humidity = encode[0] / 10
        humidity = "湿度:" + str(humidity) + "%"
        result.append(humidity)
        temp = encode[1] / 10
        temp = "温度:" + str(temp) + "摄氏度"
        result.append(temp)
        co2 = encode[2]
        co2 = "二氧化碳浓度:" + str(co2) + "ppm"
        result.append(co2)
        print(result)
        time.sleep(10)


sensor = sensorReader("COM3", 4800, 1)

while True:
    sensor.readData()
