import json
from datetime import datetime
from twilio.rest import Client
import json

ALARM_FILE = "alarms.json"
REMINDER_FILE = "reminders.json"
CONTACTS_FILE = "contacts.json"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number"
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
ORDERS_FILE = "orders.json"
BILLS_FILE = "bills.json"
NEWS_FILE = "news.json"
MUSIC_FILE = "music.json"
SMART_HOME_FILE = "smart_home.json"
EXPENSES_FILE = "expenses.json"

def set_alarm(time_str: str, message: str = "Alarm ringing!"):
    """Sets an alarm by saving the alarm time and message to a JSON file.  
    Call this function whenever a user wants to set an alarm, for example, when they say,  
    "Set an alarm for 7 AM with the message 'Wake up!'"  

    Args:  
        time_str (str): The alarm time in HH:MM (24-hour format).  
        message (str, optional): A custom message for the alarm. Defaults to "Alarm ringing!".  

    Note: View JSON Schema: set_alarm.args_schema.schema()  

    Returns:  
        dict: A dictionary confirming the alarm has been set, with the following keys:  
            - time (str): The alarm time in HH:MM format.  
            - message (str): The custom message for the alarm.  
    """  
    try:
        alarm_time = datetime.strptime(time_str, "%H:%M").strftime("%H:%M")
        try:
            with open(ALARM_FILE, "r") as file:
                alarms = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            alarms = []
        alarms.append({"time": alarm_time, "message": message})
        with open(ALARM_FILE, "w") as file:
            json.dump(alarms, file, indent=4)

        return f"Alarm set for {alarm_time} with message: '{message}'"

    except ValueError:
        return "Invalid time format. Please use HH:MM (24-hour format)."


def create_reminder(task: str, time_str: str):
    """Creates a reminder by saving the task and time to a JSON file.  
    Call this function whenever a user wants to set a reminder, for example,  
    when they say, "Remind me to take my medicine at 8 PM."  

    Args:  
        task (str): The task or event to be reminded about.  
        time (str): The reminder time in HH:MM (24-hour format).  

    Note: View JSON Schema: create_reminder.args_schema.schema()  

    Returns:  
        dict: A dictionary confirming the reminder has been set, with the following keys:  
            - task (str): The task to be reminded about.  
            - time (str): The reminder time in HH:MM format.  
    """  
    try:
        reminder_time = datetime.strptime(time_str, "%H:%M").strftime("%H:%M")
        try:
            with open(REMINDER_FILE, "r") as file:
                reminders = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            reminders = []
        reminders.append({"task": task, "time": reminder_time})
        with open(REMINDER_FILE, "w") as file:
            json.dump(reminders, file, indent=4)

        return f"Reminder set for {reminder_time} - Task: '{task}'"

    except ValueError:
        return "Invalid time format. Please use HH:MM (24-hour format)."

def call_contact(name: str):
    """Initiates a call to a saved contact.  
    Call this function whenever a user wants to make a call, for example,  
    when they say, "Call John."  

    Args:  
        name (str): The name of the contact to call.  

    Note: View JSON Schema: call_contact.args_schema.schema()  

    Returns:  
        dict: A dictionary containing the call status with the following keys:  
            - name (str): The name of the contact.  
            - status (str): "Calling" if the contact is found, otherwise "Contact not found".  
    """  
    try:
        try:
            with open(CONTACTS_FILE, "r") as file:
                contacts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            contacts = {}

        if name in contacts:
            return {"name": name, "status": "Calling"}
        else:
            return {"name": name, "status": "Contact not found"}

    except Exception as e:
        return {"error": str(e)}
    
def send_message(contact: str, message: str):
    """Sends a message to a saved contact using Twilio API.  
    Call this function whenever a user wants to send a message, for example,  
    when they say, "Send a message to John saying 'Hello!'"  

    Args:  
        contact (str): The name of the contact to send the message to.  
        message (str): The content of the message to be sent.  

    Note: View JSON Schema: send_message.args_schema.schema()  

    Returns:  
        dict: A dictionary containing the message status with the following keys:  
            - contact (str): The name of the recipient.  
            - message (str): The message content.  
            - status (str): "Message sent" if the contact is found and message is sent, otherwise "Contact not found".  
    """  
    try:
        # Load contacts from JSON file
        try:
            with open(CONTACTS_FILE, "r") as file:
                contacts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            contacts = {}

        # Check if contact exists
        if contact in contacts:
            # Get the phone number for the contact
            phone_number = contacts[contact]

            # Twilio client setup
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            # Send the message using Twilio
            message_sent = client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=phone_number
            )

            return {"contact": contact, "message": message, "status": "Message sent"}
        else:
            return {"contact": contact, "message": message, "status": "Contact not found"}

    except Exception as e:
        return {"error": str(e)}

def place_order(item: str, quantity: int):
    """Places an order for a specified item and quantity.  
    Call this function whenever a user wants to order an item, for example,  
    when they say, "Order 2 laptops."  

    Args:  
        item (str): The item to be ordered.  
        quantity (int): The quantity of the item to order.  

    Note: View JSON Schema: place_order.args_schema.schema()  

    Returns:  
        dict: A dictionary confirming the order has been placed, with the following keys:  
            - item (str): The item ordered.  
            - quantity (int): The quantity ordered.  
            - status (str): "Order placed" if the order was successfully placed.  
    """  
    try:
        try:
            with open(ORDERS_FILE, "r") as file:
                orders = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            orders = []

        orders.append({"item": item, "quantity": quantity})

        with open(ORDERS_FILE, "w") as file:
            json.dump(orders, file, indent=4)

        return {"item": item, "quantity": quantity, "status": "Order placed"}

    except Exception as e:
        return {"error": str(e)}


