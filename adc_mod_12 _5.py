##import Adafruit_BBIO.ADC as ADC#--com thisPC
##import Adafruit_BBIO.GPIO as GPIO
import datetime
from datetime import datetime
from datetime import time
import time
import os
import threading
import random
import socket
import sys
from Tkinter import *
import tkMessageBox
from multiprocessing.pool import ThreadPool
import shutil
import array
from array import *

global sock, j,i
#global connection
i=0
calibrationFactor = 1#--**change when calibrated**
doseValue = 0
##---com thisPC
##relayPin= "P9_41"
try:
	GPIO.setup(relayPin, GPIO.OUT)
	GPIO.output(relayPin, 0)
except Exception as msg:
	print("\nGPIO not initialized Properly")
	print (msg)
relayOnThresholdDoseRateIn_uRperHour = 1000


root = Tk()
j=0
i=0
def on_closing():
        
        if not(tkMessageBox.askyesno("MBAGM","Do you want to close the application?")):
                return
        
        print ("Quitting")
        global sock
        #global connection
        if sock :
                sock.close()
##------com thisPC                
##        GPIO.cleanup()
        
        #pool.join()
        #--hangs program
        root.destroy()
       #. MODBusThread.exit()        

root.protocol("WM_DELETE_WINDOW", on_closing)

def get_machine_storage():
    global mempercent
    result=os.statvfs('/')
    block_size=result.f_frsize
    total_blocks=result.f_blocks
    free_blocks=result.f_bfree
    # giga=1024*1024*1024
    mega=1000*1000
    total_size=total_blocks*block_size/mega
    free_size=free_blocks*block_size/mega
##    print('total_size = %d' % total_size)
##    print('free_size = %d' % free_size)
    mempercent = (free_blocks*100/total_blocks)
    return mempercent
##    print('free_percent= %d' %mempercent)


#---get screensize-----
width1=root.winfo_screenwidth()
height1= root.winfo_screenheight()
strsize= str(width1)+'x'+str(height1)#+'+'+str(width1/4)+'+'+str(height1/4)
#--size of window

root.geometry(strsize)
root.update()

ww=root.winfo_width()
hh=root.winfo_height()


root.title("MBAGM")
##f1= Frame(root)
##f1.grid(row=0, column=0)

#--reserve w1 for title and logo--
logo=PhotoImage(file= ( os.path.dirname(os.path.realpath(sys.argv[0])) + "/dhruva2.gif"))
##w= logo.width
##h=logo.height

tex1="MODBUS BASED AREA GAMMA MONITOR"
w1a= Label(root,image=logo)#,anchor=W)#.pack(side="left")
w1a.place(x=0, y=0, width=ww, height=hh)


c1= Canvas(root, width=95, height=95)
cc=c1.create_oval(5,5,95,95, fill="#159", outline="#159")
c1.place(x=(ww-ww/200-ww/10-5),y=15)
c1.update()
##c1.grid(row=0,column=50)
##c1.pack()

#------title----------------
w2b= Label(root,text= tex1,fg= "blue",font=("Courier", 30,"bold"))
#w2b.grid(row= 1,padx=(ww/4))
w2b.place(x=ww/8+2,y=15)
#-----------------------------

displayVariable = StringVar()
displayVariable.set(str(doseValue)+'\n'+' uR/h')

#----------PLACE DOSE ON LABEL------------------
w1a.config(textvariable= displayVariable,fg="red",font=("Courier", 100,"bold"),   compound = CENTER)
w1a.update()
offset = (3*hh/5)+15

#----------logo and RSSD----------------------- 
logo2=PhotoImage(file= ( os.path.dirname(os.path.realpath(sys.argv[0])) + "/index.gif"))
w3a=Label(root, image=logo2)
w3a.place(x=ww/200,y=15,width=(ww/10),height=(ww/10))#--top right

w3=Label(root,text=("Developed by "+'\n'+"RMS&DS/RSSD"), font=("ms serif", 15, "italic"),anchor= NW)
##w3.place(x=(8*ww/10+8)/2,y= (7*hh/8+6)*2, height=(hh/8-4)/2, width=(6*ww/7-4))#--bottom right
w3.place(x=(6*ww/7-ww/40-5),y=(10*hh/11-hh/24))
w3.config(bg=root['bg'])

