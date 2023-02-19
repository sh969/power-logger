import asyncio
from kasa import SmartPlug
import requests
import datetime
import os

# Get the current directory of the script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Define the filename and filepath
filename = "power.csv"
filepath = os.path.join(dir_path, filename)

ip_shelly = "192.168.1.40"
ip_kasa = "192.168.1.194"

try:
    dev_kasa = SmartPlug(ip_kasa)  # We create the instance inside the main loop
except:
    dev_kasa = None
    print("Could not connect to Kasa device")

async def main():
    while True:
        try:
            await dev_kasa.update()  # Request an update
        except:
            pass
        try:
            shelly_readings = requests.get("http://" + ip_shelly + "/status").json()
        except requests.exceptions.ConnectionError:
            shelly_readings = {"emeters": [{"power": -1, "voltage": -1}]}
        try:
            kasa_readings = dev_kasa.emeter_realtime
        except:
            kasa_readings = {"power": -1, "voltage": -1}
        # print line
        print("-"*25)
        # get timestamp in the following format YYYY-MM-DD HH:MM:SS
        timestamp = format(datetime.datetime.fromtimestamp(shelly_readings["unixtime"]).strftime('%Y-%m-%d %H:%M:%S'))
        print(timestamp)
        # print voltage and power from shelly
        print("Shelly: {:.1f} W, {:.1f} V".format(shelly_readings["emeters"][0]["power"], shelly_readings["emeters"][0]["voltage"]))
        # print voltage and power from kasa
        print("Kasa: {:.1f} W, {:.1f} V".format(kasa_readings["power"], kasa_readings["voltage"])) 
        # check if power.csv exists, if not create it
        try:
            open(filepath, "r")
        except FileNotFoundError:
            with open(filepath, "w") as f:
                f.write("time,shelly_power,shelly_voltage,kasa_power,kasa_voltage\n")
        with open(filepath, "a") as f:
            f.write("{},{},{},{},{}\n".format(timestamp, shelly_readings["emeters"][0]["power"], shelly_readings["emeters"][0]["voltage"], kasa_readings["power"], kasa_readings["voltage"]))
        await asyncio.sleep(30.0)  # Sleep some time between updates

if __name__ == "__main__":   
    asyncio.run(main())