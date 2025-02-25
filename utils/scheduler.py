from datetime import datetime
import json
import os
ALARM_FILE = "alarms.json"

def check_alarms():
    try:
        if not os.path.exists(ALARM_FILE):
            return

        with open(ALARM_FILE, "r") as file:
            alarms = json.load(file)

        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%Y-%m-%d")

        for alarm in alarms:
            if alarm["active_status"] and alarm["time"] == current_time and (alarm["date"] == current_date or alarm["date"] == ""):
                print(f"⏰ Alarm Alert: {alarm['message']} at {alarm['time']}!")
                alarm["active_status"] = False  

        with open(ALARM_FILE, "w") as file:
            json.dump(alarms, file, indent=4)

    except Exception as e:
        print(f"Error checking alarms: {e}")