#----------date and time-----------------------

##VarTime=StringVar()
now= datetime.now()
tempstr=now.strftime("%d/%m/%Y %H:%M:%S")
print(tempstr)

VarTime= StringVar()
VarTime.set("dd mm yy HH MM SS")

w3b=Label(root)

##w3b.config(bg= "yellow")
w3b.config(textvariable= VarTime,font=("ms serif", 15))
w3b.update()#----------------------------#################################################################
w3b.place(x=ww/200,y=(11*hh/12), width= ww/5+10)
##w3b.config(bg=root['bg'])

#---update conn status from MODBusTCPThread thread in the label--
Var1= StringVar()
Var1.set("Disconnected")

w4= Label(root)
w4.config(textvariable=Var1,font=("Courier", 20))
w4.update()##########################################################################################
w4.place(x=ww/4+1,y=offset+(3*hh/15)+2)

##-----------test-----------------
##w3b.config(textvariable=Var1,font=("ms serif", 15, "italic"), compound= CENTER)
##--------------------------------

w5= Label(root, bg= "grey",text= "Server IP",font=("Courier", 14))
w5.place(x= ww/10+2,y=(offset+hh/15),height=hh/15)
w6=Label(root, bg="grey", text= "Client IP",font=("Courier", 14))
w6.place(x= ww/10+2,y=(offset+(2*hh/15)),height=hh/15)

e1= Entry(root,font=("Courier", 13,"bold"))
e1.place(x=ww/5+2,y=(offset+hh/15),height=hh/15)
e2= Entry(root,font=("Courier", 13, "bold"))
e2.place(x=ww/5+2,y=(offset+(2*hh/15)),height=hh/15)
#e1.pack(side= "right")

e1.insert(0,"###.###.###.###:####")
e1.config(state=DISABLED)
e2.insert(0,"###.###.###.###:####")
e2.config(state=DISABLED)

##---com thisPC------  
##ADC.setup()
def ShowDoseValueOnDisplay(lock):
        global value1
        toggle=0
        value1=round(random.random()*100,2)
        while True :
                
                dirName = os.path.dirname(os.path.realpath(sys.argv[0])) + '/' + 'logging'+'/' + time.strftime("%Y")+'/'+ time.strftime("%m")+'/' #+ time.strftime("%d")+'/'
             
                if not os.path.exists(dirName):
                        os.makedirs(dirName)
                        
                value=value1
              
                timestr =time.strftime("%d")

              
                
                if not os.path.isfile(dirName+timestr+'.log'):
                        #--code to check memory here/test a replica outside  this'if'---
##                        st=get_machine_storage()
##                        print(st)
##                        if (st>=30):
##                                 shutil.rmtree(dirName)
                        #------------------------------

                        
                        f2=open(dirName+timestr+'.log','a')
                        f2.write("\tTime" +'\t\t'+"Dose Rate")

                        
                elif os.path.isfile(dirName+timestr+'.log'):
                        f2= open(dirName+timestr+'.log','a')
                        
                f2.write("\r\n\t"+ time.strftime('%H:%M:%S')+'\t')
                       
                #----uR/h to mR/h conversion -----
                if (value<1000):
                        f2.write("%d  uR/h" %value)
                        strdose= str(value) + '' + ' uR/h'
                elif (value>=1000):
                        floatValue=value/float(1000)
                        f2.write("%f  mR/h" %floatValue)
                        strdose= str(floatValue) + '' + ' mR/h'
                f2.close()

#--code to check and clean memory here/deletes the month folder in ../logging/year---
##---comThisPC-----------------------
##
##
##                st=get_machine_storage() 
##                
##
##                if (st>=80) & os.path.isfile(dirName+timestr+'.log'):# os.path.exists(dirName):
##                        os.remove(dirName+timestr+'.log')#shutil.rmtree(dirName)
               #------------------

                        
                displayVariable.set(strdose)
##-------------------------com thisPC-----------------------------------------------------------
##################################  Relay Control  ############################################
##                global relayOnThresholdDoseRateIn_uRperHour
##                global relayPin
##                if (value >= relayOnThresholdDoseRateIn_uRperHour):
##                        GPIO.output(relayPin,1)
##                else :
##                        GPIO.output(relayPin,0)
#####################################################################################################
                
                
                c1.itemconfig(cc, fill= "red")
                if (toggle==0):
                      
                        c1.itemconfig(cc, fill= "red", outline="red")
                        c1.update()
                        toggle=1
                else:
                        
                        c1.itemconfig(cc, fill= "green", outline="green")
                        c1.update()
