from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import paho.mqtt.client as mqtt
import json
from time import sleep, localtime, strftime
import RPi.GPIO as GPIO




Off = 1
On = 2
Quit = False
blink = True
OutdoorTemp = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(21,GPIO.IN, pull_up_down=GPIO.PUD_UP)

degree_sign= u'\N{DEGREE SIGN}'

stolpeStatus = Off
vedbodStatus = Off
garageStatus = Off
stugaStatus  = Off


client = mqtt.Client("DoorBell") #create new instance

def on_connect(client) :
    global vedbodStatus, stolpeStatus, garageStatus, stugaStatus

    #On start, ask devices for their status and set images on screen accordingly
    #on_message takes care of the answer
    stolpeStatus = Off
    vedbodStatus = Off
    garageStatus = Off
    stugaStatus  = Off


#---------------------------------

def setStolpe():
    global vedbodStatus, stolpeStatus, garageStatus, stugaStatus

    if stolpeStatus == On :
        client.publish("stolpe/rpc",'{"id":123, "src":"stolpe", "method":"Switch.Set", "params":{"id":0,"on":false}}')
        stolpeStatus == Off
    else :
        client.publish("stolpe/rpc",'{"id":123, "src":"stolpe", "method":"Switch.Set", "params":{"id":0,"on":true}}')
        stolpeStatus == On

def setVedbod():
    global vedbodStatus, stolpeStatus, garageStatus, stugaStatus

    if vedbodStatus == On :
        client.publish("vedbod/rpc",'{"id":123, "src":"vedbod", "method":"Switch.Set", "params":{"id":0,"on":false}}')
        vedbodStatus = Off
    else :
        client.publish("vedbod/rpc",'{"id":123, "src":"vedbod", "method":"Switch.Set", "params":{"id":0,"on":true}}')
        vedbodStatus = On

def setGarage():
    global vedbodStatus, stolpeStatus, garageStatus, stugaStatus

    if garageStatus == On :
        client.publish("garage/rpc",'{"id":123, "src":"garage", "method":"Switch.Set", "params":{"id":0,"on":false}}')
        garageStatus = Off
    else :
        client.publish("garage/rpc",'{"id":123, "src":"garage", "method":"Switch.Set", "params":{"id":0,"on":true}}')
        garageStatus = On

def setStuga():
    global vedbodStatus, stolpeStatus, garageStatus, stugaStatus

    if stugaStatus == On :
        client.publish("stuga/rpc",'{"id":123, "src":"stuga", "method":"Switch.Set", "params":{"id":0,"on":false}}')
        stugaStatus = Off
    else :
        client.publish("stuga/rpc",'{"id":123, "src":"stuga", "method":"Switch.Set", "params":{"id":0,"on":true}}')
        stugaStatus = On

#---------------------------------

def QuitClick():
    global Quit

    Quit = True
    root.quit()



def on_message(client, userdata, message):
    global vedbodStatus, stolpeStatus, garageStatus, stugaStatus, OutdoorTemp, stolpe, stolpeON, image

    payload = str(message.payload.decode("utf-8"))
    #print("message received " ,payload)

    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)


    if message.topic == "stolpe/status/switch:0" :
        js = json.loads(payload)
        if js.get('output') == True :
            stolpeStatus = On
            stolpe.configure(image = stolpeON)
        else:
            stolpeStatus = Off
            stolpe.configure(image = stolpeOFF)


    if message.topic == "stolpe/events/rpc" :
        js = json.loads(payload)
        try:
            if js["params"]["switch:0"]["output"] == True :
                stolpeStatus = On
                stolpe.configure(image = stolpeON)
            if js["params"]["switch:0"]["output"] == False :
                stolpeStatus = Off
                stolpe.configure(image = stolpeOFF)
        except:
            pass


    if message.topic == "vedbod/status/switch:0" :
        js = json.loads(payload)
        if js.get('output') == True :
            vedbodStatus = On
            vedbod.configure(image = vedbodON)
        if js.get('output') == False :
            vedbodStatus = Off
            vedbod.configure(image = vedbodOFF)


    if message.topic == "vedbod/events/rpc" :
        #print(payload)
        js = json.loads(payload)
        try:
            if js["params"]["switch:0"]["output"] == True :
                vedbodStatus = On
                vedbod.configure(image = vedbodON)
            if js["params"]["switch:0"]["output"] == False :
                vedbodStatus = Off
                vedbod.configure(image = vedbodOFF)
        except :
            pass



    if message.topic == "garage/status/switch:0" :
        js = json.loads(payload)
        if js.get('output') == True :
            garageStatus = On
            garage.configure(image = garageON)
        if js.get('output') == False :
            garageStatus = Off
            garage.configure(image = garageOFF)


    if message.topic == "garage/events/rpc" :
        js = json.loads(payload)
        if js["params"]["switch:0"]["output"] == True :
            garageStatus = On
            garage.configure(image = garageON)
        if js["params"]["switch:0"]["output"] == False :
            garageStatus = Off
            garage.configure(image = garageOFF)


    if message.topic == "stuga/status/switch:0" :
        js = json.loads(payload)
        if js.get('output') == True :
            stugaStatus = On
            stuga.configure(image = stugaON)
        if js.get('output') == False :
            stugaStatus = Off
            stuga.configure(image = stugaOFF)


    if message.topic == "stuga/events/rpc" :
        js = json.loads(payload)
        try:
            if js["params"]["switch:0"]["output"] == True :
                stugaStatus = On
                stuga.configure(image = stugaON)
            if js["params"]["switch:0"]["output"] == False :
                stugaStatus = Off
                stuga.configure(image = stugaOFF)
        except:
            pass


    if message.topic == "house/env" :
        #print(message.topic)
        try:
            js = json.loads(payload)
            print(js)
            if "sensor_id" in js :
                if js['sensor_id'] == "outdoorTemp" :
                    OutdoorTemp = float(js["properties"]["Temp"])
                    #if OutdoorTemp > 0 and OutdoorTemp <= 5:
                    #    thistemp.config(foreground="orange")
                    #if OutdoorTemp > 5 :
                    #    thistemp.config(foreground="green")
                    #thistemp.set(str(OutdoorTemp) + degree_sign)
        except:
            pass

