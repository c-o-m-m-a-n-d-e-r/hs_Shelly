# coding: utf-8

import time
import json
import urllib2
import ssl
import base64

##!!!!##################################################################################################
#### Own written code can be placed above this commentblock . Do not change or delete commentblock! ####
########################################################################################################
##** Code created by generator - DO NOT CHANGE! **##

class Shelly14169(hsl20_4.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_4.BaseModule.__init__(self, homeserver_context, "SHELLY")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_4.LOGGING_NONE,())
        self.PIN_I_IP=1
        self.PIN_I_PORT=2
        self.PIN_I_POWER=3
        self.PIN_I_BRIGHTNESS=4
        self.PIN_I_INTERVAL=5
        self.PIN_I_TRIGGERSTATUS=6
        self.PIN_I_AUTOFIRMWAREUPDATE=7
        self.PIN_I_TRIGGERFIRMWAREUPDATE=8
        self.PIN_I_REBOOT=9
        self.PIN_I_RESETTOTAL=10
        self.PIN_I_DIMMON=11
        self.PIN_I_DIMMAUS=12
        self.PIN_I_CHANNEL=13
        self.PIN_I_TYPE=14
        self.PIN_I_RED=15
        self.PIN_I_GREEN=16
        self.PIN_I_BLUE=17
        self.PIN_I_WHITE=18
        self.PIN_I_GAIN=19
        self.PIN_I_RED255=20
        self.PIN_I_GREEN255=21
        self.PIN_I_BLUE255=22
        self.PIN_I_WHITE255=23
        self.PIN_I_OPENCLOSE=24
        self.PIN_I_STOP=25
        self.PIN_I_POSITION=26
        self.PIN_I_DURATION=27
        self.PIN_I_CALIBRATE=28
        self.PIN_I_CALLBACKPORT=29
        self.PIN_I_USERNAME=30
        self.PIN_I_PASSWORD=31
        self.PIN_I_ENABLEDEBUG=32
        self.PIN_O_CONNECTIONSTATE=1
        self.PIN_O_POWER=2
        self.PIN_O_BRIGHTNESS=3
        self.PIN_O_LOAD=4
        self.PIN_O_LOADTOTAL=5
        self.PIN_O_OVERLOAD=6
        self.PIN_O_TEMP=7
        self.PIN_O_TEMPALERT=8
        self.PIN_O_FIRMWAREUPDATE=9
        self.PIN_O_RED=10
        self.PIN_O_GREEN=11
        self.PIN_O_BLUE=12
        self.PIN_O_WHITE=13
        self.PIN_O_GAIN=14
        self.PIN_O_RED255=15
        self.PIN_O_GREEN255=16
        self.PIN_O_BLUE255=17
        self.PIN_O_WHITE255=18
        self.PIN_O_EXTTEMP1=19
        self.PIN_O_EXTTEMP2=20
        self.PIN_O_EXTTEMP3=21
        self.PIN_O_POSTION=22
        self.PIN_O_INPUTSTATUS=23
        self.PIN_O_INPUTEVENT=24
        self.PIN_O_HUMIDITY=25
        self.PIN_O_BATTERY=26
        self.PIN_O_LECKAGE=27
        self.PIN_O_MOTION=28
        self.PIN_O_TAMPER=29