##                        c1.configure(outline= "red")#fill= "#1f1")
                        toggle=0
                time.sleep(10)

              
#-----------------------------------------------------------------------------------------------
def getIP():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
        # doesn't even have to be reachable
                s.connect(('10.255.255.255', 1))
                IP = s.getsockname()[0]
        except:
                IP = '127.0.0.1'
        finally:
                s.close()
                return IP
##-------------------------------------------------------------
def readDoseValue():
##        adcValue = ADC.read_raw("AIN5") ##--com thisPC
        #global curDose ##--for average dose
##        global value1
        lock.acquire()
        global doseValue,j ##--doseValue is average of curDose
        global calibrationFactor
        j=j+1
##        doseValue = int(adcValue * calibrationFactor)##--com thisPC adcValue replaced by 10
        doseValue=  random.random()*100
        doseValue= round(doseValue,2)
##        value1=doseValue
        ###--'doseValue' should now be an avg of 10 doses 
        lock.release()
        #averageDoseValue()
##        return value1
       

def averageDoseValue(name):
        global doseValue,i,j, value1 #, curDose=[]  #, curDose[10]
        curDose= []
        avgDose= []
        j=0
##        doseValue= random.random()*100
        xx= 0
        avgDose.insert(j,0)
##        doseValue= ADC.read_raw("AIN5")
##        curDose.insert(i,doseValue)
        while True:
##                j=(i+1)%10
                if (i>=9) :
                        j=(i+1)%10
##                        if(isinstance(j,int)):
##                                xx=doseValue
                        print('j='+ str(j))
                        
##                        return
                
                ##---average dose-----
##              for i in range(5):#(j, (j+10)):
##              doseValue= ADC.read_raw("AIN5") ##--com thisPC
                doseValue= random.random()*100
                doseValue= round(doseValue,2)
                curDose.insert(i,doseValue)

                if(j==1):
                        value1=(xx/10)
                        xx=0
                        print('value1= '+ str(value1))
                        

                        ##print('j='+ str(j))
##                        time.sleep(5)
                
        ##        doseValue= ADC.read_raw("AIN5")
                if (i>0):
                
##                        xx= curDose[i]+ curDose[i-1]
                        xx= curDose[i]+ xx
##                      curDose[i-1]= xx
####                    avgDose[j]=avgDose[j]/10
                        print('i='+str(i))
                        print('xx='+ str(xx))
                
                        ##print(i)
               
                        time.sleep(0.2)
                
                
                print('last' + '\t' + str(curDose[-1]))
                i=i+1
                time.sleep(1)