def timer():
    global blink, OutdoorTemp
    #clock.set(str(h)+":"+str(m))

    if blink :
        string = strftime('%H:\n%M')
        blink = False
    else:
        string = strftime('%H \n%M')
        blink = True
    thistime.set(string)

    xx = ttk.Label(master=None)
    xx.after(1000, timer)


root = Tk()
root.geometry("320x240+0+0")
root.overrideredirect(1) # Remove Window-Menu row at top and border

mainframe = ttk.Frame(root, padding=(0,0,0,0))#, background="black")
mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=0)
root.grid_rowconfigure(0,weight=0)

#Load all images
stolpeON  = ImageTk.PhotoImage(Image.open("images/lamp-post-on.png"))
stolpeOFF = ImageTk.PhotoImage(Image.open("images/lamp-post-off.png"))
vedbodON  = ImageTk.PhotoImage(Image.open("images/vedbod-on.png"))
vedbodOFF = ImageTk.PhotoImage(Image.open("images/vedbod-off.png"))
garageON  = ImageTk.PhotoImage(Image.open("images/garage-on.png"))
garageOFF = ImageTk.PhotoImage(Image.open("images/garage-off.png"))
stugaON   = ImageTk.PhotoImage(Image.open("images/stuga-on.png"))
stugaOFF  = ImageTk.PhotoImage(Image.open("images/stuga-off.png"))

#Define buttons
stolpe = ttk.Button(mainframe, image=stolpeOFF, command=setStolpe)
vedbod = ttk.Button(mainframe, image=vedbodOFF, command=setVedbod)
garage = ttk.Button(mainframe, image=garageOFF, command=setGarage)
stuga  = ttk.Button(mainframe, image=stugaOFF,  command=setStuga)

stolpe.grid(column=0, row=0, sticky=N, pady=0, padx=0)
vedbod.grid(column=1, row=0, sticky=N, pady=0, padx=0)
garage.grid(column=0, row=1, sticky=N, pady=0, padx=0)
stuga.grid(column=1,  row=1, sticky=N, pady=0, padx=0)


quit = ttk.Button(mainframe, text="Quit", command=QuitClick).grid(column=2, row=0, sticky=N, pady=0, padx=0)


thistime = StringVar()
timelabel = ttk.Label(mainframe, textvariable=thistime, foreground="darkblue", borderwidth = 0,font=("Helvetica", 24, "bold"))
timelabel.place(x=270, y=40)

thistemp = StringVar()
templabel = ttk.Label(mainframe, textvariable=thistemp, foreground="red", borderwidth=0,font=("Helvetica", 20, "bold"))
templabel.place(x=255, y=210)


#Connect to MQTT
client.connect("sara.local") #connect to broker
client.on_message=on_message #attach function to callback
#client.on_disconnect = on_disconnect
#client.on_connect = on_connect

#client.subscribe("house/lights/#")
#client.subscribe("house/doorbell/#")
client.subscribe("stolpe/status/switch:0")
client.subscribe("vedbod/status/switch:0")
client.subscribe("garage/status/switch:0")
client.subscribe("stuga/status/switch:0")

client.subscribe("stolpe/events/rpc")
client.subscribe("vedbod/events/rpc")
client.subscribe("garage/events/rpc")
client.subscribe("stuga/events/rpc")

client.subscribe("house/env")

client.loop_start()

client.publish("stolpe/command",'status_update')
sleep(0.5)
client.publish("vedbod/command",'status_update')
sleep(0.5)
client.publish("garage/command",'status_update')
sleep(0.5)
client.publish("stuga/command", 'status_update')


timer()
root.mainloop()
