import tkinter
from tkinter import ttk
import abc
from PIL import ImageTk, Image
import paho.mqtt.client as mqtt
import json
from time import sleep, localtime, strftime
import RPi.GPIO as GPIO
import logging


class GUI(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):

        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent


        self.Device = {}

        self.Device["stolpe"] = { "nbr" : 1, "status" : False, "name": "stolpe", "topic" : "stolpe/status/switch:0", "Elementid" : "",
            "picture-on":"stolpe-on.png", "picture-off" : "stolpe-off.png", "picture-disabled" : "stolpe-dis.png" }
        self.Device["vedbod"] = { "nbr" : 2, "status" : False, "name": "vedbod", "topic" : "vedbod/status/switch:0", "Elementid" : "",
            "picture-on":"vedbod-on.png", "picture-off" : "vedbod-off.png", "picture-disabled" : "vedbod-dis.png" }
        self.Device["garage"] = { "nbr" : 3, "status" : False, "name": "garage", "topic" : "garage/status/switch:0", "Elementid" : "",
            "picture-on":"garage-on.png", "picture-off" : "garage-off.png", "picture-disabled" : "garage-dis.png" }
        self.Device["stuga"]  = { "nbr" : 4, "status" : False, "name": "stuga", "topic" : "stuga/status/switch:0",  "Elementid" : "",
            "picture-on":"stuga-on.png",  "picture-off" : "stuga-off.png",  "picture-disabled" : "stuga-dis.png" }

        self.init_gui()




    def timer(self):
        if self.blink :
            string = strftime('%H:\n%M')
            self.blink = False
        else:
            string = strftime('%H \n%M')
            self.blink = True
        self.thistime.set(string)

        #Inviseble label for time counter...
        xx = ttk.Label(master=None)
        xx.after(1000, self.timer)



    def setStolpe(self):
        if self.stolpeStatus == True :
            self.client.publish("stolpe/rpc",'{"id":123, "src":"stolpe", "method":"Switch.Set", "params":{"id":0,"on":false}}')
            self.stolpeStatus = False
        else :
            self.client.publish("stolpe/rpc",'{"id":123, "src":"stolpe", "method":"Switch.Set", "params":{"id":0,"on":true}}')
            self.stolpeStatus = True

    def setVedbod(self):
        if self.vedbodStatus == True :
            self.client.publish("vedbod/rpc",'{"id":123, "src":"vedbod", "method":"Switch.Set", "params":{"id":0,"on":false}}')
            self.vedbodStatus = False
        else :
            self.client.publish("vedbod/rpc",'{"id":123, "src":"vedbod", "method":"Switch.Set", "params":{"id":0,"on":true}}')
            self.edbodStatus = True

    def setGarage(self):
        if self.garageStatus == True :
            self.client.publish("garage/rpc",'{"id":123, "src":"garage", "method":"Switch.Set", "params":{"id":0,"on":false}}')
            self.garageStatus = False
        else :
            self.client.publish("garage/rpc",'{"id":123, "src":"garage", "method":"Switch.Set", "params":{"id":0,"on":true}}')
            self.garageStatus = True

    def setStuga(self):
        if self.stugaStatus == True :
            self.client.publish("stuga/rpc",'{"id":123, "src":"stuga", "method":"Switch.Set", "params":{"id":0,"on":false}}')
            self.stugaStatus = False
        else :
            self.client.publish("stuga/rpc",'{"id":123, "src":"stuga", "method":"Switch.Set", "params":{"id":0,"on":true}}')
            self.stugaStatus = True

    #---------------------------------


    def QuitClick(self):
        #global Quit

        self.Quit = True
        root.quit()


    def Button_callback(self,gpio_id):
        # Disable so we don't queue up stuff
        GPIO.remove_event_detect(self.DoorbellButton)

        GPIO.output(self.DoorbellRelay, GPIO.HIGH)   # Ding
        sleep(0.4)
        GPIO.output(self.DoorbellRelay, GPIO.LOW)    # Dong
        sleep(0.1)

        logging.info("Doorbell activated")

        GPIO.add_event_detect(self.DoorbellButton, GPIO.FALLING, bouncetime=200)
        GPIO.add_event_callback(self.DoorbellButton, self.Button_callback)




    def init_gui(self):

        logging.basicConfig(filename='/home/martin/db.log', format='%(asctime)s %(message)s',  level=logging.INFO)

        #self.root.title('Test GUI')
        self.root.geometry("320x240+0+0")
        self.root.overrideredirect(1) # Remove Window-Menu row at top and border

        #self.grid(column=0, row=0, sticky='nsew')
        #self.grid_columnconfigure(0, weight=1) # Allows column to stretch upon resizing
        #self.grid_rowconfigure(0, weight=1) # Same with row
        #self.root.grid_columnconfigure(0, weight=1)
        #self.root.grid_rowconfigure(0, weight=1)
        #self.root.option_add('*tearOff', 'FALSE') # Disables ability to tear menu bar into own window

        # Menu Bar
        #self.menubar = Menubar(self.root)

        # Create Widgets
        #self.btn = ttk.Button(self, text='Open Window', command=self.openwindow)

        # Layout using grid
        #self.btn.grid(row=0, column=0, sticky='ew')

        # Padding
        #for child in self.winfo_children():
        #    child.grid_configure(padx=10, pady=5)
        #mainframe = ttk.Frame(root, padding=(0,0,0,0))#, background="black")
        self.grid(row=0, column=0, sticky='ew') #(N,W,E,S))
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_rowconfigure(0,weight=0)

        #Load all images
        self.stolpeON  = ImageTk.PhotoImage(Image.open("images/lamp-post-on.png"))
        self.stolpeOFF = ImageTk.PhotoImage(Image.open("images/lamp-post-off.png"))
        self.vedbodON  = ImageTk.PhotoImage(Image.open("images/vedbod-on.png"))
        self.vedbodOFF = ImageTk.PhotoImage(Image.open("images/vedbod-off.png"))
        self.garageON  = ImageTk.PhotoImage(Image.open("images/garage-on.png"))
        self.garageOFF = ImageTk.PhotoImage(Image.open("images/garage-off.png"))
        self.stugaON   = ImageTk.PhotoImage(Image.open("images/stuga-on.png"))
        self.stugaOFF  = ImageTk.PhotoImage(Image.open("images/stuga-off.png"))

        #Define buttons
        self.stolpe = ttk.Button(self, image=self.stolpeOFF, command=self.setStolpe)
        self.vedbod = ttk.Button(self, image=self.vedbodOFF, command=self.setVedbod)
        self.garage = ttk.Button(self, image=self.garageOFF, command=self.setGarage)
        self.stuga  = ttk.Button(self, image=self.stugaOFF,  command=self.setStuga)

        self.stolpe.grid(column=0, row=0, sticky='n', pady=0, padx=0)
        self.vedbod.grid(column=1, row=0, sticky='N', pady=0, padx=0)
        self.garage.grid(column=0, row=1, sticky='N', pady=0, padx=0)
        self.stuga.grid(column=1,  row=1, sticky='N', pady=0, padx=0)


        quit = ttk.Button(self, text="Quit", command=self.QuitClick).grid(column=2, row=0, sticky='N', pady=0, padx=0)

        self.thistime = tkinter.StringVar()
        self.timelabel = ttk.Label(self, textvariable=self.thistime, foreground="darkblue", borderwidth = 0,font=("Helvetica", 24, "bold"))
        self.timelabel.place(x=270, y=40)

        self.thistemp = tkinter.StringVar()
        self.templabel = ttk.Label(self, textvariable=self.thistemp, foreground="red", borderwidth=0,font=("Helvetica", 20, "bold"))
        self.templabel.place(x=255, y=210)


        self.Quit = False
        self.blink = True
        self.OutdoorTemp = 0

        # HARDWARE ports ---------------------------------
        GPIO.setmode(GPIO.BCM)
        #GPIO.setwarnings(False)
        #GPIO.setup(2,GPIO.OUT, initial=GPIO.LOW)
        #GPIO.setup(21,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # GPIO pins
        self.MovementDetector = 18      # Input from movement sensor USED IN BACKLIGHT.PY

        self.DoorbellButton   = 21      # Input from button
        self.DoorbellLed      = 2       # Output to lit the button Led

        self.DoorbellRelay    = 26      # Output for doorbell relay
        self.AnotherRelay     = 20      # Outpur for Relay #2



        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.DoorbellRelay, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.AnotherRelay,  GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.DoorbellLed,   GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(self.DoorbellButton,GPIO.IN,  pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.DoorbellButton,   GPIO.FALLING, bouncetime=200)
        GPIO.add_event_callback(self.DoorbellButton, self.Button_callback)



        # END of HARDWARE ports ---------------------------------



        self.stolpeStatus = False
        self.vedbodStatus = False
        self.garageStatus = False
        self.stugaStatus  = False

        #Connect to MQTT
        self.client = mqtt.Client("DoorBell") #create new instance
        self.client.connect("sara.local") #connect to broker
        self.client.on_message=self.on_message #attach function to callback
        #self.client.on_disconnect = on_disconnect
        #self.client.on_connect = on_connect

        #self.client.subscribe("house/lights/#")
        #self.client.subscribe("house/doorbell/#")
        self.client.subscribe("stolpe/status/switch:0")
        self.client.subscribe("vedbod/status/switch:0")
        self.client.subscribe("garage/status/switch:0")
        self.client.subscribe("stuga/status/switch:0")

        self.client.subscribe("stolpe/events/rpc")
        self.client.subscribe("vedbod/events/rpc")
        self.client.subscribe("garage/events/rpc")
        self.client.subscribe("stuga/events/rpc")

        self.client.subscribe("house/env")

        self.client.loop_start()

        self.client.publish("stolpe/command",'status_update')
        self.client.publish("vedbod/command",'status_update')
        self.client.publish("garage/command",'status_update')
        self.client.publish("stuga/command", 'status_update')

        self.timer()



    def on_message(self, client, userdata, message):
        payload = str(message.payload.decode("utf-8"))
        #print("message received " ,payload)
        #print("message topic=",message.topic)
        #print("message qos=",message.qos)
        #print("message retain flag=",message.retain)

        js = json.loads(payload)

        if message.topic == "house/env" :
            #print(message.topic)
            #print("message received " ,payload)
            try:
                if "sensor_id" in js :
                    if js['sensor_id'] == "outdoorTemp" :
                        OutdoorTemp = js["properties"]["Temp"]
                        x = str(js["properties"]["Temp"]) + u'\N{DEGREE SIGN}'
                        self.thistemp.set(x)
                        if OutdoorTemp > 0 and OutdoorTemp <= 5:
                            self.templabel.configure(foreground="orange")
                        if OutdoorTemp > 5 :
                            self.templabel.configure(foreground="green")
            except Exception as e:
                logging.info("Error 90" + message.topic + " Error:" + str(e) + "\n" + js)
                pass

            return


        if message.topic == "stolpe/status/switch:0" :
            try:
                if js.get('output') == True :
                    self.stolpeStatus = True
                    self.stolpe.configure(image = self.stolpeON)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " on")
                else:
                    self.stolpeStatus = False
                    self.stolpe.configure(image = self.stolpeOFF)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " off")
            except Exception as e:
                logging.info("Error 10" + message.topic + " Error:" + str(e) + "\n" + js)
                pass


        if message.topic == "stolpe/events/rpc" :
            try:
                if js["params"]["switch:0"]["output"] == True :
                    self.stolpeStatus = True
                    self.stolpe.configure(image = self.stolpeON)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " on")
                if js["params"]["switch:0"]["output"] == False :
                    self.stolpeStatus = False
                    self.stolpe.configure(image = self.stolpeOFF)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " off")
            except Exception as e:
                logging.info("Error 20" + message.topic + " Error:" + str(e) + "\n" + js)
                pass


        if message.topic == "vedbod/status/switch:0" :
            try:
                if js.get('output') == True :
                    self.vedbodStatus = True
                    self.vedbod.configure(image = self.vedbodON)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " on")
                if js.get('output') == False :
                    self.vedbodStatus = False
                    self.vedbod.configure(image = self.vedbodOFF)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " off")
            except Exception as e:
                logging.info("Error 30" + message.topic + " Error:" + str(e) + "\n" + js)
                pass


        if message.topic == "vedbod/events/rpc" :
            try:
                if js["params"]["switch:0"]["output"] == True :
                    self.vedbodStatus = True
                    self.vedbod.configure(image = self.vedbodON)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " on")
                if js["params"]["switch:0"]["output"] == False :
                    self.vedbodStatus = False
                    self.vedbod.configure(image = self.vedbodOFF)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " off")
            except Exception as e:
                logging.info("Error 40" + message.topic + " Error:" + str(e) + "\n" + js)
                pass

        if message.topic == "garage/status/switch:0" :
            try:
                if js.get('output') == True :
                    self.garageStatus = True
                    self.garage.configure(image = self.garageON)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " on")
                if js.get('output') == False :
                    self.garageStatus = False
                    self.garage.configure(image = self.garageOFF)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " off")
            except Exception as e:
                logging.info("Error 50" + message.topic + " Error:" + str(e) + "\n" + js)
                pass


        if message.topic == "garage/events/rpc" :
            try:
                if js["params"]["switch:0"]["output"] == True :
                    self.garageStatus = True
                    self.garage.configure(image = self.garageON)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " on")
                if js["params"]["switch:0"]["output"] == False :
                    self.garageStatus = False
                    self.garage.configure(image = self.garageOFF)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " off")
            except Exception as e:
                logging.info("Error 60" + message.topic + " Error:" + str(e) + "\n" + js)
                pass


        if message.topic == "stuga/status/switch:0" :
            try:
                if js.get('output') == True :
                    self.stugaStatus = True
                    self.stuga.configure(image = self.stugaON)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " on")
                if js.get('output') == False :
                    self.stugaStatus = False
                    self.stuga.configure(image = self.stugaOFF)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " off")
            except Exception as e:
                logging.info("Error 70" + message.topic + " Error:" + str(e) + "\n" + js)
                pass


        if message.topic == "stuga/events/rpc" :
            try:
                if js["params"]["switch:0"]["output"] == True :
                    self.stugaStatus = True
                    self.stuga.configure(image = self.stugaON)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " on")
                if js["params"]["switch:0"]["output"] == False :
                    self.stugaStatus = False
                    self.stuga.configure(image = self.stugaOFF)
                    logging.info(message.topic.split('/')[0] + " " + message.topic.split('/')[2] + " off")
            except Exception as e:
                logging.info("Error 80" + message.topic + " Error:" + str(e) + "\n" + js)
                pass



if __name__ == '__main__':
    root = tkinter.Tk()
    GUI(root)
    root.mainloop()