#=================start thread==================================               
def MODBusTCPThread(lock):
        global sock
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print ('Socket Created')
        #----status----
        Var1.set('Socket Created')
        w4.config(bg="green",font=("Courier", 15))
        time.sleep(2)

        # Bind the socket to the port
        server_address = (getIP(), 502)
        #----status----
        e1.config(state=NORMAL,fg="blue")
        e1.delete(0,END)
        e1.insert(0,(str(server_address[0])+':'+str(server_address[1])))
        e1.config(state=DISABLED)
    
        try : 
                sock.bind(server_address)
        except socket.error as msg :
                print ('*********Bind failed************ \n Error Code : ' + str(msg[0]) + ' :  ' + msg[1])
                Var1.set('Socket Binding failed - Error Code : ' + str(msg[0]) + ' :  ' + msg[1])
        #w4.config(bg="red",font=("Courier", 20))
                w4.config(bg="red")
                time.sleep(2)
                sys.exit()

        print ('Socket binding Completed and Connection Started')
        #----status----
        Var1.set('Socket binding Completed and Connection Started')
        #w4.config(bg="yellow",font=("Courier", 20))
        w4.config(bg="yellow")
        time.sleep(2)
        #print('Connection Started on %s port %s' % server_address)
        #sock.bind(server_address)
        # Listen for incoming connections
        sock.listen(1)

        while True:
                print('Waiting for connection on %s port %s' % server_address)
        
                #----status----
                Var1.set('Waiting for connection on '+str(server_address[0])+':'+str(server_address[1]))
                w4.config(bg="magenta", fg="black")#,font=("Courier", 20))

                #e2.insert(0,"###.###.###.###:####")
                e2.config(state=NORMAL)
                e2.delete(0,END)
                e2.insert(0,"###.###.###.###:####")
                e2.config(state=DISABLED)
                #global connection
                connection, client_address = sock.accept()

                print ("*******************Connected! Hello Cargo Scanner --AGM************************")
                #----status----
                Var1.set('*Connected! Hello Cargo Scanner --AGM*' )
                w4.config(bg="Green", fg="blue",justify=CENTER)
        
                try:
                    #print "connection from ", client_address
            
                    #print ("connection from %s",client_address)

                    #----status----
                    e2.config(state=NORMAL)
                    e2.delete(0,END)
                    e2.insert(0,(str(client_address[0])+':'+str(client_address[1])))
                    e2.config(state=DISABLED)
                    # Receive the data in small chunks and retransmit it
                    while True:
                        try : 
                            data = connection.recv(1024)
                        except socket.error as msg:
                            print ('*****************Connection failed**************\n Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
                            Var1.set('Connection failed-Error Code : ' + str(msg[0]) + ' :  ' + msg[1])
                            w4.config(bg="red")#,font=("Courier", 20))
                            time.sleep(2)
                            break
                        if data:
                            print("\nData Received from Client :")
                            print(" ".join("{0:x}".format(ord(c)) for c in data))
                    
                            if  ((ord(data[2])<<8)+ord(data[3]))!=0 :
                                sendDataString = 'Not a valid MODBUS Packet'#--4th byte should be 0 to ascertain TCP protocol
                            else :
                                sendDataBuffer1 = data[0:5] #it will copy the first five bytes of data not six
                                #print('sending data to the client')
                                dataList = list (data)	
                                if ord(dataList[7])!=4 :  #--4 fC for reading Input register, 3 is fC for reading Holding registers  
                                    sendDataBuffer2= chr(0x3) + data[6] + chr(ord(dataList[7]) | 0x80) + chr(0x01)
                                elif ((ord(data[8])<<8)+ord(data[9]))!=0 :
                                    sendDataBuffer2= chr(0x3) + data[6] + chr(ord(dataList[7]) | 0x80) + chr(0x02)
                                elif ((ord(data[10])<<8)+ord(data[11]))!=1 :
                                    sendDataBuffer2= chr(0x3) + data[6] + chr(ord(dataList[7]) | 0x80) + chr(0x02)
                                else :
                                    #value = int(ADC.read_raw("AIN5"))
                                    lock.acquire()
                                    global doseValue
                                    value = doseValue
                                    lock.release()
                                    sendDataBuffer2 = chr(0x5) + dataList[6] + dataList[7] + chr(0x02) + chr(0xFF & (value>>8)) + chr(value & 0x00ff)
                                sendDataString =  sendDataBuffer1 +  sendDataBuffer2
                                print("Data Sent to Client")
                                print(" ".join("{0:x}".format(ord(c)) for c in sendDataString))
                                connection.send(sendDataString)
                        else:
                            print 'no more data from'+ str(client_address[0])+':'+str(client_address[1])
                            break
                
                finally:
                # Clean up the connection
                    #sock.close()
                    connection.close()

#===========end thread==============================================

def time_update(name):
          #----date time update--
                
              while True:
                now= datetime.now()
##                print(now)
                time.sleep(1)
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                VarTime.set(dt_string)
##                VarTime.update()
                

        
#-------------------------------------------------------------------
lock = threading.Lock()
#adcValue=0
GUIDoseDisplayThread = threading.Thread(target= ShowDoseValueOnDisplay, args=(lock,))
MODBusThread= threading.Thread(target=MODBusTCPThread, args=(lock,))
TimeUpdateThread= threading.Thread(target=time_update, args=(1,))
DemoAverageThread= threading.Thread(target=averageDoseValue, args=(1,))
MODBusThread.daemon= True
GUIDoseDisplayThread.daemon = True
TimeUpdateThread.daemon= True
DemoAverageThread.daemon= True
MODBusThread.start()
GUIDoseDisplayThread.start()
TimeUpdateThread.start()
DemoAverageThread.start()
##get_machine_storage()
root.mainloop()
