#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Int8

'''

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

'''
from socket import*
import time
import struct

#ip = "10.30.91.119"
ip = "127.0.0.1"
port = 20175
#port = 50000

clientSocket = socket(AF_INET,SOCK_STREAM)  #소켓 생성
clientSocket.connect((ip,port))   # 서버와 연결

print("연결 확인됐습니다.")

bindata = open('gpsdata_little_endian.trj', 'ab')

way = 1


pre_time = 0
pre_lat = 0.000000
pre_lon = 0.000000
pre_alt = 0.000000


count = 0
def talker():
    #pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('gps_recoder', anonymous=False)
    rate = rospy.Rate(100) # 10hz
    global pre_time
    global count
    global pre_lat,pre_alt,pre_lon
    
    while not rospy.is_shutdown():
        #clientSocket.send(aa+"|"+bb)
        clientSocket.send("I am a client".encode("UTF-8"))

        print("메시지를 전송했습니다. %d초"%(count))
        data = clientSocket.recv(1024)  #데이터 수신

        #print("recieved data :"+data.decode())
        #data2 = data.decode()
        a=data.split(",");
        try:
            time_s = a[1]
            lat_s = a[2]
            lon_s = a[4]
            alt_s = a[11]
            

            if(time_s != "") :
                gps_time = float(time_s)
                #if gps_time == pre_time :
                #    continue
                if ((gps_time - pre_time)>=2 and (gps_time%100)!=58 and (gps_time%100)!=59 and (gps_time%100)!=0 and (gps_time%100)!=1):
                    gps_time = gps_time-1
                #if (gps_time - pre_time)<=0 : #& abs(gps_time-pre_time)<50 :
                 #   gps_time = pre_time+1
        
            if(lat_s != "") :
                #lat = float(lat_s)
                lat = float(lat_s[0:2]) + float(lat_s[2:])/60
            else : 
                print("error_ddd")
                lat = pre_lat
            if(lon_s != "") :
                #lon = float(lon_s)
                lon = float(lon_s[0:3]) + float(lon_s[3:])/60
            else :
                lon = pre_lon
            if(alt_s != "") :
                alt = float(alt_s)
            else:
                alt = pre_alt
    
            lat = round(lat,6)
            lon = round(lon,6)
            alt = round(alt,2)
        

        except :
            gps_time = pre_time
            lat = pre_lat
            lon = pre_lon
            alt = pre_alt
            print("value error")

        pre_time = gps_time
        pre_lat = lat 
        pre_lon = lon
        pre_alt = alt

        count = count+1

    
#            count = count+1
#            if count >10:
#            break
    

        bindata.write(struct.pack("<i",way))
#     bindata.write('\t')
        bindata.write(struct.pack("<I",(gps_time)))
#     bindata.write('\t')
        bindata.write(struct.pack("<d",(lat)))
#     bindata.write('\t')
        bindata.write(struct.pack("<d",(lon)))
#     bindata.write('\t')
        bindata.write(struct.pack("<d",(alt)))

    

    
    
    
        #time.sleep(0.005)

    bindata.close()
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