def pay_bill(bill_type: str, amount: float):
    """Pays a utility bill by saving the payment details.  
    Call this function whenever a user wants to pay a bill, for example,  
    when they say, "Pay my electricity bill of $100."  

    Args:  
        bill_type (str): Type of the utility bill (e.g., electricity, water, internet).  
        amount (float): Amount to pay for the bill.  

    Note: View JSON Schema: pay_bill.args_schema.schema()  

    Returns:  
        dict: A dictionary confirming the bill has been paid, with the following keys:  
            - bill_type (str): Type of the bill.  
            - amount (float): The amount paid.  
            - status (str): "Bill paid" if the payment was successful.  
    """  
    try:
        try:
            with open(BILLS_FILE, "r") as file:
                bills = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            bills = []

        bills.append({"bill_type": bill_type, "amount": amount})

        with open(BILLS_FILE, "w") as file:
            json.dump(bills, file, indent=4)

        return {"bill_type": bill_type, "amount": amount, "status": "Bill paid"}

    except Exception as e:
        return {"error": str(e)}


def check_news(category: str):
    """Fetches the latest news for a given category.  
    Call this function to get the latest news, for example,  
    when they say, "Show me the latest tech news."  

    Args:  
        category (str): The news category (e.g., sports, technology, health).  

    Note: View JSON Schema: check_news.args_schema.schema()  

    Returns:  
        dict: A dictionary containing the latest news in the specified category, with the following keys:  
            - category (str): The category of news.  
            - news (list): A list of news headlines.  
    """  
    try:
        news_data = {
            "sports": ["Sports news 1", "Sports news 2"],
            "technology": ["Tech news 1", "Tech news 2"],
            "health": ["Health news 1", "Health news 2"]
        }

        news = news_data.get(category.lower(), ["No news available"])

        return {"category": category, "news": news}

    except Exception as e:
        return {"error": str(e)}


def play_music(genre: str):
    """Plays music based on the genre.  
    Call this function whenever a user wants to play music, for example,  
    when they say, "Play some jazz music."  

    Args:  
        genre (str): The genre of music to play.  

    Note: View JSON Schema: play_music.args_schema.schema()  

    Returns:  
        dict: A dictionary confirming the music genre being played, with the following keys:  
            - genre (str): The genre of music.  
            - status (str): "Playing music" if the music is successfully played.  
    """  
    try:
        music = {"genre": genre, "status": "Playing music"}

        try:
            with open(MUSIC_FILE, "r") as file:
                music_history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            music_history = []

        music_history.append(music)
        with open(MUSIC_FILE, "w") as file:
            json.dump(music_history, file, indent=4)

        return music

    except Exception as e:
        return {"error": str(e)}


def control_smart_home(device: str, action: str):
    """Controls a smart home device by saving the action.  
    Call this function whenever a user wants to control a smart device, for example,  
    when they say, "Turn on the lights."  

    Args:  
        device (str): The smart device to control (e.g., lights, thermostat, door lock).  
        action (str): The action to perform (e.g., turn on, turn off, set temperature).  

    Note: View JSON Schema: control_smart_home.args_schema.schema()  

    Returns:  
        dict: A dictionary confirming the action performed on the device, with the following keys:  
            - device (str): The device controlled.  
            - action (str): The action performed.  
            - status (str): "Action performed" if the control was successful.  
    """  
    try:
        action_details = {"device": device, "action": action}

        try:
            with open(SMART_HOME_FILE, "r") as file:
                smart_home_controls = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            smart_home_controls = []

        smart_home_controls.append(action_details)
        with open(SMART_HOME_FILE, "w") as file:
            json.dump(smart_home_controls, file, indent=4)

        return {"device": device, "action": action, "status": "Action performed"}

    except Exception as e:
        return {"error": str(e)}


def track_expenses(category: str, amount: float):
    """Logs an expense and provides spending insights.  
    Call this function whenever a user wants to track an expense, for example,  
    when they say, "I spent $50 on groceries."  

    Args:  
        category (str): The category of the expense (e.g., groceries, entertainment).  
        amount (float): The amount spent.  

    Note: View JSON Schema: track_expenses.args_schema.schema()  

    Returns:  
        dict: A dictionary confirming the expense has been logged, with the following keys:  
            - category (str): The category of the expense.  
            - amount (float): The amount spent.  
            - status (str): "Expense logged" if the expense was successfully logged.  
    """  
    try:
        try:
            with open(EXPENSES_FILE, "r") as file:
                expenses = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            expenses = []

        expenses.append({"category": category, "amount": amount})

        with open(EXPENSES_FILE, "w") as file:
            json.dump(expenses, file, indent=4)

        return {"category": category, "amount": amount, "status": "Expense logged"}

    except Exception as e:
        return {"error": str(e)}

print(send_message("John Doe", "Hello, how are you?"))
print(call_contact("John Doe"))
print(create_reminder("Take medicine", "20:00"))
print(set_alarm("15:30", "Time for the meeting!"))
print(place_order("Laptop", 2))
print(pay_bill("Electricity", 150.75))
print(check_news("sports"))
print(play_music("Jazz"))
print(control_smart_home("Lights", "Turn On"))
print(track_expenses("Groceries", 50.75))