########################################################################################################
#### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
###################################################################################################!!!##

        self.INSTANZNAME = "Shelly_0_0"
        self.USERAGENT  = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        self.URLS = {
            "status"  : "/status",
            "reboot"  : "/reboot",
            "update"  : "/ota?update=1",
            "command" : "/{0}/{1}"
        }

        #self.MODULEID = self._get_module_id()

    def parseStatus(self, data):
        jsonData = json.loads(data)
            
        state_on_off = 0
        state_brightness = 0
        state_red = False
        state_green = False
        state_blue = False
        state_white = False
        state_gain = False

        if "inputs" in jsonData:
            if "input" in jsonData["inputs"][self.PIN_I_CHANNEL]:
                self._set_output_value(self.PIN_O_INPUTSTATUS, jsonData["inputs"][self.PIN_I_CHANNEL]["input"])
            if "event" in jsonData["inputs"][self.PIN_I_CHANNEL]:
                self._set_output_value(self.PIN_O_INPUTEVENT, jsonData["inputs"][self.PIN_I_CHANNEL]["event"])
            
        if "relays" in jsonData:
            if 0 <= self.PIN_I_CHANNEL < len(jsonData["relays"]):
                if "ison" in jsonData["relays"][self.PIN_I_CHANNEL]:
                    self.URLS["command"] = "/relay/{0}".format(self.PIN_I_CHANNEL)
                    state_on_off = int(jsonData["relays"][self.PIN_I_CHANNEL]["ison"])
            
            if "lights" in jsonData:
                self.URLS["command"] = "/light/{0}".format(self.PIN_I_CHANNEL)
                state_on_off = int(jsonData["lights"][self.PIN_I_CHANNEL]["ison"])
                
                if "brightness" in jsonData["lights"][self.PIN_I_CHANNEL]:
                    state_brightness = jsonData["lights"][self.PIN_I_CHANNEL]["brightness"]
                if "red" in jsonData["lights"][self.PIN_I_CHANNEL]:
                    state_red = int(jsonData["lights"][self.PIN_I_CHANNEL]["red"])
                if "green" in jsonData["lights"][self.PIN_I_CHANNEL]:
                    state_green = int(jsonData["lights"][self.PIN_I_CHANNEL]["green"])
                if "blue" in jsonData["lights"][self.PIN_I_CHANNEL]:
                    state_blue = int(jsonData["lights"][self.PIN_I_CHANNEL]["blue"])
                if "white" in jsonData["lights"][self.PIN_I_CHANNEL]:
                    state_white = int(jsonData["lights"][self.PIN_I_CHANNEL]["white"])
                if "gain" in jsonData["lights"][self.PIN_I_CHANNEL]:
                    state_gain = int(jsonData["lights"][self.PIN_I_CHANNEL]["gain"])
            
            # Rollers
            if "rollers" in jsonData:
                if "current_pos" in jsonData["rollers"][self.PIN_I_CHANNEL]:
                    self._set_output_value(self.PIN_O_POSTION, jsonData["rollers"][self.PIN_I_CHANNEL]["current_pos"])
            
            # Meters
            if "meters" in jsonData:
                if "overpower" in jsonData["meters"][self.PIN_I_CHANNEL]:
                    if jsonData["meters"][self.PIN_I_CHANNEL]["overpower"]:
                        overpower = 1
                    else:
                        overpower = 0
                    self._set_output_value(self.PIN_O_OVERLOAD, overpower)
                    
                if "total" in jsonData["meters"][self.PIN_I_CHANNEL]:
                    self._set_output_value(self.PIN_O_LOADTOTAL, round( float(jsonData["meters"][self.PIN_I_CHANNEL]["total"]) / 60 / 1000, 2))
                
                if "power" in jsonData["meters"][self.PIN_I_CHANNEL]:
                    self._set_output_value(self.PIN_O_LOAD, round( float(jsonData["meters"][self.PIN_I_CHANNEL]["power"]), 0))
                    
            # eMeters
            if "emeters" in jsonData:
                if "overpower" in jsonData["emeters"][self.PIN_I_CHANNEL]:
                    if jsonData["emeters"][self.PIN_I_CHANNEL]["overpower"]:
                        overpower = 1
                    else:
                        overpower = 0
                    self._set_output_value(self.PIN_O_OVERLOAD, overpower)
                    
                if "total" in jsonData["emeters"][self.PIN_I_CHANNEL]:
                    self._set_output_value(self.PIN_O_LOADTOTAL, round( float(jsonData["emeters"][self.PIN_I_CHANNEL]["total"]) / 60 / 1000, 2))
                
                if "power" in jsonData["emeters"][self.PIN_I_CHANNEL]:
                    self._set_output_value(self.PIN_O_LOAD, round( float(jsonData["emeters"][self.PIN_I_CHANNEL]["power"]), 0))

            # Sensor
            if "sensor" in jsonData:
                if "state" in jsonData["sensor"]:
                    if jsonData["sensor"]["state"] == "open":
                        state = 1
                    else:
                        state = 0
                    self._set_output_value(self.PIN_O_POWER, state)

            if "wifi_sta" in jsonData:
                if jsonData["wifi_sta"]["connected"]:
                    wifi_connection = 1
                else:
                    wifi_connection = 0
                self._set_output_value(self.PIN_O_CONNECTIONSTATE, wifi_connection)

            

            if "overtemperature" in jsonData:
                if jsonData["overtemperature"]:
                    overtemperature = 1
                else:
                    overtemperature = 0
                self._set_output_value(self.PIN_O_TEMPALERT, overtemperature)
            
            if "has_update" in jsonData:
                if jsonData["has_update"]:
                    has_update = 1
                    if self.PIN_I_AUTOFIRMWAREUPDATE:
                        self.fwupdate()
                else:
                    has_update = 0
                
                self._set_output_value(self.PIN_O_FIRMWAREUPDATE, has_update)
                    
            if "tmp" in jsonData:
                self._set_output_value(self.PIN_O_TEMP, round (float (jsonData["tmp"]["tC"]) , 1))
                
            if "red" in jsonData:
                state_red = int(jsonData["red"])
            if "green" in jsonData:
                state_green = int(jsonData["green"])
            if "blue" in jsonData:
                state_blue = int(jsonData["blue"])
            if "white" in jsonData:
                state_white = int(jsonData["white"])
            if "gain" in jsonData:
                state_gain = int(jsonData["gain"])
            
            if state_red is not False:
                self._set_output_value(self.PIN_O_RED, round(state_red / 2.55))
                self._set_output_value(self.PIN_O_RED255, state_red)
            
            if state_green is not False:
                self._set_output_value(self.PIN_O_GREEN, round(state_green / 2.55 ))
                self._set_output_value(self.PIN_O_GREEN255, state_green)
            
            if state_blue is not False:
                self._set_output_value(self.PIN_O_BLUE, round(state_blue / 2.55 ))
                self._set_output_value(self.PIN_O_BLUE255, state_blue)
            
            if state_white is not False:
                self._set_output_value(self.PIN_O_WHITE, round(state_white / 2.55 ))
                self._set_output_value(self.PIN_O_WHITE255, state_white)
            
            if state_gain is not False:
                self._set_output_value(self.PIN_O_GAIN, state_gain)
            
            if "ext_temperature" in jsonData:
                if "0" in jsonData["ext_temperature"]:
                    self._set_output_value(self.PIN_O_EXTTEMP1, round (float(jsonData["ext_temperature"]["0"]["tC"]), 1))
                if "1" in jsonData["ext_temperature"]:
                    self._set_output_value(self.PIN_O_EXTTEMP2, round (float(jsonData["ext_temperature"]["1"]["tC"]), 1))
                if "2" in jsonData["ext_temperature"]:
                    self._set_output_value(self.PIN_O_EXTTEMP3, round (float(jsonData["ext_temperature"]["2"]["tC"]), 1))
                    
            if "ext_humidity" in jsonData:
                if "0" in jsonData["ext_humidity"]:
                    self._set_output_value(self.PIN_O_HUMIDITY, round (float(jsonData["ext_humidity"]["0"]["hum"]), 1))

            if "hum" in jsonData:
                self._set_output_value(self.PIN_O_HUMIDITY, round (float(jsonData["hum"]["value"]), 1))

            if "bat" in jsonData:
                self._set_output_value(self.PIN_O_BATTERY, round (float(jsonData["bat"]["value"]), 1))

            if "flood" in jsonData:
                self._set_output_value(self.PIN_O_LECKAGE, jsonData["flood"])
            
            self._set_output_value(self.PIN_O_POWER, state_on_off)
            self._set_output_value(self.PIN_O_BRIGHTNESS, state_brightness)

    def getStatus(self):
        url = "http://{0}:{1}{2}".format(self.PIN_I_IP, self.PIN_I_PORT, self.URLS["status"])
        response = self.doRequest(url)
        self.parseStatus(response)
        self.log_debug('getStatus', response)

    def reboot(self):
        self.doRequest(self.URLS["reboot"])

    def fwupdate(self):
        self.doRequest(self.URLS["update"])


    def doRequest(self, url):
        headers = {}
        headers['Content-Type'] = 'application/json; charset=UTF-8'
        headers['User-Agent'] = self.USERAGENT
        headers['Connection'] = 'close'
        if self.PIN_I_USERNAME != "" and self.PIN_I_PASSWORD != "":
            auth = "{0}:{1}".format(self.PIN_I_USERNAME, self.PIN_I_PASSWORD)
            headers['Authorization'] = "Basic {0}".format(base64.b64encode(auth))
        
        ctx = ssl._create_unverified_context()
        request = urllib2.Request(url, headers = headers)
        response = urllib2.urlopen(request, context=ctx)
        response_data = response.read()
        return response_data

    def on_init(self):
        self.setDeviceName()
        self.interval = self.FRAMEWORK.create_interval()
        if bool(self._get_input_value(self.PIN_I_INTERVAL)):
            self.interval.set_interval(self._get_input_value(self.PIN_I_INTERVAL) * 1000, self.getStatus)
            self.interval.start()

    def on_input_value(self, index, value):
        if index == self.PIN_I_IP or index == self.PIN_I_PORT:
            self.setDeviceName()

        if index == self.PIN_I_TRIGGERSTATUS and bool(value):
            self.getStatus()

        if index == self.PIN_I_REBOOT and bool(value):
            self.reboot()

        if index == self.PIN_I_TRIGGERFIRMWAREUPDATE and bool(value):
            self.fwupdate()

    def setDeviceName(self):
        self.INSTANZNAME = "Shelly_{0}_{1}".format(self._get_input_value(self.PIN_I_IP), self._get_input_value(self.PIN_I_PORT))

    def log_debug(self, key, value):
        if bool(self._get_input_value(self.PIN_I_ENABLE_DEBUG)):
            if not self.DEBUG:
                self.DEBUG = self.FRAMEWORK.create_debug_section()

            self.DEBUG.set_value(str(key), str(value))

